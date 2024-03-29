import yfinance as yf
import pandas as pd
import numpy as np
import openpyxl

## Creating the Stock list and the randomization <-- Further Optimization possible
df = pd.read_csv("etoro_data.csv")
stock_list = df["Ticker"].values.tolist()

num = int(input("How many stocks does every group need?: "))
group1 = np.random.choice(stock_list,num,replace=False)
group2 = np.random.choice(stock_list,num,replace=False)
group3 = np.random.choice(stock_list,num,replace=False)
group4 = np.random.choice(stock_list,num,replace=False)
print("Group 1 Stocks are: ", group1, "\n Group 2 Stocks are: ", group2, "\n Group 3 Stocks are: ", group3, "\n Group 4 Stocks are: ", group4)

## Create a newlist that combines all the stocks for every group into one big list
newlist = [y for x in [group1, group2, group3,group4] for y in x]
newlist.insert(0,"SPY")

## Define Risk free Rate
risk_f = 0.0346

## Stock+Market returns and Download
dfh = yf.download(newlist, period="5y", interval="1wk", ignore_tz = True, prepost = False)["Adj Close"]
returns = dfh.pct_change()
aar_arith = returns.mean()*52
std_deviation = returns.std()
sharpe_arith = (aar_arith/std_deviation)
covariance = returns.cov()
beta = covariance["SPY"]/returns["SPY"].var()
CAPM = risk_f + beta * (mrkt_ret - risk_f)
df_analysis = pd.DataFrame({"CAPM" : CAPM, "Beta" : beta, "Std_deviation" : std_deviation, "Sharpe Arith" : sharpe_arith, "AAR Arith" : aar_arith})

def to_excel(num):
    df_analysis.to_excel(r'/Users/sebastianhaidinger/code/malkiel/CAPM_stock_analysis.xlsx', index = True, sheet_name= "Analysis"+ num)

to_excel(str(2))
