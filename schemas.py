from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

class PaymentBase(BaseModel):
    amount: float
    account_number: str

class PaymentCreate(PaymentBase):
    pass

class Payment(BaseModel):
    id: int
    customer_id: int
    payment_date: datetime
    amount: float
    status: str

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    account_number: str
    issue_date: date
    interest_rate: float
    tenure: int
    emi_due: float

class Customer(CustomerBase):
    id: int
    
    class Config:
        from_attributes = True

class CustomerWithHistory(Customer):
    payments: List[Payment] = []
