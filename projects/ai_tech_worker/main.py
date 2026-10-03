import os
import hmac
import hashlib
from typing import Optional
from pydantic import BaseModel
import httpx
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
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
    tier: str
    telegram_id: Optional[str] = "WEB_GUEST"
    username: Optional[str] = None

class StartCheckRequest(BaseModel):
    telegram_id: str
    username: Optional[str] = None

async def send_telegram_message(chat_id: str, text: str):
    if not TELEGRAM_BOT_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload, timeout=5.0)
    except Exception as e:
        print(f"Telegram notify error: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "AI Tech Worker Platform", "version": "3.0.0"}

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
async def create_qris(req: CreateQRISRequest, db: Session = Depends(get_db)):
    tier_config = {
        "STARTER": {"price": 100000, "tasks": 50, "name": "Starter (50 Tasks)"},
        "ADVANCE": {"price": 249000, "tasks": 150, "name": "Advance (150 Tasks)"},
        "PRO": {"price": 499000, "tasks": 350, "name": "Pro Enterprise (350 Tasks)"}
    }
    
    tier_upper = req.tier.upper()
    if tier_upper not in tier_config:
        raise HTTPException(status_code=400, detail="Pilihan tier paket tidak valid")
        
    cfg = tier_config[tier_upper]
    
    data = {
        "action": "api_create_qris",
        "account_id": BUATQRIS_ACCOUNT_ID,
        "secret_token": BUATQRIS_SECRET_TOKEN,
        "amount": str(cfg["price"]),
        "description": f"Langganan {cfg['name']} AI Tech Worker",
        "fee_by": "user"
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(BUATQRIS_API_URL, data=data, headers=headers, timeout=12.0)
            res_json = res.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gagal menghubungi server BuatQris: {str(e)}")
            
    if not res_json.get("success"):
        raise HTTPException(status_code=400, detail=res_json.get("message", "Gagal generate QRIS"))
        
    trx_data = res_json["data"]
    
    trx = Transaction(
        transaction_id=str(trx_data["transaction_id"]),
        telegram_id=req.telegram_id,
        tier_package=tier_upper,
        tokens_allocated=cfg["tasks"],
        amount=trx_data["amount"],
        total_amount=trx_data["total_amount"],
        status="pending",
        qr_url=trx_data["qr_url"]
    )
    db.add(trx)
    db.commit()
    
    return {
        "status": "success",
        "transaction_id": trx_data["transaction_id"],
        "amount": trx_data["amount"],
        "total_amount": trx_data["total_amount"],
        "qr_url": trx_data["qr_url"],
        "expired_at": trx_data.get("expired_at"),
        "payment_url": trx_data.get("payment_url")
    }

@app.post("/api/payment/webhook")
async def payment_webhook(
    request: Request,
    x_buatqris_signature: Optional[str] = Header(None),
    x_buatqris_event: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    raw_body = await request.body()
    
    if BUATQRIS_SIGNING_SECRET:
        calc_sig = "sha256=" + hmac.new(
            BUATQRIS_SIGNING_SECRET.encode("utf-8"),
            raw_body,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(calc_sig, x_buatqris_signature or ""):
            raise HTTPException(status_code=401, detail="Invalid Webhook Signature")
            
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON Payload")
        
    event = payload.get("event") or x_buatqris_event
    trx_id = str(payload.get("transaction_id", ""))
    
    trx = db.query(Transaction).filter(Transaction.transaction_id == trx_id).first()
    if not trx:
        return {"status": "ignored_unknown_trx"}
        
    if trx.status == "success":
        return {"status": "already_processed"}
        
    if event == "payment.success" or payload.get("status") == "success":
        trx.status = "success"
        user = db.query(User).filter(User.telegram_id == trx.telegram_id).first()
        if user:
            user.tokens_remaining += trx.tokens_allocated
            user.total_tokens_purchased += trx.tokens_allocated
            user.tier = trx.tier_package
            db.commit()
            
            if not trx.telegram_id.startswith("WEB_"):
                msg = (
                    "🎉 *PEMBAYARAN QRIS TERVERIFIKASI!*\n\n"
                    f"• Paket: *{trx.tier_package}*\n"
                    f"• Kuota Masuk: *+{trx.tokens_allocated} Tasks*\n"
                    f"• Total Sisa Kuota: *{user.tokens_remaining} Tasks*\n\n"
                    "AI Tech Worker Anda sudah aktif dan siap mengeksekusi instruksi tugas sekarang! 🚀"
                )
                await send_telegram_message(trx.telegram_id, msg)
                
    elif event in ["payment.expired", "payment.failed"]:
        trx.status = payload.get("status", "failed")
        db.commit()
        
    return {"status": "success"}

# Multi-Page Sub-Route Serving

@app.get("/")
def serve_home():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

@app.get("/skills")
def serve_skills():
    return FileResponse(os.path.join(BASE_DIR, "static", "skills.html"))

@app.get("/skills.html")
def serve_skills_html():
    return FileResponse(os.path.join(BASE_DIR, "static", "skills.html"))

@app.get("/pricing")
def serve_pricing():
    return FileResponse(os.path.join(BASE_DIR, "static", "pricing.html"))

@app.get("/pricing.html")
def serve_pricing_html():
    return FileResponse(os.path.join(BASE_DIR, "static", "pricing.html"))

@app.get("/case-studies")
def serve_cases():
    return FileResponse(os.path.join(BASE_DIR, "static", "case-studies.html"))

@app.get("/case-studies.html")
def serve_cases_html():
    return FileResponse(os.path.join(BASE_DIR, "static", "case-studies.html"))

@app.get("/docs")
def serve_docs():
    return FileResponse(os.path.join(BASE_DIR, "static", "docs.html"))

@app.get("/docs.html")
def serve_docs_html():
    return FileResponse(os.path.join(BASE_DIR, "static", "docs.html"))

@app.get("/tutorial")
@app.get("/tutorial.html")
def serve_tutorial():
    return FileResponse(os.path.join(BASE_DIR, "static", "docs.html"))

@app.get("/about")
def serve_about():
    return FileResponse(os.path.join(BASE_DIR, "static", "about.html"))

@app.get("/about.html")
def serve_about_html():
    return FileResponse(os.path.join(BASE_DIR, "static", "about.html"))

@app.get("/enterprise")
@app.get("/enterprise.html")
def serve_enterprise():
    return FileResponse(os.path.join(BASE_DIR, "static", "enterprise.html"))

@app.get("/umkm")
@app.get("/umkm.html")
def serve_umkm():
    return FileResponse(os.path.join(BASE_DIR, "static", "umkm.html"))

@app.get("/personal")
@app.get("/personal.html")
def serve_personal():
    return FileResponse(os.path.join(BASE_DIR, "static", "personal.html"))

@app.get("/contact")
@app.get("/contact.html")
def serve_contact():
    return FileResponse(os.path.join(BASE_DIR, "static", "contact.html"))

# Static Mount for Assets
static_dir = os.path.join(BASE_DIR, 'static')
if os.path.exists(static_dir):
    app.mount('/static', StaticFiles(directory=static_dir), name='static')
