import logging
import psycopg2
from psycopg2.extras import execute_values
from airflow.hooks.base import BaseHook
from functools import wraps


def redshift_connection(func):
    """
    Decorador para establecer y cerrar una conexión a Redshift.
    
    Args:
        func (function): Función a decorar, que recibe 'conn' como primer argumento.
    
    Returns:
        function: La función decorada con una conexión a Redshift.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Estableciendo conexión con Redshift.")
        redshift_conn = BaseHook.get_connection('redshift_conn')
        conn = psycopg2.connect(
            dbname=redshift_conn.schema,
            user=redshift_conn.login,
            password=redshift_conn.password,
            host=redshift_conn.host,
            port=redshift_conn.port
        )
        logging.info("Conexión con Redshift establecida. Ejecutando función.")
        result = func(conn, *args, **kwargs)
        conn.close()
        logging.info("Conexión con Redshift cerrada.")
        return result
    return wrapper


@redshift_connection
def load_data_to_redshift(conn, df, tabla):
    """
    Carga un DataFrame en una tabla de Redshift.
 
    Args:
        conn (psycopg2.connection): Conexión a Redshift.
        df (pd.DataFrame): DataFrame a cargar.
        tabla (str): Nombre de la tabla en Redshift.
    """
    logging.info("Iniciando carga de datos en Redshift.")
    cur = conn.cursor()
    cols = ",".join([f'"{col}"' for col in df.columns])
    query = f"INSERT INTO {tabla} ({cols}) VALUES %s"
    data = [tuple(row) for row in df.to_numpy()]
    execute_values(cur, query, data)
    conn.commit()
    cur.close()
    logging.info("Carga de datos completada exitosamente.")


def execute_query():
    logging.info("Iniciando ejecución de la consulta en Redshift.")

    # Obtener la conexión a Redshift desde Airflow
    redshift_conn = BaseHook.get_connection('redshift_conn')

    # Crear la conexión de psycopg2 a Redshift
    conn = psycopg2.connect(
        dbname=redshift_conn.schema,
        user=redshift_conn.login,
        password=redshift_conn.password,
        host=redshift_conn.host,
        port=redshift_conn.port
    )
    cur = conn.cursor()

    query = """
    TRUNCATE pda."2024_felipe_miguel_reto_schema".stocks_holding;

    INSERT INTO pda."2024_felipe_miguel_reto_schema".stocks_holding
    WITH last_value_ticker AS (
        SELECT date, ticker, close
        FROM (
            SELECT date, ticker, close,
                ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date DESC) AS row_n
            FROM pda."2024_felipe_miguel_reto_schema".stocks_prices_daily
        ) AS subquery
        WHERE row_n = 1
    )
    SELECT t.ticker,
        t."date",
        t.gross_cost,
        t.gross_cost / c.dolar_ccl AS gross_cost_usd,
        s.close / c.dolar_ccl AS last_price_usd,
        ((s.close * t.nominal_quantity) / c.dolar_ccl) AS current_holding,
        ((s.close * t.nominal_quantity) / c.dolar_ccl) - (t.gross_cost / c.dolar_ccl) AS profit,
        ((s.close * t.nominal_quantity) / c.dolar_ccl) / (t.gross_cost / c.dolar_ccl) - 1 AS var_perc
    FROM pda."2024_felipe_miguel_reto_schema".stocks_transactions t
    LEFT JOIN pda."2024_felipe_miguel_reto_schema".dolar_ccl c ON t."date" = c.fecha
    LEFT JOIN last_value_ticker s ON t.ticker = s.ticker;
    """

    logging.info("Ejecutando consulta SQL en Redshift.")
    cur.execute(query)
    conn.commit()

    # Cerrar cursor y conexión
    cur.close()
    conn.close()

    logging.info("Consulta ejecutada y conexión cerrada exitosamente.")
