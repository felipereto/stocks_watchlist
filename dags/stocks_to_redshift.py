from load_data_to_redshift import load_data_to_redshift
from stocks_prices_daily import get_daily_stock_data


def stocks_to_redshift(**context):
    
    start_date = context['data_interval_start'].strftime('%Y-%m-%d')
    print(start_date)
    end_date = context['data_interval_end'].strftime('%Y-%m-%d')
    print(end_date)
    tickers= ["BBAR.BA", "CEPU.BA", "AAPL.BA", "TGNO4.BA", "PAMP.BA", "AMZN.BA"]    
    df = get_daily_stock_data(start_date, end_date,tickers) 
    table_name = 'pda."2024_felipe_miguel_reto_schema".stocks_prices_daily'
    load_data_to_redshift(df, table_name)
