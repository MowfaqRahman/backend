from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, database
from datetime import date

app = FastAPI(title="Payment Collection API")

# Enable CORS for Flutter web/mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def root():
    return {"message": "Payment Collection API", "status": "running", "version": "1.1.0-deploy-test"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "payment-backend"}

@app.get("/customers", response_model=List[schemas.Customer])
def read_customers(db: Session = Depends(database.get_db)):
    customers = db.query(models.Customer).all()
    return customers

@app.post("/payments", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(database.get_db)):
    # Find customer by account number
    customer = db.query(models.Customer).filter(models.Customer.account_number == payment.account_number).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_payment = models.Payment(
        customer_id=customer.id,
        amount=payment.amount,
        status="Success"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.get("/payments/{account_number}", response_model=List[schemas.Payment])
def read_payment_history(account_number: str, db: Session = Depends(database.get_db)):
    customer = db.query(models.Customer).filter(models.Customer.account_number == account_number).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer.payments

@app.post("/seed")
def seed_data(db: Session = Depends(database.get_db)):
    # Check if data already exists
    if db.query(models.Customer).count() > 0:
        return {"message": "Database already seeded"}
    
    sample_customers = [
        models.Customer(
            account_number="ACC1001",
            issue_date=date(2023, 1, 15),
            interest_rate=12.5,
            tenure=24,
            emi_due=1500.00
        ),
        models.Customer(
            account_number="ACC1002",
            issue_date=date(2023, 3, 10),
            interest_rate=10.0,
            tenure=36,
            emi_due=2200.50
        ),
        models.Customer(
            account_number="ACC1003",
            issue_date=date(2023, 6, 20),
            interest_rate=11.2,
            tenure=12,
            emi_due=5000.00
        )
    ]
    db.add_all(sample_customers)
    db.commit()
    return {"message": "Sample data seeded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
