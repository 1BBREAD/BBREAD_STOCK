import streamlit as st
import pandas as pd
import inqr.corpNameCodeInqr as ic
import inqr.corpFinStatInqr as icf
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

# quarter = st.selectbox(
#     "분기",
#     [None, 1, 2, 3, 4],
#     format_func=lambda x: "전체" if x is None else f"{x}분기"
# )
period_label = st.radio(
    "조회 구분",
    ["결산", "분기"]
)

def df_cis(rows) :
    if not rows:
        st.info("조회 결과가 없습니다.")
    else:
        df = pd.DataFrame(rows)

        # 화면에 쓸 컬럼만 정리
        use_cols = [
        "year",
        "quarter",
        "revenue",
        "cost_sles",
        "expenses",
        "oper_income",
        "profit_loss"
        ]

        df2 = df[use_cols]
        # 행/열 뒤집기
        df_t = df2.T

        # 행 이름을 원하는 한글로 변경
        df_t.index = [
        "연도",
        "분기",
        "매출액",
        "매출원가",
        "판관비",
        "영업이익",
        "순이익"
        ]
        # 열 제목을 보기 좋게 (예: 2024-1Q 형태)
        df_t.columns = [ f"{y}년 {q}분기" for y, q in zip(df["year"], df["quarter"]) ]

        st.dataframe(df_t, use_container_width=True)
        
if st.button("재무제표 조회"):

    if corp_code is None:
        st.error("기업명을 확인하세요.")
    else:

        period_type = "F" if period_label == "결산" else "Q"

        rows = icf.get_financial_statement(
            client=client_db,
            corp_code=corp_code,
            period_type=period_type
        )
        df_cis(rows)

st.write("입력값 확인")
st.write("기업명:", corp_name)
st.write("기업코드:", corp_code)
st.write("연도:", year)
