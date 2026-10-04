from datetime import datetime, timedelta
import json
import sqlite3
import re
import os
import hmac
import hashlib
import time
import secrets
import random
from typing import Optional
from pydantic import BaseModel
import httpx
from fastapi import FastAPI, Request, HTTPException, Header, Depends, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, Response, PlainTextResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Base, User, Transaction, sessionmaker, create_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/tech_worker_billing.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Load env credentials
env_file = os.path.join(BASE_DIR, ".env")
env_vars = {}
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env_vars[k] = v

BUATQRIS_API_URL = env_vars.get("BUATQRIS_API_URL", "https://api.buatqris.site")
BUATQRIS_ACCOUNT_ID = env_vars.get("BUATQRIS_ACCOUNT_ID", "")
BUATQRIS_SECRET_TOKEN = env_vars.get("BUATQRIS_SECRET_TOKEN", "")
BUATQRIS_SIGNING_SECRET = env_vars.get("BUATQRIS_SIGNING_SECRET", "")
TELEGRAM_BOT_TOKEN = env_vars.get("TELEGRAM_BOT_TOKEN", "")
ADMIN_SECRET_KEY = env_vars.get("ADMIN_SECRET_KEY", "secret_admin_key_8899")
ADMIN_MASTER_PIN = env_vars.get("ADMIN_MASTER_PIN", "778899")

# Whitelist Official Accounts: Andi (Owner), Sedny (Admin), Avrell (Admin)
WHITELIST_ADMINS = {
    "661471478": "Andi Saputra (Owner)",
    "856579127": "Sedny Mur Prasetyo (Admin)",
    "5955713269": "Avrell (Admin)",
    "728903007": "Admin"
}

ADMIN_OTP_STORE = {}

def create_admin_token(telegram_id: str) -> str:
    exp = int(time.time()) + 86400  # 24 jam
    payload = f"{telegram_id}:{exp}"
    sig = hmac.new(ADMIN_SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"

def verify_admin_token(token: str) -> tuple[bool, str]:
    if not token:
        return False, "Token tidak ditemukan"
    parts = token.split(":")
    if len(parts) != 3:
        return False, "Format token tidak valid"
    tid, exp_str, sig = parts
    if tid not in WHITELIST_ADMINS:
        return False, "Akses ditolak: ID Telegram tidak terdaftar di Whitelist"
    try:
        exp = int(exp_str)
        if time.time() > exp:
            return False, "Sesi login telah kadaluwarsa, silakan login ulang"
    except ValueError:
        return False, "Stempel waktu token tidak valid"
    
    expected_sig = hmac.new(ADMIN_SECRET_KEY.encode(), f"{tid}:{exp_str}".encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(sig, expected_sig):
        return True, tid
    return False, "Tanda tangan token tidak valid"


app = FastAPI(title="AI Tech Worker Platform", docs_url=None, redoc_url=None)

@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Models
class CreateQRISRequest(BaseModel):
    telegram_id: str
    tier: str

class StartCheckRequest(BaseModel):
    telegram_id: str
    username: Optional[str] = None

class AdminOTPRequest(BaseModel):
    telegram_id: str

class AdminVerifyOTPRequest(BaseModel):
    telegram_id: str
    otp: str

class AdminVerifyPINRequest(BaseModel):
    telegram_id: str
    pin: str


async def send_telegram_notify(chat_id: str, text: str, parse_mode: str = "HTML"):
    if not TELEGRAM_BOT_TOKEN:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(url, json=payload, timeout=8.0)
            if res.status_code == 200:
                return True
            elif parse_mode:
                # Fallback to plain text if markup parsing failed
                payload.pop("parse_mode", None)
                res2 = await client.post(url, json=payload, timeout=5.0)
                return res2.status_code == 200
            return False
    except Exception as e:
        print(f"Telegram notify error: {e}")
        return False

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "AI Tech Worker Platform", "version": "3.1.0"}

# --- AUTH ADMIN ENDPOINTS ---

@app.post("/api/admin/auth/request-otp")
async def admin_request_otp(req: AdminOTPRequest):
    tid = req.telegram_id.strip()
    if tid not in WHITELIST_ADMINS:
        return JSONResponse(
            status_code=403,
            content={"status": "error", "message": "ID Telegram tidak terdaftar dalam Whitelist Administrator resmi."}
        )
    
    admin_name = WHITELIST_ADMINS[tid]
    otp = f"{random.randint(100000, 999999)}"
    ADMIN_OTP_STORE[tid] = {
        "otp": otp,
        "exp": time.time() + 300  # 5 menit
    }
    
    tg_text = (
        f"🔐 *KODE VERIFIKASI ADMIN DASHBOARD*\\n\\n"
        f"Halo *{admin_name}*,\\n"
        f"Berikut adalah kode OTP untuk masuk ke Dashboard Laporan:\\n\\n"
        f"👉 *`{otp}`*\\n\\n"
        f"_Kode berlaku selama 5 menit. Dilarang membagikan kode ini kepada pihak lain._"
    )
    sent = await send_telegram_notify(tid, tg_text)
    
    return {
        "status": "success",
        "message": f"Kode OTP 6-digit berhasil dikirim ke Telegram {admin_name}.",
        "telegram_sent": sent
    }

@app.post("/api/admin/auth/verify-otp")
def admin_verify_otp(req: AdminVerifyOTPRequest):
    tid = req.telegram_id.strip()
    otp = req.otp.strip()
    
    if tid not in WHITELIST_ADMINS:
        return JSONResponse(
            status_code=403,
            content={"status": "error", "message": "Akses Ditolak: ID tidak terdaftar."}
        )
        
    stored = ADMIN_OTP_STORE.get(tid)
    if not stored:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "OTP belum diminta atau sudah digunakan. Silakan minta kode baru."}
        )
        
    if time.time() > stored["exp"]:
        ADMIN_OTP_STORE.pop(tid, None)
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Kode OTP telah kadaluwarsa (lebih dari 5 menit). Silakan minta kode baru."}
        )
        
    if stored["otp"] != otp:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Kode OTP salah. Silakan periksa kembali pesan Telegram Anda."}
        )
        
    # Success -> Clear OTP and issue signed token
    ADMIN_OTP_STORE.pop(tid, None)
    token = create_admin_token(tid)
    admin_name = WHITELIST_ADMINS[tid]
    
    return {
        "status": "success",
        "token": token,
        "admin_name": admin_name,
        "telegram_id": tid
    }

