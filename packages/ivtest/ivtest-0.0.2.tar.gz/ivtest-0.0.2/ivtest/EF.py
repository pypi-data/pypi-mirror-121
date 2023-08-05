import pandas as pd
import numpy as np
import scipy.optimize as solver
import math
from .correlation_analysis import log_returns, excise
from .macro_analysis import annualized_std



# 投资组合波动性
def prtf_sd(weights, cov):
    return np.sqrt(np.dot(weights.T, np.dot(cov, weights)))


# 用蒙特卡洛方法模拟权重组合
def monte_carlos_stimulator(df):

    rts = log_returns(df)
    #rt_a = annualized_returns(rts)
    rt_a = rts.mean() * 252
    cov = rts.cov()
    cov_a = cov * 252

    # 生成n个随机投资组合，n为参数
    prtf_rt = []
    prtf_vol = []
    #prtf_w = []

    n_assets = len(df.columns)
    n_prtf = 100000


    for i in range(n_prtf):
        weights = np.random.random(n_assets)
        weights /= np.sum(weights)
        rt = np.dot(weights, rt_a)
        vol = prtf_sd(weights, cov_a)
        
        prtf_rt.append(rt)
        prtf_vol.append(vol)
        #prtf_w.append(weights)

    prtf = pd.DataFrame([prtf_rt, prtf_vol]).T    
    prtf.columns = ['returns', 'volatility']
    prtf['sharpe'] = prtf['returns'] / prtf['volatility']

    return prtf


# 最大夏普比率（负向）
def neg_sharpe(weights, returns, cov):
    std = prtf_sd(weights, cov)
    rt = np.dot(weights, returns)
    return -rt / std



# 用scipy solver（优化函数）找到最大夏普组合的波动性，收益率，权重
def max_sharpe_ratio(df, ytd_days=None, limits=None, date_len=None):

    if date_len != None:
        rts = excise(log_returns(df), date_len, ytd_days)
    else:
        rts = log_returns(df)

    rt_a = rts.mean() * 252
    cov = rts.cov()
    cov_a = cov * 252

    num_assets = len(rt_a)
    args = (rt_a, cov_a)
    x0 = np.array([1.0 / num_assets for x in range(num_assets)]) 
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # 查看是否有自定义上下限
    if limits == None:
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))
    else:
        bounds = tuple((asset['lower'], asset['upper']) for asset in limits)
    
    max_sharpe = solver.minimize(neg_sharpe, x0, args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)

    sd_max = prtf_sd(max_sharpe['x'], cov_a)
    rt_max = np.dot(max_sharpe['x'], rt_a)

    max_sharpe_allocation = pd.DataFrame(max_sharpe['x'], index=df.columns, columns=['allocation'])
    max_sharpe_allocation['allocation'] = [round(i*100, 2) for i in max_sharpe_allocation['allocation']]
    max_sharpe_allocation = max_sharpe_allocation.T

    return max_sharpe_allocation, sd_max, rt_max




# 用scipy solver（优化函数）找到最小波动性组合的波动性，收益率，权重
def min_variance(df, ytd_days=None, limits=None, date_len=None):

    if date_len != None:
        rts = excise(log_returns(df), date_len, ytd_days)
    else:
        rts = log_returns(df)

    rt_a = rts.mean() * 252
    cov = rts.cov()
    cov_a = cov * 252

    num_assets = len(rt_a)
    args = cov_a
    x0 = np.array([1.0 / num_assets for x in range(num_assets)]) 
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # 查看是否有自定义上下限
    if limits == None:
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))
    else:
        bounds = tuple((asset['lower'], asset['upper']) for asset in limits)

    min_vol = solver.minimize(prtf_sd, x0, args=args, method='SLSQP', bounds=bounds, constraints=constraints)

    sd_min = prtf_sd(min_vol['x'], cov_a)
    rt_min = np.dot(min_vol['x'], rt_a)

    min_vol_allocation = pd.DataFrame(min_vol['x'], index=df.columns, columns=['allocation'])
    min_vol_allocation['allocation'] = [round(i*100, 2) for i in min_vol_allocation['allocation']]
    min_vol_allocation = min_vol_allocation.T

    return min_vol_allocation, sd_min, rt_min


