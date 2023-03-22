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

##Create a newlist that combines all the stocks for every group into one big list
newlist = [y for x in [group1, group2, group3,group4] for y in x]
newlist.insert(0,"SPY")

## Define Market Rate and Risk free Rate
mrkt_ret = 0.008
risk_f = 0.0346

