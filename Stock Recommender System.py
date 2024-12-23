import numpy as np , pandas as pd, matplotlib.pyplot as plt
import yfinance as yf 
import pandas_ta as ta , mplfinance as mpl 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv("C:\\ind_nifty500list.csv")

stock_universe = df['Symbol'].tolist()

stock_universe = [symbol + '.NS' for symbol in stock_universe]

stock = 'TATAMOTORS.NS'
ticker = yf.Ticker(stock)

#GEtting PE
industry = ticker.info.get('industry')
stock_pe = ticker.info.get('forwardPE')
print(industry)

#GEtting quarterly results
financials = ticker.quarterly_financials

info = ticker.info
print(info)

#Stock Financial
stock_roe = ticker.info.get('returnOnEquity')

stock_rev_growth = ticker.info.get('revenueGrowth')

stock_gross_margin = ticker.info.get('grossMargins')

stock_ebitda_margin = ticker.info.get('ebitdaMargins')

stock_op_margin = ticker.info.get('operatingMargins')

stock_cr = ticker.info.get('currentRatio')

stock_qr = ticker.info.get('quickRatio')

stock_earning_growth = ticker.info.get('earningsQuarterlyGrowth')

stock_target_price = ticker.info.get('targetMedianPrice')

stock_price = ticker.info.get('previousClose')

stock_roa = ticker.info.get('returnOnAssets')

#Testing
print(stock_cr)
print(stock_qr)
print(f"Price is {stock_price}")
print(f"target price is {stock_target_price}")

stock_pnl = ticker.income_stmt

#ICR Calculation
stock_int_exp = stock_pnl.loc['Interest Expense']
stock_ebit = stock_pnl.loc['EBIT']
stock_icr = stock_ebit/stock_int_exp
cur_stock_icr = stock_icr.iloc[0]
print(cur_stock_icr)


#Actual EPS
eps = financials.loc['Diluted EPS']
latest_eps = eps.iloc[0]


cr_score =0

if stock_cr >=1.95 and stock_cr <= 4:
    cr_score=1

print(f"CR Score is {cr_score}")

qr_score = 0
if stock_qr >= 0.95 and stock_qr <=2:
    qr_score=1

print(f"QR Score is {qr_score}")

icr_score = 0
if cur_stock_icr > 2.2:
    icr_score=1
print(f"ICR score is {icr_score} ")

analyst_price_score = 0
if stock_price < stock_target_price:
    analyst_price_score=1

print(f"Analyst price Score is {analyst_price_score}")

stocks_in_industry =[]

#Getting stocks in same industry
for stock_symbol in stock_universe:
        
    tickers = yf.Ticker(stock_symbol)
    stock_industry = tickers.info.get('industry')

    if stock_industry == industry:
        stocks_in_industry.append(stock_symbol)

print(stocks_in_industry)

#Getting PE ratio of comparable firms
pe_ratio =[]

for i in stocks_in_industry:
    pe = yf.Ticker(i).info.get('forwardPE')
    if pe>0:
        pe_ratio.append(pe)

#Average PE RAtio
industry_pe_ratio = (sum(pe_ratio)/len(pe_ratio))
print(industry_pe_ratio)

pe_score = 0

#PE Score
if stock_pe < industry_pe_ratio:
    pe_score =1
else:
    pe_score=0

print(f"PE Score is {pe_score}")

#comparable ROE
roe =[]

for j in stocks_in_industry:
    peer_roe = yf.Ticker(j).info.get('returnOnEquity')
    roe.append(peer_roe)

#Handling none values
filtered_roe = [num for num in roe if num is not None]

industry_roe = np.mean(filtered_roe)

#roe score
roe_score = 0

if stock_roe > industry_roe:
    roe_score = 1

#Comparabele operating margin
op_margin =[]

for k in stocks_in_industry:
    peer_op = yf.Ticker(k).info.get('operatingMargins')
    op_margin.append(peer_op)

filtered_op = [op for op in op_margin if op is not None]

industry_op_margin = np.mean(filtered_op)

op_score = 0

if stock_op_margin > industry_op_margin:
    op_score = 1

print(f"roe score is {roe_score}")
print(f"op_margin score is {op_score}")

roa =[]
for l in stocks_in_industry:
    peer_roa =yf.Ticker(l).info.get('returnOnAssets')
    roa.append(peer_roa)

filtered_roa = [a for a in roa if a is not None]

industry_roa = np.mean(filtered_roa)

roa_score =0

if stock_roa > industry_roa:
    roa_score =1

print(f"roa score is {roa_score}")

total_score = (
    (0.9* cr_score) +
     (0.9*qr_score) +
      (0.18*icr_score) + 
      (0.125*pe_score) +
       (0.18*roe_score) + 
       (0.1*analyst_price_score) +
        (0.1175*roa_score) +
         (0.1175*op_score))

print(f"total score is {total_score}")

if total_score >0.55:
    print(f"This stock is a buy")
elif total_score<0.45:
    print(f"This stock is a sell")
else:
    print(f"This stock is rated Hold")
