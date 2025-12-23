import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

if not SUPABASE_URL:
    print("CRITICAL: SUPABASE_URL environment variable is missing!")
if not SUPABASE_KEY:
    print("CRITICAL: SUPABASE_KEY environment variable is missing!")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials. Ensure SUPABASE_URL and SUPABASE_KEY are set.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase():
    return supabase
