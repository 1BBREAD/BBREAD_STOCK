import streamlit as st

st.set_page_config(page_title="Value Screener", layout="wide")

st.title("📊 가치투자 스크리너 (Local MVP)")

per_limit = st.slider("PER 최대", 3, 20, 10)
roe_limit = st.slider("ROE 최소 (%)", 0, 30, 10)

st.button("스크리닝 실행")

st.write("👉 조건을 만족하는 기업 리스트 표시")
