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
if st.button("재무제표 조회"):

    if corp_code is None:
        st.error("기업명을 확인하세요.")
    else:

        period_type = "F" if period_label == "결산" else "Q"

        rows = icf.get_financial_statement(
            client=client_db,
            corp_code=corp_code,
            year=year,
            period_type=period_type
        )

        if not rows:
            st.info("조회 결과가 없습니다.")
        else:
            df = pd.DataFrame(rows)

            # 보기 좋게 컬럼명 변경(필요 시)
            df = df.rename(columns={
                "corp_code": "기업코드",
                "year": "연도",
                "quarter": "분기",
                "account_cd": "계정코드",
                "report_type": "보고서구분",
                "amt": "금액"
            })

            st.dataframe(df, use_container_width=True)

st.write("입력값 확인")
st.write("기업명:", corp_name)
st.write("기업코드:", corp_code)
st.write("연도:", year)
