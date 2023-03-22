import yfinance as yf
import pandas as pd
import numpy as np
import openpyxl
##  Parsing CSV
etoro_raw = pd.read_csv("etoro_data.csv")
stock_list = etoro_raw["Ticker"].values.tolist()

##  random stock selection and group allocation
stock_num = int(input("How many stocks does every group need?: "))

all_picks = ["SPY"]
for k in range(1,5):
    group_picks = np.random.choice(stock_list,stock_num,replace=False)
    print("Group ", k, "stocks are: ", group_picks)
    all_picks.extend(group_picks)

##  Define Market Rate and Risk free Rate
mrkt_ret = 0.008
risk_f = 0.0346

# Stock+Market returns and Download
dfh = yf.download(all_picks, period="5y", interval="1wk",
                  ignore_tz=True, prepost=False)["Close"]
returns = dfh.pct_change()
aar_arith = returns.mean()*52
std_deviation = returns.std()
sharpe_arith = (aar_arith/std_deviation)
covariance = returns.cov()
beta = covariance["SPY"]/returns["SPY"].var()
CAPM = risk_f + beta * (mrkt_ret - risk_f)
df_analysis = pd.DataFrame({"CAPM": CAPM, "Beta": beta, "Std_deviation": std_deviation,
                          "Sharpe Arith": sharpe_arith, "AAR Arith": aar_arith})



def to_excel(num):
    df_analysis.to_excel(r'/Users/arthurbirnstiel/desktop/malkiel/CAPM_stock_analysis.xlsx',
                         index=True, sheet_name="Analysis" + num)

to_excel(str(1))