# 有效前沿收益
def efficient_return(returns, cov, target, limits=None):
    num_assets = len(returns)
    args = cov
    x0 = np.array([1.0 / num_assets for x in range(num_assets)]) 

    def port_returns(weight):
        return np.dot(weight, returns)

    constraints = (
                    {'type': 'eq', 'fun': lambda x: port_returns(x) - target},
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
                    )
    
    # 查看是否有自定义上下限
    if limits == None:
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))
    else:
        bounds = tuple((asset['lower'], asset['upper']) for asset in limits)

    result = solver.minimize(prtf_sd, x0=x0, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    
    sd = prtf_sd(result['x'], cov)
    rt = np.dot(result['x'], returns)

    ary = np.append(np.append(result['x'], sd), rt)
    idx = returns.index.to_list() + ['std', 'rt']

    return pd.Series(ary, index=idx)


# 有效前沿组合
def efficient_frontier(df, n_prtf, ytd_days=None, limits=None, date_len=None):

    if date_len != None:
        rts = excise(log_returns(df), date_len, ytd_days)
    else:
        rts = log_returns(df)

    rt_a = rts.mean() * 252
    cov = rts.cov()
    cov_a = cov * 252

    rt_min = min_variance(df)[2]
    rt_max = max_sharpe_ratio(df)[2]
    target = np.linspace(rt_min, rt_max, n_prtf)

    efficients = []
    for ret in target:
        efficients.append(efficient_return(rt_a, cov_a, ret, limits))
    
    return efficients


# 投资风险比
# 找出单个基金的收益风险比（年化）
def return_risks_ef(df, ytd_days=None, date_len=None):

    if date_len != None:
        rts = excise(log_returns(df), date_len, ytd_days)
    else:
        rts = log_returns(df)

    stds_annualized = annualized_std(rts)
    rt_annualized = rts.mean() * 252

    rt_risk = pd.DataFrame([stds_annualized, rt_annualized]).T
    rt_risk.columns = ['risks', 'returns']
    rt_risk['sharpe'] = round(rt_risk['returns'] / rt_risk['risks'], 2)

    return rt_risk


# 既定目标收益
def ef_target_returns(tgt_min, tgt_max, n_prtf, df, ytd_days=None, limits=None, date_len=None):

    if tgt_max < tgt_min:
        raise Exception("目标设定错误!")
    else:

        # 用最大夏普和最小方差组合定义目标收益上下限
        rt_min = min_variance(df)[2]
        rt_max = max_sharpe_ratio(df)[2]
        
        if tgt_min < rt_min:
            raise Exception("超过目标下限! 最低下限为" + str(math.ceil(rt_min * 1000) / 1000))
        elif tgt_max > rt_max:
            raise Exception("超过目标上限! 最高上限为" + str(math.floor(rt_max * 1000) / 1000))
        else:
            if date_len != None:
                rts = excise(log_returns(df), date_len, ytd_days)
            else:
                rts = log_returns(df)
                rt_a = rts.mean() * 252
                cov = rts.cov()
                cov_a = cov * 252

                target = np.linspace(tgt_min, tgt_max, n_prtf)

                efficients = []
                for ret in target:
                    efficients.append(efficient_return(rt_a, cov_a, ret, limits))

    return efficients


# 既定目标风险
def ef_target_risks(tgt_min, tgt_max, n_prtf, df, limits=None, date_len=None):

    if tgt_max < tgt_min:
        raise Exception("目标设定错误!")
    else:
        # 由于配置组合是由最小方差所取得，只能用收益推导方差，无法用方差推导收益
        # 用最大夏普和最小方差组合定义目标收益上下限
        std_min = min_variance(df)[1]
        std_max = max_sharpe_ratio(df)[1]

        if tgt_min < std_min:
            raise Exception("超过目标下限! 最低下限为" + str(math.ceil(std_min * 1000) / 1000))
        elif tgt_max > std_max:
            raise Exception("超过目标上限! 最高上限为" + str(math.floor(std_max * 1000) / 1000))
        else:
            efficients = efficient_frontier(df, n_prtf, limits, date_len)

            efficient_portfolios = [p for p in efficients if (p['std'] >= tgt_min) & (p['std'] <= tgt_max)]

    return efficient_portfolios


