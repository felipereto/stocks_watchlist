import yfinance as yf 
from datetime import date

def get_daily_stock_data(start_date,end_date):
    
    tickers= ["BBAR.BA", "CEPU.BA", "AAPL.BA", "TGNO4.BA", "PAMP.BA", "AMZN.BA"]
    daily_stock_data=yf.download(tickers,start=start_date, end=end_date, interval='1d')
    
    # Utilizo stack para pasar los tickers a filas
    stacked_data = daily_stock_data.stack(level='Ticker').reset_index()
    stacked_data.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)

    return stacked_data 
