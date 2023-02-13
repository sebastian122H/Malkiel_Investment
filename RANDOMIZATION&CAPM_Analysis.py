import yfinance as yf
import pandas as pd
import numpy as np
import openpyxl
import statistics
##  Parsing CSV

etoro_raw = pd.read_csv("etoro_data.csv")
stock_list = etoro_raw["Ticker"].values.tolist()




##  random stock selection and group allocation
stock_num = int(input("How many stocks does every group need?: "))

all_picks = []
for k in range(1,5):
    group_picks = np.random.choice(stock_list,stock_num,replace=False)
    print("Group ", k, "stocks are: ", group_picks)
    all_picks.extend(group_picks)

##  Define Market Rate and Risk free Rate
mrkt_ret = 0.008
risk_f = 0.0346

## Market Returns and Download
dfm = yf.download("SPY", period="5y", interval="1wk", ignore_tz = True, prepost = False)["Close"]

market_returns = []
for i in range(len(dfm)):
    if i +1 < len(dfm):
        market_returns.append((dfm.iloc[i + 1] - dfm.iloc[i]) / dfm.iloc[i])
    else: 
        market_geo_returns = [i + 1 for i in market_returns]
        df_mreturns = pd.DataFrame({"Ret" : market_returns, "Ret + 1" : market_geo_returns})
        variance_market = np.var(df_mreturns["Ret"])

##Stock returns and Download

dfh = yf.download(newlist, period="5y", interval="1wk", ignore_tz = True, prepost = False)["Close"]


for j in range(len(newlist)):
    returns = []
    for i in range(len(dfh)):
        if i +1 < len(dfh):
            returns.append((dfh.iloc[i + 1,j] - dfh.iloc[i,j]) / dfh.iloc[i,j])
        else: 
            continue
    ## Defining the necessary variables to caluclate the VIP variables
    geo_returns = [i + 1 for i in returns]
    df_returns = pd.DataFrame({"Ret" : returns, "Ret + 1" : geo_returns})
    Weeks = len(df_returns)
    Years = len(df_returns)/52
    aar_arith = np.average(df_returns["Ret"])*52
    aar_geo = (np.product(df_returns["Ret + 1"])**(1/Years)) - 1
    variance_stock = np.var(df_returns["Ret"])
    ##VIP Variables that give us the final calculations and data necessary to calculate CAPM
    std_deviation = np.std(df_returns["Ret"])
    if std_deviation != 0:
        sharpe_arith = (aar_arith/std_deviation)
        sharpe_geo = (aar_geo/std_deviation)
        covariance = np.cov(df_returns["Ret"],df_mreturns["Ret"])
        beta = covariance[0,1]/variance_market
        CAPM = risk_f + beta * (mrkt_ret - risk_f)
    analyis_df = pd.DataFrame({"Stock" : stock_list[j], "CAPM" : CAPM, "Beta" : beta, "Sharpe Arith" : sharpe_arith,
    "AAR Arith" :aar_arith,"std. Deviation" : std_deviation}, index=[0])
    print(analyis_df)

analyis_df.to_excel(r'/Users/sebastianhaidinger/code/malkiel/CAPM_stock_analysis.xlsx', index = False)
