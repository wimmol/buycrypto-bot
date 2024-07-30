from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_premium = Column(Boolean, nullable=False, default=False)
    language_code = Column(String, nullable=True)
    wallets = Column(String, nullable=True)
    created_at = Column(String, default=datetime.utcnow().__str__)

    orders = relationship("Order", back_populates="user")


class Voucher(Base):
    __tablename__ = 'vouchers'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=True)
    asset_url = Column(String, nullable=True)
    stars_amount = Column(Integer, nullable=False, default=0)
    jetton_amount = Column(Float, nullable=False, default=0.0)
    jetton_name = Column(String, nullable=False)
    jetton_symbol = Column(String, nullable=False)
    ton_amount = Column(Float, nullable=False, default=0.0)
    jetton_address = Column(String, nullable=True)
    balance = Column(Integer, nullable=False, default=0)

    orders = relationship("Order", back_populates="voucher")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    voucher_id = Column(Integer, ForeignKey('vouchers.id'), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(String, default=datetime.utcnow().__str__)

    user = relationship("User", back_populates="orders")
    voucher = relationship("Voucher", back_populates="orders")
