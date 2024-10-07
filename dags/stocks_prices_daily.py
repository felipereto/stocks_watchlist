import yfinance as yf


def get_daily_stock_data(start_date, end_date, tickers):
    daily_stock_data = yf.download(
        tickers, start=start_date, end=end_date, interval='1d'
    )

    if len(tickers) == 1:
        # Si solo es un ticker, agregar una columna 'Ticker' manualmente
        daily_stock_data['Ticker'] = tickers[0]
        stacked_data = daily_stock_data.reset_index()
    else:
        # Si hay más de un ticker, usar stack como antes
        stacked_data = daily_stock_data.stack(level='Ticker').reset_index()

    stacked_data.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)

    column_order = ['Date', 'Ticker', 'Adj_Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    stacked_data = stacked_data[[col for col in column_order if col in stacked_data.columns]]

    return stacked_data
