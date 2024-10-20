from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from stocks_to_redshift import stocks_to_redshift
from ccl_to_redshift import ccl_to_redshift
from stocks_holding import execute_query

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': True
}

with DAG(
    'dag_cargar_cotizaciones',
    default_args=default_args,
    description='DAG para cargar cotizaciones y CCL en Redshift',
    schedule_interval="@daily"
) as dag:

    obtener_cotizaciones_task = PythonOperator(
        task_id='obtener_y_preparar_cotizaciones',
        python_callable=stocks_to_redshift,
        provide_context=True
    )

    obtener_ccl_task = PythonOperator(
        task_id='ccl_to_redshift',
        python_callable=ccl_to_redshift,
        provide_context=True
    )

    tabla_rendimiento_actual = PythonOperator(
        task_id='rendimiento_actual',
        python_callable=execute_query,
        provide_context=True
    )

    [obtener_cotizaciones_task, obtener_ccl_task] >> tabla_rendimiento_actual
