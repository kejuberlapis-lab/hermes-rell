# 04 - Implementasi Middleware & Webhook FastAPI (Integrasi BuatQris)

Dokumen ini berisi kode backend Python FastAPI yang mengintegrasikan bot Telegram AI Tech Worker dengan Open API **BuatQris** (`https://api.buatqris.site`).

---

## 1. Model Database (`models.py`)

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    telegram_id = Column(String(64), primary_key=True, index=True)
    username = Column(String(128), nullable=True)
    tier = Column(String(32), default='TRIAL')          # TRIAL, STARTER, ADVANCE, PRO
    tokens_remaining = Column(Integer, default=8)       # 8 Token Free Trial
    total_tokens_purchased = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = 'transactions'
    
    transaction_id = Column(String(64), primary_key=True, index=True) # Dari BuatQris
    telegram_id = Column(String(64), ForeignKey('users.telegram_id'), nullable=False)
    tier_package = Column(String(32), nullable=False)
    tokens_allocated = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)     # Nominal + kode unik
    status = Column(String(32), default='pending')      # pending, success, expired, failed
    qr_url = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="transactions")
```

---

## 2. Service Integrasi BuatQris & Webhook Server (`app.py`)

```python
import os
import hmac
import hashlib
import httpx
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from models import Base, User, Transaction, sessionmaker, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tech_worker_billing.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

BUATQRIS_API_URL = "https://api.buatqris.site"
BUATQRIS_ACCOUNT_ID = os.getenv("BUATQRIS_ACCOUNT_ID", "YOUR_ACCOUNT_ID")
BUATQRIS_SECRET_TOKEN = os.getenv("BUATQRIS_SECRET_TOKEN", "sk_live_YOUR_TOKEN")
BUATQRIS_SIGNING_SECRET = os.getenv("BUATQRIS_SIGNING_SECRET", "YOUR_SIGNING_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")

app = FastAPI(title="AI Tech Worker - BuatQris Gateway")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper: Kirim Foto / QRIS ke Telegram
async def send_telegram_photo(chat_id: str, photo_url: str, caption: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

# Helper: Kirim Pesan Teks ke Telegram
async def send_telegram_message(chat_id: str, text: str, reply_markup: dict = None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

# Endpoint: Generate Dynamic QRIS via BuatQris
@app.post("/api/payment/create-qris")
async def create_qris(telegram_id: str, tier: str, db: Session = Depends(get_db)):
    tier_config = {
        "STARTER": {"price": 100000, "tasks": 50, "name": "Paket Starter"},
        "ADVANCE": {"price": 249000, "tasks": 150, "name": "Paket Advance"},
        "PRO": {"price": 499000, "tasks": 350, "name": "Paket Pro Enterprise"}
    }
    
    if tier not in tier_config:
        raise HTTPException(status_code=400, detail="Pilihan paket tidak valid")
        
    cfg = tier_config[tier]
    
    # Request form-urlencoded ke BuatQris
    data = {
        "action": "api_create_qris",
        "account_id": BUATQRIS_ACCOUNT_ID,
        "secret_token": BUATQRIS_SECRET_TOKEN,
        "amount": cfg["price"],
        "description": f"Beli {cfg['name']} AI Tech Worker",
        "fee_by": "user"
    }
    
    async with httpx.AsyncClient() as client:
        res = await client.post(BUATQRIS_API_URL, data=data, timeout=10.0)
        res_json = res.json()
        
    if not res_json.get("success"):
        raise HTTPException(status_code=500, detail=res_json.get("message", "Gagal membuat QRIS"))
        
    trx_data = res_json["data"]
    
    # Simpan transaksi ke DB
    trx = Transaction(
        transaction_id=str(trx_data["transaction_id"]),
        telegram_id=telegram_id,
        tier_package=tier,
        tokens_allocated=cfg["tasks"],
        amount=trx_data["amount"],
        total_amount=trx_data["total_amount"],
        status="pending",
        qr_url=trx_data["qr_url"]
    )
    db.add(trx)
    db.commit()
    
    # Kirim Gambar QRIS ke Telegram User
    caption = (
        f"💳 *TAGIHAN PEMBAYARAN QRIS DINAMIS*

"
        f"• Paket: *{cfg['name']} ({cfg['tasks']} Tasks)*
"
        f"• Total Bayar: *Rp {trx_data['total_amount']:,}*
"
        f"• Berlaku Hingga: `{trx_data['expired_at']}`

"
        f"⚠️ *PENTING:* Silakan scan QRIS di atas menggunakan BCA, GoPay, Dana, OVO, ShopeePay, atau m-Banking lain. "
        f"Pastikan nominal transfer sesuai persis (termasuk kode unik) agar aktivasi instan otomatis!"
    )
    await send_telegram_photo(chat_id=telegram_id, photo_url=trx_data["qr_url"], caption=caption)
    
    return {"status": "success", "transaction_id": trx_data["transaction_id"]}

# Endpoint Webhook: Menerima Callback BuatQris
@app.post("/api/payment/webhook")
async def buatqris_webhook(
    request: Request,
    x_buatqris_signature: str = Header(None),
    x_buatqris_event: str = Header(None),
    db: Session = Depends(get_db)
):
    raw_body = await request.body()
    
    # 1. Verifikasi Signature Wajib
    calc_sig = "sha256=" + hmac.new(
        BUATQRIS_SIGNING_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(calc_sig, x_buatqris_signature or ""):
        raise HTTPException(status_code=401, detail="Invalid Webhook Signature")
        
    payload = await request.json()
    event = payload.get("event")
    trx_id = str(payload.get("transaction_id"))
    
    trx = db.query(Transaction).filter(Transaction.transaction_id == trx_id).first()
    if not trx:
        return {"status": "ignored_unknown_transaction"}
        
    # 2. Idempotency Check (Hindari dobel top-up)
    if trx.status == "success":
        return {"status": "already_processed"}
        
    if event == "payment.success" and payload.get("status") == "success":
        trx.status = "success"
        
        # Tambah token user
        user = db.query(User).filter(User.telegram_id == trx.telegram_id).first()
        if user:
            user.tokens_remaining += trx.tokens_allocated
            user.total_tokens_purchased += trx.tokens_allocated
            user.tier = trx.tier_package
            db.commit()
            
            # Notifikasi ke Telegram
            success_msg = (
                f"🎉 *PEMBAYARAN QRIS TERVERIFIKASI!*

"
                f"• Paket: *{trx.tier_package}*
"
                f"• Kuota Masuk: *+{trx.tokens_allocated} Tasks*
"
                f"• Total Sisa Kuota: *{user.tokens_remaining} Tasks*

"
                f"AI Tech Worker Anda sudah aktif dan siap mengeksekusi instruksi tugas sekarang! 🚀"
            )
            await send_telegram_message(chat_id=user.telegram_id, text=success_msg)
            
    elif event in ["payment.expired", "payment.failed"]:
        trx.status = payload.get("status", "failed")
        db.commit()
        
    return {"status": "success"}
```
