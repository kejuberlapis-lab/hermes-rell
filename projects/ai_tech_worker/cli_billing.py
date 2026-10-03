#!/usr/bin/env python3
import sys
import os
import argparse
import json
import urllib.request
import urllib.parse
from sqlalchemy.orm import Session
from models import Base, User, Transaction, sessionmaker, create_engine

BASE_DIR = "/home/ubuntu/ai_tech_worker"
DATABASE_URL = f"sqlite:///{BASE_DIR}/tech_worker_billing.db"
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

def check_user(telegram_id: str, username: str = None):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
        if not user:
            # New user
            user = User(
                telegram_id=str(telegram_id),
                username=username,
                tier="UNVERIFIED",
                tokens_remaining=0
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return {"status": "success", "is_new": True, "tokens": 0, "tier": "UNVERIFIED"}
        
        return {
            "status": "success",
            "is_new": False,
            "tokens": user.tokens_remaining,
            "tier": user.tier
        }
    finally:
        db.close()

def create_qris(telegram_id: str, tier: str):
    tier_config = {
        "TRIAL": {"price": 1000, "tasks": 8, "name": "Aktivasi Free Trial (8 Tasks)"},
        "STARTER": {"price": 100000, "tasks": 50, "name": "Starter (50 Tasks)"},
        "ADVANCE": {"price": 249000, "tasks": 150, "name": "Advance (150 Tasks)"},
        "PRO": {"price": 499000, "tasks": 350, "name": "Pro Enterprise (350 Tasks)"}
    }
    
    tier_upper = tier.upper()
    if tier_upper not in tier_config:
        return {"status": "error", "message": f"Tier {tier} tidak valid."}
        
    cfg = tier_config[tier_upper]
    
    payload = {
        "action": "api_create_qris",
        "account_id": BUATQRIS_ACCOUNT_ID,
        "secret_token": BUATQRIS_SECRET_TOKEN,
        "amount": str(cfg["price"]),
        "description": f"Aktivasi {cfg['name']} ID:{telegram_id}",
        "fee_by": "user"
    }
    
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        BUATQRIS_API_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            res_json = json.loads(response.read().decode())
    except Exception as e:
        return {"status": "error", "message": f"Gagal menghubungi BuatQris: {str(e)}"}
        
    if not res_json.get("success"):
        return {"status": "error", "message": res_json.get("message", "Gagal generate QRIS")}
        
    trx_data = res_json["data"]
    
    db: Session = SessionLocal()
    try:
        trx = Transaction(
            transaction_id=str(trx_data["transaction_id"]),
            telegram_id=str(telegram_id),
            tier_package=tier_upper,
            tokens_allocated=cfg["tasks"],
            amount=trx_data["amount"],
            total_amount=trx_data["total_amount"],
            status="pending",
            qr_url=trx_data.get("qr_url", "")
        )
        db.add(trx)
        db.commit()
    finally:
        db.close()
        
    return {
        "status": "success",
        "tier": tier_upper,
        "package_name": cfg["name"],
        "tasks": cfg["tasks"],
        "price_base": cfg["price"],
        "total_amount": trx_data["total_amount"],
        "qr_url": trx_data.get("qr_url"),
        "transaction_id": trx_data["transaction_id"],
        "expired_at": trx_data.get("expired_at")
    }

def deduct_token(telegram_id: str, count: int = 1):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
        if not user:
            return {"status": "error", "message": "User not found", "tokens": 0}
            
        if user.tokens_remaining < count:
            return {
                "status": "insufficient_tokens",
                "tokens": user.tokens_remaining,
                "tier": user.tier,
                "message": "Saldo token habis. Silakan top up via QRIS."
            }
            
        user.tokens_remaining -= count
        user.total_tasks_completed += count
        db.commit()
        db.refresh(user)
        return {
            "status": "success",
            "tokens_remaining": user.tokens_remaining,
            "tasks_completed": user.total_tasks_completed
        }
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["check", "create-qris", "deduct"])
    parser.add_argument("--telegram-id", required=True)
    parser.add_argument("--username", default=None)
    parser.add_argument("--tier", default="TRIAL")
    parser.add_argument("--count", type=int, default=1)
    
    args = parser.parse_args()
    
    if args.action == "check":
        res = check_user(args.telegram_id, args.username)
    elif args.action == "create-qris":
        res = create_qris(args.telegram_id, args.tier)
    elif args.action == "deduct":
        res = deduct_token(args.telegram_id, args.count)
        
    print(json.dumps(res, indent=2))
