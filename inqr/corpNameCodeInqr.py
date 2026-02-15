
def get_corp_code_by_name(supabase, corp_name: str):
    """
    기업명으로 corp_code 조회
    없으면 None 리턴
    """
    if not corp_name:
        return None
    res = supabase.rpc(
        "get_corpcode_from_name",
        {
            "p_corp_name": '삼성전자'
        }
    ).execute()
    return res.data[0]['corp_code']
