import streamlit as st
import pandas as pd
import screening.growth as growth
import inqr.corpNameCodeInqr as ic
from db.con import con


st.set_page_config(layout="wide")
st.title("재무 스크리닝")

client_db = con()

# ---------------------------
# 입력 영역
# ---------------------------

corp_name = st.text_input("기업명", value="")
corp_code = ''
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
    format_func=lambda x: "선택 안함" if x is None else f"{x}분기"
)

revenue_growth = st.number_input(
    "매출 증가율 하한(%)",
    value=0.0,
    step=1.0
)

st.divider()

# ---------------------------
# 결과 초기화
# ---------------------------

if "result_df" not in st.session_state:
    st.session_state.result_df = None
    st.session_state.result_title = None


# ---------------------------
# 공통 출력 함수
# ---------------------------

def render_result(result, title):

    if not result:
        st.warning("조회 결과가 없습니다.")
        return

    df = pd.DataFrame(result)
    df["growth"] = df["growth"].astype(float)

    df = df.rename(columns={
        "corp_name": "기업명",
        "re_cur": "당기 매출",
        "re_base": "기준 매출",
        "growth": "증가율(%)"
    })

    st.session_state.result_title = title
    st.session_state.result_df = df


# ---------------------------
# 버튼 영역
# ---------------------------

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("YoY 전년도 결산 대비"):

        st.session_state.result_df = None

        result1 = growth.get_revenue_growth_yoy(
            client_db,
            year,
            revenue_growth,
            corp_code
        )

        render_result(result1, "YoY 전년도 결산 대비 증가 데이터")


with col2:
    if st.button("YoY 전분기 대비"):

        if quarter is None:
            st.warning("분기를 선택하세요.")
        else:
            st.session_state.result_df = None

            result2 = growth.get_revenue_growth_yoy_quarter(
                client_db,
                year,
                revenue_growth,
                corp_code,
                quarter
            )

            render_result(
                result2,
                f"YoY {quarter}분기 전기 대비 증가 데이터"
            )


with col3:
    if st.button("QoQ 전분기 대비"):

        if quarter is None:
            st.warning("분기를 선택하세요.")
        else:
            st.session_state.result_df = None

            result3 = growth.get_revenue_growth_qoq(
                client_db,
                year,
                revenue_growth,
                corp_code,
                quarter
            )

            render_result(
                result3,
                f"QoQ {quarter}분기 전분기 대비 증가 데이터"
            )


# ---------------------------
# 결과 출력
# ---------------------------

if st.session_state.result_df is not None:

    st.subheader(st.session_state.result_title)

    st.dataframe(
        st.session_state.result_df,
        use_container_width=True,
        column_config={
            "당기 매출": st.column_config.NumberColumn(format="%,d"),
            "기준 매출": st.column_config.NumberColumn(format="%,d"),
            "증가율(%)": st.column_config.NumberColumn(format="%.2f")
        }
    )
