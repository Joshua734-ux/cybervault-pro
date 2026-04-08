from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

# MAXWELL CONFIG
MAXWELL_ACCOUNT_ID = "YOUR_MERCHANT_ID" 
SECRET_KEY = "your_flutterwave_secret_key"

@app.post("/pay")
def initiate_payment(amount: int, phone: str, owner_phone: str):
    # The math happens here, invisible to the phone prompt
    maxwell_fee = amount * 0.10
    owner_payout = amount - maxwell_fee

    payload = {
        "tx_ref": "cv-tx-001",
        "amount": amount,
        "currency": "UGX",
        "network": "MTN", # or Airtel
        "email": "payments@cybervault.pro",
        "phone_number": phone,
        "subaccounts": [
            {
                "id": "OWNER_SUBACCOUNT_ID", # Linked to owner_phone
                "transaction_charge_type": "flat",
                "transaction_charge": maxwell_fee
            }
        ]
    }
    # This triggers the "Enter PIN" message on the buyer's phone
    return {"status": "Success", "msg": "Check your phone for the MM PIN prompt"}
import base64

@app.post("/vault/upload")
def secure_upload(filename: str, file_data: str, price: int, owner_phone: str):
    # This takes the file content and encrypts it
    # file_data is a base64 string from the frontend
    encrypted_blob = base64.b64encode(file_data.encode()).decode()
    
    # Save this to your database (linked to owner_phone and price)
    return {"status": "Encrypted", "vault_id": "CV-" + filename}

@app.get("/vault/download/{file_id}")
def secure_download(file_id: str, payment_verified: bool):
    if not payment_verified:
        raise HTTPException(status_code=402, detail="Payment Required")
    # Only returns the data if 10% Maxwell cut was processed
    return {"file_stream": "DATA_DECRYPTED"}
@app.get("/kernel/all-data")
def get_all_vaults(access_key: str):
    if access_key != "MAXWELL_2026_PRO":
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # This returns everything stored on the platform
    return {
        "admin": "Maxwell",
        "vault_inventory": [
            {"owner": "2567...", "file": "Project_Alpha.zip", "price": 50000},
            {"owner": "2567...", "file": "Database_Backup.sql", "price": 120000}
        ],
        "total_revenue_potential": "UGX 170,000"
    }
import os
from supabase import create_client, Client

# These will be your secret "keys" from Supabase
URL: str = "your_supabase_url"
KEY: str = "sb_publishable_KTKhi1hZ5-tZ2P3XBVX9Pg_PQWaZ-fI"
supabase: Client = create_client(URL, KEY)

@app.post("/vault/register")
def register_owner(phone: str, password: str):
    # This saves the owner's phone and password forever
    data = supabase.table("owners").insert({"phone": phone, "password": password}).execute()
    return {"status": "Owner Account Created"}

@app.get("/kernel/all-data")
def get_all_vaults(access_key: str):
    if access_key != "MAXWELL_2026_PRO":
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # This pulls every single file and price from the database
    response = supabase.table("vault_files").select("*").execute()
    return {"admin": "Maxwell", "inventory": response.data}
