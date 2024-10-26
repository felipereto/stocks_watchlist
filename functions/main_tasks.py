import logging
import json
from data_extraction import obtener_datos_dolar, get_daily_stock_data
from redshift_operations import load_data_to_redshift


def ccl_to_redshift(**context):
    """
    Obtiene y carga datos del dólar CCL en Redshift.
    
    Args:
        **context: Contexto de ejecución de Airflow.
    """
    end_date = context['ds']
    df = obtener_datos_dolar(end_date)
    table_name = 'pda."2024_felipe_miguel_reto_schema".dolar_ccl'
    load_data_to_redshift(df, table_name)


def stocks_to_redshift(**context):
    """
    Descarga datos de acciones y los carga en Redshift.
    
    Args:
        **context: Contexto de ejecución de Airflow.
    """
    start_date = context['data_interval_start'].strftime('%Y-%m-%d')
    end_date = context['data_interval_end'].strftime('%Y-%m-%d')
    logging.info(f"Proceso iniciado para el rango de fechas: {start_date} a {end_date}")

    with open('/opt/airflow/config/config.json', 'r') as f:
        config = json.load(f)

    tickers = config['tickers']
    logging.info(f"Tickers cargados desde el archivo de configuración: {tickers}")

    df = get_daily_stock_data(start_date, end_date, tickers)
    table_name = 'pda."2024_felipe_miguel_reto_schema".stocks_prices_daily'
    logging.info(f"Cargando datos de {len(tickers)} tickers en la tabla {table_name}")

    load_data_to_redshift(df, table_name)
    logging.info("Proceso finalizado exitosamente.")
