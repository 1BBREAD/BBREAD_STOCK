from supabase import create_client

SUPABASE_URL="https://lwktxccwsldfcxyamraz.supabase.co"
SUPABASE_KEY="sb_publishable_pqiE6JU9ZYbg1wbaHSlRlQ_1Q-J-Iqx"

def db_con() :
  supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
  return supabse
