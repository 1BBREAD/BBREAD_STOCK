import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def con() :
  url = st.secrets["SUPABASE_URL"]
  key = st.secrets["SUPABASE_KEY"]
  supabase = create_client(url,key)
  return supabase
