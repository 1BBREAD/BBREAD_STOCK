import streamlit as st
from supabase import create_client

@st.cache_resource
def con():
  supabase_conf = st.secrets["connections"]["supabase"]
  url = supabase_conf["SUPABASE_URL"]
  key = supabase_conf["SUPABASE_KEY"]
  supabase = create_client(url,key)
  return supabase
