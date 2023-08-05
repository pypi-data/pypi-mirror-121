import pandas as pd
import numpy as np
from datetime import datetime
#from WindPy import *


# 相关性分析

# 整理数据
def clean_data(df):

    df = df.pivot(index='report_date', columns='fund_code', values='anv_y') # values后期要改成复权累计净值
    df.index = pd.to_datetime(df.index)

    return df

# 对数收益率
def log_returns(df):

    return np.log(df / df.shift(1))

# 累计收益率
def cumulative_returns(rt):
    return np.exp(rt.cumsum())

'''
# 摘取函数
def excise(df, date_len):

    w.start()

    len_dict = {'5yr': 1260, 
                '3yr': 756,
                '1yr': 252,
                'ytd': w.tdayscount(datetime(datetime.today().year,1,1), datetime.today().date()).Data[0][0],
                '6mo': 126,
                '3mo': 63,
                '1mo': 21}


    # 摘取的长度必须要小于或等于原有的长度，否则新df跟原df一致
    if len_dict[date_len] <= len(df):
    
        df_new = df.iloc[-len_dict[date_len]:].copy()
    
    else:
        df_new = df.copy()

    return df_new

'''

# 为收益趋势曲线图表准备开始日期一致的收益数据
def collect_rt_plot(df, date_len=None):    

    df = clean_data(df)
    
    # 找到收益数据一致有效的开始日期
    rt = log_returns(df)
    idx_start = rt.loc[:rt.dropna(how='any').index[0]].index[-2]
    rt = rt.loc[idx_start:].copy()
    rt.iloc[0] = np.zeros(len(rt.columns))

    # 摘取设定的时间跨度
    if date_len != None:
        rt = excise(rt, date_len)


    return rt

# 相关系数(时间跨度为参数)
def cal_corr(rt):

    # rt为收益，date_len为时间跨度
    # 返回相关性矩阵

    return rt.corr()






