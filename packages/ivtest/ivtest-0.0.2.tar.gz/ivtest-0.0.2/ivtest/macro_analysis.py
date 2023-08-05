import pandas as pd
import numpy as np
from .correlation_analysis import log_returns, cumulative_returns, excise


# 收益风险图

# 年化波动率
def annualized_std(rt):

    return rt.std() * np.sqrt(252)

# 年化收益率
def annualized_returns(rt):

    cum_rt = cumulative_returns(rt)

    return pd.Series([cum_rt[i].dropna().iloc[-1] ** (252 / len(cum_rt[i].dropna())) - 1 for i in cum_rt.columns], index=cum_rt.columns)

# 收益风险组合
def return_risks(df, date_len=None):

    if date_len != None:
        rt = excise(log_returns(df), date_len)
    else:
        rt = log_returns(df)

    stds_annualized = round(annualized_std(rt) * 100, 2)
    rt_annualized = round(annualized_returns(rt) * 100, 2)

    rt_risk = pd.DataFrame([stds_annualized, rt_annualized]).T
    rt_risk.columns = ['risks', 'returns']
    rt_risk['sharpe'] = round(rt_risk['returns'] / rt_risk['risks'], 2)

    return rt_risk
