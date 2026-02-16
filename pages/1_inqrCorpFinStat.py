import streamlit as st
import pandas as pd
import inqr.corpNameCodeInqr as ic
from db.con import con

st.set_page_config(layout="wide")

st.title("기업이름을 통해 재무제표를 확인")

corp_name = st.text_input("기업명")
corp_code = ''

client_db = con()

if corp_name.strip():
    corp_code = ic.get_corp_code_by_name(client_db, corp_name.strip())

year = st.number_input(
    "연도",
    min_value=2000,
    max_value=2100,
    step=1,
    value=2024
)

quarter = st.selectbox(
    "분기",
    [None, 1, 2, 3, 4],
    format_func=lambda x: "전체" if x is None else f"{x}분기"
)

st.write("입력값 확인")
st.write("기업명:", corp_name)
st.write("기업코드:", corp_code)
st.write("연도:", year)
st.write("분기:", quarter)
