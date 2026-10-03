# Telegram Dynamic QRIS Gatekeeper Middleware (FastAPI + Payment Gateway)

A standardized, plug-and-play middleware architecture for gatekeeping AI Tech Worker Telegram bots behind an automated Dynamic QRIS paywall.

---

## 1. Architecture Flow

```
[User Telegram]
       │
       ▼ (1. Inbound Webhook: /start or User Prompt)
[FastAPI Gatekeeper Middleware]
       │
       ├──► Query SQLite/Postgres User Balance:
       │      • If remaining_tasks > 0 OR trial_tokens < 8:
       │          └── Pass prompt to Hermes Agent / LLM runtime -> Stream reply back
       │      • If remaining_tasks == 0 AND trial_tokens >= 8:
       │          └── Return Tier Menu + "Beli Paket Kuota" Inline Buttons
       │
       ▼ (2. User clicks Tier button: Starter / Advance / Pro)
[Payment Gateway API] (Tripay / Duitku / Pakasir / Midtrans / Xendit)
       │
       ├──► Generate Dynamic QRIS with unique order_id and nominal
       ├──► Telegram sends QR image + Total amount + 15m expiration timer
       │
       ▼ (3. User scans QRIS & pays via Mobile Banking / E-Wallet)
[Bank / Payment Gateway Webhook]
       │
       ▼ (4. Callback to VPS: POST /api/payment/webhook)
[FastAPI Verification]
       │
       ├──► 1. Verify HMAC-SHA256 signature / Merchant Secret Key
       ├──► 2. Validate payment status == 'PAID' or 'settlement'
       ├──► 3. Atomic DB transaction: increment remaining_tasks (+50 / +150 / +350)
       └──► 4. Send Telegram push notification: "Pembayaran berhasil! Kuota X task aktif."
```

---

## 2. Minimal FastAPI Skeleton

```python
import os
import hmac
import hashlib
import httpx
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(title="AI Agent Telegram QRIS Gatekeeper")

# BuatQris Configuration
BUATQRIS_URL = "https://api.buatqris.site"
BUATQRIS_ACCOUNT_ID = os.getenv("BUATQRIS_ACCOUNT_ID", "YOUR_ACCOUNT_ID")
BUATQRIS_SECRET_TOKEN = os.getenv("BUATQRIS_SECRET_TOKEN", "sk_live_YOUR_SECRET")
BUATQRIS_SIGNING_SECRET = os.getenv("BUATQRIS_SIGNING_SECRET", "YOUR_SIGNING_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your-bot-token")

def verify_buatqris_signature(raw_body: bytes, header_sig: str) -> bool:
    """Verifies HMAC-SHA256 signature from BuatQris webhook using raw request body."""
    calc = "sha256=" + hmac.new(
        BUATQRIS_SIGNING_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(calc, header_sig or "")

@app.post("/api/payment/create-qris")
async def create_qris(telegram_id: str, amount: int, description: str):
    """Generates dynamic QRIS via BuatQris Open API (form-urlencoded single action endpoint)."""
    payload = {
        "action": "api_create_qris",
        "account_id": BUATQRIS_ACCOUNT_ID,
        "secret_token": BUATQRIS_SECRET_TOKEN,
        "amount": amount,
        "description": description[:100],
        "fee_by": "user"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(BUATQRIS_URL, data=payload, timeout=10.0)
        res_json = res.json()
    if not res_json.get("success"):
        raise HTTPException(status_code=500, detail=res_json.get("message", "Gateway Error"))
    return res_json["data"]

@app.post("/api/payment/webhook")
async def payment_webhook(request: Request, background_tasks: BackgroundTasks):
    raw_body = await request.body()
    signature = request.headers.get("X-BuatQris-Signature", "")
    
    # 1. Verify Security Signature on Raw Body
    if not verify_buatqris_signature(raw_body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    data = await request.json()
    event = data.get("event")
    status = data.get("status")
    trx_id = str(data.get("transaction_id"))
    total_amount = data.get("total_amount", 0)
    
    if event == "payment.success" and status == "success":
        # 2. Map nominal to task quota (Match with total_amount including unique code)
        task_quota = 50 if total_amount <= 105000 else (150 if total_amount <= 260000 else 350)
        
        # 3. Update Database (Atomic Increment + Idempotency Check)
        # await db.users.update_one({"current_trx_id": trx_id}, {"$inc": {"remaining_tasks": task_quota}})
        
        # 4. Notify User on Telegram
        # background_tasks.add_task(send_telegram_message, telegram_id, msg)
        
    return {"success": True}
```

---

## 3. Database Schema Recommendations

```sql
CREATE TABLE IF NOT EXISTS users (
    telegram_id BIGINT PRIMARY KEY,
    username VARCHAR(128),
    tier VARCHAR(32) DEFAULT 'trial',
    trial_used INT DEFAULT 0,
    remaining_tasks INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    order_id VARCHAR(64) PRIMARY KEY,
    telegram_id BIGINT REFERENCES users(telegram_id),
    tier VARCHAR(32),
    amount NUMERIC(12, 2),
    qr_string TEXT,
    qr_url TEXT,
    status VARCHAR(32) DEFAULT 'UNPAID', -- UNPAID, PAID, EXPIRED, FAILED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP
);
```
