import psycopg2
from airflow.hooks.base import BaseHook


def execute_query():
    try:
        redshift_conn = BaseHook.get_connection('redshift_conn')

        conn = psycopg2.connect(
            dbname=redshift_conn.schema,
            user=redshift_conn.login,
            password=redshift_conn.password,
            host=redshift_conn.host,
            port=redshift_conn.port
        )

        cur = conn.cursor()

        query = """
        DROP TABLE IF EXISTS pda."2024_felipe_miguel_reto_schema".stocks_holding;

        CREATE TABLE pda."2024_felipe_miguel_reto_schema".stocks_holding AS (
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
        LEFT JOIN last_value_ticker s ON t.ticker = s.ticker
        );
        """

        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()

        print("Consulta ejecutada exitosamente.")

    except Exception as e:
        print(f"Error al conectar o ejecutar la consulta en Redshift: {e}")
        raise
