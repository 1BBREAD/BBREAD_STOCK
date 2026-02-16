import streamlit as st
import pandas as pd
import screening.growth as growth
import inqr.corpNameCodeInqr as ic
from db.con import con


st.set_page_config(page_title="Value Screener", layout="wide")

st.title("📊 가치투자 스크리너")

st.write("왼쪽 사이드바에서 기능을 선택하세요.")
