import psycopg2
import psycopg2.extras
from wrapper_redshift import redshift_connection


@redshift_connection
def load_data_to_redshift(conn, df, tabla):
    try:
        cur = conn.cursor()

        cols = ",".join([f'"{col}"' for col in df.columns])
        query = f"INSERT INTO {tabla} ({cols}) VALUES %s"
        data = [tuple(row) for row in df.to_numpy()]

        psycopg2.extras.execute_values(cur, query, data)

        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error al cargar los datos en Redshift: {e}")
        raise
