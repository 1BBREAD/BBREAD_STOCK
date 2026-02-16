def get_financial_statement(client, corp_code, year, period_type):
    """
    period_type : 'F' (결산) , 'Q' (분기 전체)
    """

    if period_type == "F":
        quarters = [5]
    elif period_type == "Q":
        quarters = [1, 2, 3, 4]
    else:
        raise ValueError("period_type must be 'F' or 'Q'")

    # -----------------------------------
    # 1. CIS 중에서 실제 값 있는 것만
    # -----------------------------------
    cis_resp = (
        client.table("fin_cis_q")
        .select("*")
        .eq("corp_code", corp_code)
        .eq("year", year)
        .eq("report_type", "CIS")
        .in_("quarter", quarters)
        .not_.is_("revenue", "null")
        .execute()
    )

    cis_rows = cis_resp.data or []

    # CIS key set
    cis_key_set = set(
        (
            r["corp_code"],
            r["year"],
            r["quarter"]
        )
        for r in cis_rows
    )

    # -----------------------------------
    # 2. IS 전체
    # -----------------------------------
    is_resp = (
        client.table("fin_cis_q")
        .select("*")
        .eq("corp_code", corp_code)
        .eq("year", year)
        .eq("report_type", "IS")
        .in_("quarter", quarters)
        .execute()
    )

    is_rows = is_resp.data or []

    # -----------------------------------
    # 3. CIS가 존재하는 계정은 IS 제거
    # -----------------------------------
    filtered_is_rows = [
        r for r in is_rows
        if (
            r["corp_code"],
            r["year"],
            r["quarter"]
        ) not in cis_key_set
    ]

    # -----------------------------------
    # 4. 합치기
    # -----------------------------------
    result = cis_rows + filtered_is_rows

    # -----------------------------------
    # 5. 정렬
    # -----------------------------------
    result.sort(
        key=lambda x: (
            x["year"],
            x["quarter"]
        )
    )

    return result
