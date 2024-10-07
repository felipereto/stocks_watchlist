import psycopg2
import psycopg2.extras
from airflow.hooks.base import BaseHook


def load_data_to_redshift(df, tabla):
    try: 
        redshift_conn = BaseHook.get_connection('redshift_conn')
        print(redshift_conn)
        conn = psycopg2.connect(
            dbname=redshift_conn.schema,
            user=redshift_conn.login,
            password=redshift_conn.password,
            host=redshift_conn.host,
            port=redshift_conn.port
        )

        cur = conn.cursor()

        cols = ",".join([f'"{col}"' for col in df.columns])
        query = f"INSERT INTO {tabla} ({cols}) VALUES %s"
        data = [tuple(row) for row in df.to_numpy()]

        psycopg2.extras.execute_values(cur, query, data)

        conn.commit()
        cur.close()
    except Exception as e:
        f"Error al cargar los datos en Redshift: {e}"
        raise