import yfinance as yf
import pandas as pd
import numpy as np
##  Parsing CSV

etoro_raw = pd.read_csv("etoro_data.csv")
stock_list = etoro_raw["Ticker"].values.tolist()

##  random stock selection and group allocation
stock_num = int(input("How many stocks does every group need?: "))

k = 1
all_picks = []
for k in range(1,5):
    group_picks = np.random.choice(stock_list,stock_num,replace=False)
    print("Group ", k, "stocks are: ", group_picks)
    all_picks.extend(group_picks)

##  Define Market Rate and Risk free Rate
mrkt_ret = 0.008
risk_f = 0.0346

##  market return
market_data = yf.download("SPY", period="5y", interval="1wk", group_by='ticker')
market_returns = market_data['Adj Close'].pct_change().to_list()
market_returns.pop(0)
variance_market = np.var(market_returns)

# market_geo_returns = [i + 1 for i in market_returns]
# df_mreturns = pd.DataFrame({"Ret" : market_returns, "Ret + 1" : market_geo_returns})

##  Stock returns

stock_data = yf.download(all_picks, period="5y", interval="1wk", ignore_tz = True, prepost = False)["Adj Close"]

##  calculation of fundamental indicators
for j in range(len(all_picks)):
    stock_returns = stock_data[all_picks[j]].pct_change().to_list()
    # check that this does not count nan!!!!!!!!!!!
    weeks = len(stock_returns)
    years = weeks/52
    mean_return = stock_returns.mean()
    std_return = stock_returns.std()

    aar_arith = mean_return * 52
    variance_stock = stock_returns.var()
    sharpe_arith = (aar_arith/std_return)
    covariance = np.cov(stock_returns,market_returns)
    beta = covariance/variance_market
    # why not use the market return calculated earlier?
    CAPM = risk_f + beta * (mrkt_ret - risk_f)
    print("Stock: ",all_picks[j], "\n", "CAPM: " ,CAPM, "\n", "Beta: ", beta, "\n", "Sharpe arith: (", sharpe_arith, ")" "\n", "AAR arith: (", aar_arith,")", "\n" "Std. Dev: ",std_return, "\n")
# add more/different indicators?
