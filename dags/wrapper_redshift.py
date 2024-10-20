import psycopg2
from airflow.hooks.base import BaseHook
from functools import wraps

def redshift_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            redshift_conn = BaseHook.get_connection('redshift_conn')
            conn = psycopg2.connect(
                dbname=redshift_conn.schema,
                user=redshift_conn.login,
                password=redshift_conn.password,
                host=redshift_conn.host,
                port=redshift_conn.port
            )
            result = func(conn, *args, **kwargs)
            conn.close() 
            return result
        except Exception as e:
            print(f"Error al conectar a Redshift: {e}")
            raise
    return wrapper


