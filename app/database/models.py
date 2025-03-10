from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, Time, ForeignKey, Float, Boolean
from datetime import datetime, timezone
from .connection import Base

class ReminderTime(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id")) 
    task = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False, index=True)


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    telegram_id = Column(BigInteger, index=True, unique=True, nullable=False) # index=True: para facilitar las busquedas.
    stripe_customer_id = Column(String(255), nullable=True)  # ID en Stripe
    timezone = Column(String(255), nullable=False)
