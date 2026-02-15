import streamlit as st
import pandas as pd
import screening.growth as growth
from inqr import corpNameCodeInqr
from db import con

st.set_page_config(page_title="Value Screener", layout="wide")

st.title("📊 가치투자 스크리너 (Local MVP)")

revenue_growth = st.slider("매출 성장률(%)", 3, 20, 10)
roe_limit = st.slider("ROE 최소 (%)", 0, 30, 10)

corp_name = st.text_input("기업명")

year = st.number_input(
    "특정 연도",
    min_value=2000,
    max_value=2100,
    step=1
)

quarter = st.selectbox(
    "특정 분기",
    options=[None, 1, 2, 3, 4],
    format_func=lambda x: "선택 안함" if x is None else f"{x}분기"
)

client_db = con()
corp_code = None

if corp_name.strip():
    corp_code = get_corp_code_by_name(client_db, corp_name.strip())

st.write("corp_code :", corp_code)

if st.button("스크리닝 실행") :

  # 1번 쿼리 : 특정 연도만 필요
  result1 = growth.get_revenue_growth_yoy(client_db, year, revenue_growth, corp_code)

  result2 = None
  result3 = None

  # 2, 3번 쿼리 : 특정 연도 + 특정 분기 필요
  if quarter is not None:
      result2 = growth.get_revenue_growth_yoy_quarter(client_db, year,revenue_growth, corp_code, quarter)
      result3 = growth.get_revenue_growth_qoq(client_db, year,revenue_growth, corp_code, quarter)
    
  data = result1
  df = pd.DataFrame(data)
  df["growth"] = df["growth"].astype(float)
  
  df = df.rename(columns={
    "corp_name": "기업명",
    "re_cur": "당기 매출",
    "re_base": "기준 매출",
    "growth": "증가율(%)"
  })

  st.dataframe(
    df,
    use_container_width=True,
    column_config={
        "당기 매출": st.column_config.NumberColumn(format="%,d"),
        "기준 매출": st.column_config.NumberColumn(format="%,d"),
        "증가율(%)": st.column_config.NumberColumn(format="%.2f")
    }
)

# st.write("1번 쿼리 결과", result1)
# st.write("2번 쿼리 결과", result2)
# st.write("3번 쿼리 결과", result3)

