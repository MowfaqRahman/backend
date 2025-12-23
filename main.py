from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import schemas, database
from datetime import date
from supabase import Client

app = FastAPI(title="Payment Collection API (Supabase)")

# Enable CORS for Flutter web/mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Payment Collection API", "status": "running", "version": "2.0.0-supabase"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "payment-backend"}

@app.get("/customers", response_model=List[schemas.Customer])
def read_customers(supabase: Client = Depends(database.get_supabase)):
    response = supabase.table("customers").select("*").execute()
    return response.data

@app.post("/payments", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, supabase: Client = Depends(database.get_supabase)):
    # Find customer by account number
    cust_response = supabase.table("customers").select("id").eq("account_number", payment.account_number).execute()
    
    if not cust_response.data:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer_id = cust_response.data[0]["id"]
    
    payment_data = {
        "customer_id": customer_id,
        "payment_amount": payment.amount,
        "status": "Success"
    }
    
    pay_response = supabase.table("payments").insert(payment_data).execute()
    
    if not pay_response.data:
         raise HTTPException(status_code=500, detail="Failed to create payment")
         
    # Convert back to schema format
    res = pay_response.data[0]
    return {
        "id": res["id"],
        "customer_id": res["customer_id"],
        "payment_date": res["payment_date"],
        "amount": res["payment_amount"],
        "status": res["status"]
    }

@app.get("/payments/{account_number}", response_model=List[schemas.Payment])
def read_payment_history(account_number: str, supabase: Client = Depends(database.get_supabase)):
    cust_response = supabase.table("customers").select("id").eq("account_number", account_number).execute()
    
    if not cust_response.data:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer_id = cust_response.data[0]["id"]
    
    pay_response = supabase.table("payments").select("*").eq("customer_id", customer_id).execute()
    
    return [
        {
            "id": p["id"],
            "customer_id": p["customer_id"],
            "payment_date": p["payment_date"],
            "amount": p["payment_amount"],
            "status": p["status"]
        } for p in pay_response.data
    ]

@app.post("/seed")
def seed_data(supabase: Client = Depends(database.get_supabase)):
    # Check if data already exists
    count_response = supabase.table("customers").select("count", count="exact").execute()
    if count_response.count and count_response.count > 0:
        return {"message": "Database already seeded"}
    
    sample_customers = [
        {
            "account_number": "ACC1001",
            "issue_date": "2023-01-15",
            "interest_rate": 12.5,
            "tenure": 24,
            "emi_due": 1500.00
        },
        {
            "account_number": "ACC1002",
            "issue_date": "2023-03-10",
            "interest_rate": 10.0,
            "tenure": 36,
            "emi_due": 2200.50
        },
        {
            "account_number": "ACC1003",
            "issue_date": "2023-06-20",
            "interest_rate": 11.2,
            "tenure": 12,
            "emi_due": 5000.00
        }
    ]
    
    supabase.table("customers").insert(sample_customers).execute()
    return {"message": "Sample data seeded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
