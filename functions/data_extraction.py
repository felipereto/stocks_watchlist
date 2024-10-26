import requests
import pandas as pd
import yfinance as yf
import os

def obtener_datos_dolar(period_date):
    """
    Obtiene los datos del dólar CCL para una fecha específica.
    
    Args:
        period_date (str): Fecha en formato 'YYYY-MM-DD'.
    
    Returns:
        pd.DataFrame: DataFrame con columnas ['fecha', 'dolar_ccl'].
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f'https://mercados.ambito.com//dolarrava/cl/grafico/{period_date}/{period_date}'
    response = requests.get(url, headers=headers)
    data = response.json()
    df = pd.DataFrame(data[1:], columns=['fecha', 'dolar_ccl'])
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    return df

def get_daily_stock_data(start_date, end_date, tickers):
    """
    Descarga datos diarios de acciones de Yahoo Finance.
    
    Args:
        start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
        end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.
        tickers (list): Lista de tickers a descargar.
    
    Returns:
        pd.DataFrame: DataFrame con los datos diarios de las acciones.
    """
    # Configura una nueva ubicación de caché para yfinance
    new_cache_location = '/tmp/py-yfinance-cache'
    os.makedirs(new_cache_location, exist_ok=True)
    yf.set_tz_cache_location(new_cache_location)

    daily_stock_data = yf.download(tickers, start=start_date, end=end_date, interval='1d')

    if len(tickers) == 1:
        daily_stock_data['Ticker'] = tickers[0]
        stacked_data = daily_stock_data.reset_index()
    else:
        stacked_data = daily_stock_data.stack(level='Ticker', future_stack=True).reset_index()

    stacked_data.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)
    column_order = ['Date', 'Ticker', 'Adj_Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    stacked_data = stacked_data[[col for col in column_order if col in stacked_data.columns]]
    return stacked_data
