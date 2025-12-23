import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

if not SUPABASE_URL or not SUPABASE_KEY:
    # Fallback to provided credentials if not in env
    SUPABASE_URL = "https://zplspvcuzjxavdmbpcsa.supabase.co"
    SUPABASE_KEY = "sb_publishable_wxd83d7VhWOcFv9kQHFSvQ_qEHTymYt"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase():
    return supabase
