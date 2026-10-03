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
    
    transaction_id = Column(String(64), primary_key=True, index=True) # ID dari BuatQris
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
