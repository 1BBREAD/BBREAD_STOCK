def get_revenue_growth_yoy( supabase, in_year, in_growth_rate, in_corp_code ) :
  in_base_year = in_year - 1
  
  res = supabase.rpc(
        "get_revenue_growth_yoy",
        {
            "p_year": in_year,
            "p_base_year": in_base_year,
            "p_growth_rate": in_growth_rate,
            "p_corp_code" : in_corp_code
        }
  ).execute()
  return res.data

def get_revenue_growth_qoq( supabase, in_year, in_growth_rate, in_corp_code, in_quarter ) :
  base_quarter = in_quarter-1
  base_year = in_year
  if ( in_quarter == 1 ) :
    base_quarter = 4
    base_year = in_year-1    
  
  res = supabase.rpc(
        "get_revenue_growth_qoq",
        {
            "p_year": in_year,
            "p_base_year": base_year,
            "p_growth_rate": in_growth_rate,
            "p_corp_code" : in_corp_code,
            "p_quarter" : in_quarter,
            "p_base_quarter" : base_quarter
        }
  ).execute()
  return res.data

def get_revenue_growth_yoy_quarter( supabase, in_year, in_growth_rate, in_corp_code, in_quarter ) :
  in_base_year = in_year-1
  res = supabase.rpc(
        "get_revenue_growth_yoy_quarter",
        {
            "p_year": in_year,
            "p_base_year": in_base_year,
            "p_growth_rate": in_growth_rate,
            "p_corp_code" : in_corp_code,
            "p_quarter" : in_quarter
        }
  ).execute()
  return res.data
