import yfinance as yf
import pandas as pd
import numpy as np


dfh = pd.read_csv("HOUS.csv")


returns = []
for i in range(len(dfh)):
    if i +1 < len(dfh):
        returns.append((dfh.iloc[i + 1,5] - dfh.iloc[i,5]) / dfh.iloc[i,5])
    else: 
        geo_returns = [i + 1 for i in returns]
        df_returns = pd.DataFrame({"Ret" : returns, "Ret + 1" : geo_returns})
print(df_returns)


##This has to become the market returns of the SMP 500
market_returns = []
for i in range(len(dfh)):
    if i +1 < len(dfh):
        returns.append((dfh.iloc[i + 1,5] - dfh.iloc[i,5]) / dfh.iloc[i,5])
    else: 
        geo_returns = [i + 1 for i in returns]
        df_returns = pd.DataFrame({"Ret" : returns, "Ret + 1" : geo_returns})
print(df_returns)




















##Required Variables
Weeks = len(df_returns)
Years = len(df_returns)/52
aar_arith = np.average(df_returns["Ret"])*52
aar_geo = (np.product(df_returns["Ret + 1"])**(1/Years)) - 1
variance_stock = np.var(df_returns["Ret"])
std_deviation = np.std(df_returns["Ret"])
sharpe_arith = (aar_arith/std_deviation)
sharpe_geo = (aar_geo/std_deviation)

print(sharpe_arith)
print(sharpe_geo)