import streamlit as st
from st_supabase_connection import SupabaseConnection

def db_con() :
  supabase = st.connection("supabase",type=SupabaseConnection)
  return supabse