@app.post("/api/admin/auth/verify-pin")
def admin_verify_pin(req: AdminVerifyPINRequest):
    tid = req.telegram_id.strip()
    pin = req.pin.strip()
    
    if tid not in WHITELIST_ADMINS:
        return JSONResponse(
            status_code=403,
            content={"status": "error", "message": "Akses Ditolak: ID tidak terdaftar dalam Whitelist."}
        )
        
    if pin != ADMIN_MASTER_PIN:
        return JSONResponse(
            status_code=401,
            content={"status": "error", "message": "Security PIN salah. Silakan coba lagi."}
        )
        
    token = create_admin_token(tid)
    admin_name = WHITELIST_ADMINS[tid]
    
    return {
        "status": "success",
        "token": token,
        "admin_name": admin_name,
        "telegram_id": tid
    }

# --- SECURE METRICS ENDPOINT ---

def format_wib(dt):
    if not dt:
        return "-"
    # dt in SQLite is UTC naive datetime -> convert to WIB (+7 hours)
    wib_time = dt + timedelta(hours=7)
    return wib_time.strftime("%Y-%m-%d %H:%M:%S WIB")

@app.get("/api/admin/metrics")
def get_admin_metrics(db: Session = Depends(get_db)):
    admin_name = "Admin Console" 
    
    users = db.query(User).all()
    transactions = db.query(Transaction).order_by(Transaction.created_at.desc()).all()
    
    # Auto-expire pending transactions older than 30 minutes
    now_utc = datetime.utcnow()
    dirty = False
    for tx in transactions:
        if tx.status == "pending" and tx.created_at:
            diff_seconds = (now_utc - tx.created_at).total_seconds()
            if diff_seconds > 1800:
                tx.status = "expired"
                dirty = True
    if dirty:
        db.commit()
    
    total_users = len(users)
    trial_activations = len([t for t in transactions if t.tier_package == 'TRIAL'])
    
    tx_by_status = {"success": 0, "pending": 0, "expired": 0, "failed": 0}
    package_dist = {"STARTER": 0, "ADVANCE": 0, "PRO": 0, "TRIAL": 0}
    rev_success = 0
    rev_pending = 0
    rev_expired = 0
    
    for tx in transactions:
        st = (tx.status or "").lower()
        if st in ["success", "paid"]:
            tx_by_status["success"] += 1
            rev_success += tx.total_amount or tx.amount
        elif st == "pending":
            tx_by_status["pending"] += 1
            rev_pending += tx.total_amount or tx.amount
        elif st == "expired":
            tx_by_status["expired"] += 1
            rev_expired += tx.total_amount or tx.amount
        else:
            tx_by_status["failed"] += 1
            
        pkg = (tx.tier_package or "").upper()
        if pkg in package_dist:
            package_dist[pkg] += 1
        else:
            package_dist[pkg] = 1
            
    nginx_hits = 0
    unique_ips = set()
    nginx_log = "/var/log/nginx/access.log"
    if os.path.exists(nginx_log):
        try:
            with open(nginx_log, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "techworker.my.id" in line or ":8088" in line:
                        nginx_hits += 1
                        m = re.match(r"^(\d+\.\d+\.\d+\.\d+)", line)
                        if m:
                            unique_ips.add(m.group(1))
        except Exception:
            pass
            
    tx_list = [
        {
            "transaction_id": t.transaction_id,
            "telegram_id": t.telegram_id,
            "tier_package": t.tier_package,
            "tokens_allocated": t.tokens_allocated,
            "amount": t.amount,
            "total_amount": t.total_amount,
            "status": t.status,
            "qr_url": t.qr_url,
            "created_at": format_wib(t.created_at),
            "paid_at": format_wib(t.paid_at)
        }
        for t in transactions
    ]
    
    # Resolve real Telegram names & bot interaction data
    tg_names_map = {}
    for prof in ["profil-admin-mvp", "hermes-support"]:
        c_path = f"/home/ubuntu/.hermes/profiles/{prof}/channel_directory.json"
        if os.path.exists(c_path):
            try:
                with open(c_path) as cf:
                    cd = json.load(cf)
                    for it in cd.get("platforms", {}).get("telegram", []):
                        if it.get("id"):
                            tg_names_map[str(it["id"])] = it.get("name") or "User"
            except Exception:
                pass
                
    mvp_db_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/state.db"
    mvp_stats_map = {}
    if os.path.exists(mvp_db_path):
        try:
            mconn = sqlite3.connect(mvp_db_path)
            mc = mconn.cursor()
            mc.execute("SELECT user_id, display_name, SUM(message_count), MAX(started_at) FROM sessions WHERE user_id IS NOT NULL GROUP BY user_id")
            for mrow in mc.fetchall():
                uid = str(mrow[0])
                mvp_stats_map[uid] = {
                    "display_name": mrow[1],
                    "total_messages": mrow[2] or 0,
                    "last_seen": mrow[3]
                }
            mconn.close()
        except Exception:
            pass

    user_list = []
    for u in users:
        uid = str(u.telegram_id)
        real_name = tg_names_map.get(uid) or (mvp_stats_map.get(uid, {}).get("display_name")) or u.username or "User Telegram"
        msg_count = mvp_stats_map.get(uid, {}).get("total_messages", 0)
        tokens_rem = u.tokens_remaining if u.tokens_remaining is not None else 8
        
        user_list.append({
            "telegram_id": u.telegram_id,
            "username": real_name,
            "tier": u.tier or "TRIAL",
            "tokens_remaining": tokens_rem,
            "tokens_used": max(0, 8 - tokens_rem) if u.tier == "TRIAL" else 0,
            "messages_sent": msg_count,
            "total_tokens_purchased": u.total_tokens_purchased or 0,
            "created_at": format_wib(u.created_at),
            "updated_at": format_wib(u.updated_at)
        })
    
    return {
        "status": "success",
        "admin_name": admin_name,
        "admin_telegram_id": "ADMIN",
        "total_users": total_users,
        "trial_activations": trial_activations,
        "total_transactions": len(transactions),
        "transactions_by_status": tx_by_status,
        "package_distribution": package_dist,
        "revenue_success": rev_success,
        "revenue_pending": rev_pending,
        "revenue_expired": rev_expired,
        "nginx_hits": nginx_hits,
        "nginx_unique_ips": len(unique_ips),
        "transactions": tx_list,
        "users": user_list
    }

# --- STANDARD USER & BILLING ENDPOINTS ---

@app.post("/api/user/start")
def user_start(req: StartCheckRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == req.telegram_id).first()
    if not user:
        user = User(
            telegram_id=req.telegram_id,
            username=req.username,
            tier='TRIAL',
            tokens_remaining=8
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "status": "success",
            "is_new": True,
            "tokens": 8,
            "tier": "TRIAL",
            "message": "Selamat datang! Anda mendapatkan 8 Token Free Trial untuk eksekusi tugas."
        }
    
    return {
        "status": "success",
        "is_new": False,
        "tokens": user.tokens_remaining,
        "tier": user.tier
    }

@app.post("/api/payment/create-qris")
def create_qris(req: CreateQRISRequest, db: Session = Depends(get_db)):
    import urllib.request
    import urllib.parse
    import json
    
    tier_config = {
        "TRIAL": {"price": 1000, "tasks": 8, "name": "Lihat Bagaimana Virtual Tech Worker Bekerja (8 Token)"},
        "STARTER": {"price": 99000, "tasks": 50, "name": "Starter (50 Token)"},
        "ADVANCE": {"price": 249000, "tasks": 150, "name": "Advance (150 Token)"},
        "PRO": {"price": 499000, "tasks": 350, "name": "Pro Enterprise (350 Token)"}
    }
    
    tier_upper = req.tier.upper()
    if tier_upper not in tier_config:
        raise HTTPException(status_code=400, detail="Paket langganan tidak valid.")
        
    cfg = tier_config[tier_upper]
    amount = cfg["price"]
    tokens = cfg["tasks"]
    
    # Batasan Maksimal 2x Trial per Akun Telegram
    if tier_upper == "TRIAL":
        tid_str = str(req.telegram_id).strip()
        trial_paid_count = db.query(Transaction).filter(
            Transaction.telegram_id == tid_str,
            Transaction.tier_package == "TRIAL",
            Transaction.status.in_(["success", "paid"])
        ).count()
        
        if trial_paid_count >= 2:
            raise HTTPException(
                status_code=400,
                detail="Batas Maksimal Uji Coba Tercapai (Maksimal 2x per Akun Telegram). Anda sudah menggunakan 2 kali kuota Uji Coba. Untuk melanjutkan pekerjaan operasional, silakan pilih Paket Starter (50 Token · Rp 99.000)."
            )
    
    payload = {
        "action": "api_create_qris",
        "account_id": BUATQRIS_ACCOUNT_ID,
        "secret_token": BUATQRIS_SECRET_TOKEN,
        "amount": str(amount),
        "description": f"Aktivasi {cfg['name']} ID:{req.telegram_id}",
        "fee_by": "user"
    }
    
    data_bytes = urllib.parse.urlencode(payload).encode("utf-8")
    request_obj = urllib.request.Request(
        BUATQRIS_API_URL,
        data=data_bytes,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    
    try:
        with urllib.request.urlopen(request_obj, timeout=15.0) as response:
            res_json = json.loads(response.read().decode())
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gagal menghubungi BuatQris API: {str(e)}")
        
    if not res_json.get("success"):
        raise HTTPException(status_code=502, detail=res_json.get("message", "Gagal generate QRIS."))
        
    trx_data = res_json.get("data", {})
    tx_id = str(trx_data.get("transaction_id"))
    total_amount = int(trx_data.get("total_amount", amount))
    qr_url = trx_data.get("qr_url")
    qr_image = trx_data.get("qris_image", qr_url)
    
    tx = Transaction(
        transaction_id=tx_id,
        telegram_id=req.telegram_id,
        tier_package=tier_upper,
        tokens_allocated=tokens,
        amount=amount,
        total_amount=total_amount,
        status='pending',
        qr_url=qr_url
    )
    db.add(tx)
    db.commit()
    
    return {
        "status": "success",
        "transaction_id": tx_id,
        "tier": tier_upper,
        "package_name": cfg["name"],
        "tokens": tokens,
        "amount": amount,
        "total_amount": total_amount,
        "qr_url": qr_url,
        "qr_image": qr_image,
        "instructions": f"Silakan scan QRIS di atas dengan GoPay/OVO/Dana/BCA/ShopeePay. Total bayar tepat Rp {total_amount:,}."
    }

@app.get("/api/payment/check/{transaction_id}")
def check_payment_status(transaction_id: str, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan.")
    
    # Auto-expire if pending for more than 30 minutes (1800 seconds)
    if tx.status == "pending" and tx.created_at:
        diff_seconds = (datetime.utcnow() - tx.created_at).total_seconds()
        if diff_seconds > 1800:
            tx.status = "expired"
            db.commit()
            db.refresh(tx)
            
    return {
        "status": "success",
        "transaction_id": tx.transaction_id,
        "payment_status": tx.status,
        "tier": tx.tier_package,
        "tokens": tx.tokens_allocated,
        "amount": tx.amount,
        "total_amount": tx.total_amount,
        "paid_at": format_wib(tx.paid_at) if tx.paid_at else None
    }

@app.post("/api/payment/webhook")
async def buatqris_webhook(request: Request, db: Session = Depends(get_db)):
    raw_body = await request.body()
    signature = (
        request.headers.get("X-BuatQris-Signature")
        or request.headers.get("x-buatqris-signature")
        or request.headers.get("X-Signature")
        or request.headers.get("x-signature")
    )
    
    if BUATQRIS_SIGNING_SECRET and signature:
        raw_digest = hmac.new(
            BUATQRIS_SIGNING_SECRET.encode(),
            raw_body,
            hashlib.sha256
        ).hexdigest()
        
        valid = (
            hmac.compare_digest(signature, raw_digest)
            or hmac.compare_digest(signature, f"sha256={raw_digest}")
        )
        if not valid:
            raise HTTPException(status_code=401, detail="Invalid HMAC webhook signature")
            
    payload = await request.json()
    tx_id = payload.get("transaction_id") or payload.get("data", {}).get("transaction_id")
    status = payload.get("status") or payload.get("data", {}).get("status")
    
    tx = db.query(Transaction).filter(Transaction.transaction_id == tx_id).first()
    if not tx:
        return {"status": "ignored", "message": "Transaction not found"}
        
    if status == "success" and tx.status != "success":
        tx.status = "success"
        tx.paid_at = datetime.utcnow()
        
        user = db.query(User).filter(User.telegram_id == tx.telegram_id).first()
        if user:
            user.tier = tx.tier_package
            user.tokens_remaining += tx.tokens_allocated
            user.total_tokens_purchased += tx.tokens_allocated
        else:
            user = User(
                telegram_id=tx.telegram_id,
                tier=tx.tier_package,
                tokens_remaining=tx.tokens_allocated,
                total_tokens_purchased=tx.tokens_allocated
            )
            db.add(user)
            
        db.commit()
        
        tier_title = tx.tier_package.upper()
        tokens_cnt = tx.tokens_allocated
        total_paid = f"{tx.total_amount:,}".replace(",", ".")
        
        msg = (
            f"🎉 <b>PEMBAYARAN BERHASIL DIVERIFIKASI!</b>\n\n"
            f"Halo! Pembayaran QRIS Anda sebesar <b>Rp {total_paid}</b> telah kami terima dan diverifikasi secara otomatis.\n\n"
            f"📋 <b>Detail Akun & Kuota Anda:</b>\n"
            f"• <b>Paket Langganan:</b> {tier_title}\n"
            f"• <b>Kuota Tugas:</b> {tokens_cnt} Token Eksekusi\n"
            f"• <b>Status Akun:</b> 🟢 Aktif & Siap Bekerja\n\n"
            f"🤖 <b>Silakan Mulai Menggunakan Saya Sekarang!</b>\n"
            f"Saya adalah AI Tech Worker Anda. Anda bisa langsung memberikan instruksi pekerjaan teknis apa pun di sini, ketikkan tugas atau pertanyaan pertama Anda sekarang untuk langsung saya eksekusi!"
        )
        await send_telegram_notify(tx.telegram_id, msg, parse_mode="HTML")
        
    elif status in ["expired", "failed"]:
        tx.status = status
        db.commit()
        
    return {"status": "ok", "message": "Webhook processed successfully"}

# --- STATIC MULTI-PAGE ROUTES ---

@app.api_route("/", methods=["GET", "HEAD"])
def serve_home():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

@app.api_route("/skills", methods=["GET", "HEAD"])
@app.api_route("/skills.html", methods=["GET", "HEAD"])
def serve_skills():
    return FileResponse(os.path.join(BASE_DIR, "static", "skills.html"))

@app.api_route("/pricing", methods=["GET", "HEAD"])
@app.api_route("/pricing.html", methods=["GET", "HEAD"])
def serve_pricing():
    return FileResponse(os.path.join(BASE_DIR, "static", "pricing.html"))

@app.api_route("/case-studies", methods=["GET", "HEAD"])
@app.api_route("/case-studies.html", methods=["GET", "HEAD"])
def serve_cases():
    return FileResponse(os.path.join(BASE_DIR, "static", "case-studies.html"))

@app.api_route("/docs", methods=["GET", "HEAD"])
@app.api_route("/docs.html", methods=["GET", "HEAD"])
@app.api_route("/tutorial", methods=["GET", "HEAD"])
@app.api_route("/tutorial.html", methods=["GET", "HEAD"])
def serve_docs():
    return FileResponse(os.path.join(BASE_DIR, "static", "docs.html"))

@app.api_route("/about", methods=["GET", "HEAD"])
@app.api_route("/about.html", methods=["GET", "HEAD"])
def serve_about():
    return FileResponse(os.path.join(BASE_DIR, "static", "about.html"))

@app.api_route("/enterprise", methods=["GET", "HEAD"])
@app.api_route("/enterprise.html", methods=["GET", "HEAD"])
def serve_enterprise():
    return FileResponse(os.path.join(BASE_DIR, "static", "enterprise.html"))

@app.api_route("/umkm", methods=["GET", "HEAD"])
@app.api_route("/umkm.html", methods=["GET", "HEAD"])
def serve_umkm():
    return FileResponse(os.path.join(BASE_DIR, "static", "umkm.html"))

@app.api_route("/personal", methods=["GET", "HEAD"])
@app.api_route("/personal.html", methods=["GET", "HEAD"])
def serve_personal():
    return FileResponse(os.path.join(BASE_DIR, "static", "personal.html"))

@app.api_route("/contact", methods=["GET", "HEAD"])
@app.api_route("/contact.html", methods=["GET", "HEAD"])
def serve_contact():
    return FileResponse(os.path.join(BASE_DIR, "static", "contact.html"))

@app.api_route("/dashboard", methods=["GET", "HEAD"])
@app.api_route("/dashboard.html", methods=["GET", "HEAD"])
@app.api_route("/admin", methods=["GET", "HEAD"])
def serve_dashboard():
    return FileResponse(os.path.join(BASE_DIR, "static", "dashboard.html"))

@app.api_route("/robots.txt", methods=["GET", "HEAD"])
def serve_robots():
    return FileResponse(os.path.join(BASE_DIR, "static", "robots.txt"), media_type="text/plain")

@app.api_route("/sitemap.xml", methods=["GET", "HEAD"])
def serve_sitemap():
    return FileResponse(os.path.join(BASE_DIR, "static", "sitemap.xml"), media_type="application/xml")

@app.api_route("/llms.txt", methods=["GET", "HEAD"])
def serve_llms():
    return FileResponse(os.path.join(BASE_DIR, "static", "llms.txt"), media_type="text/plain; charset=utf-8")

@app.api_route("/a7d9f2b4c8e146039582710364958102.txt", methods=["GET", "HEAD"])
def serve_indexnow_key():
    return FileResponse(os.path.join(BASE_DIR, "static", "a7d9f2b4c8e146039582710364958102.txt"), media_type="text/plain")

@app.api_route("/google9710c4f647f38670.html", methods=["GET", "HEAD"])
def serve_google_verify():
    return FileResponse(os.path.join(BASE_DIR, "static", "google9710c4f647f38670.html"), media_type="text/html")

# Static Mount for Assets
static_dir = os.path.join(BASE_DIR, 'static')
if os.path.exists(static_dir):
    app.mount('/static', StaticFiles(directory=static_dir), name='static')
