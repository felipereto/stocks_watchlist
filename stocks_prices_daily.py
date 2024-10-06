import yfinance as yf 
from datetime import date

tickers= ["BBAR.BA", "CEPU.BA", "AAPL.BA", "TGNO4.BA", "PAMP.BA", "AMZN.BA"]

daily_stock_data = yf.download(tickers, start='2024-10-03', end='2024-10-04', interval='1d' )

print(daily_stock_data)
print(daily_stock_data.head())
