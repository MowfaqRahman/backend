from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    issue_date = Column(Date)
    interest_rate = Column(Float)
    tenure = Column(Integer)  # in months
    emi_due = Column(Float)

    payments = relationship("Payment", back_populates="customer")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)
    amount = Column(Float)
    status = Column(String, default="Success")

    customer = relationship("Customer", back_populates="payments")
