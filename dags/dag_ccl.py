from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from ccl_to_redshift import ccl_to_redshift

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 7),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': True
}

with DAG(
    'dag_ccl',
    default_args=default_args,
    description='DAG para cargar ccl en Redshift',
    schedule_interval="@daily"
) as dag:

    obtener_ccl_task = PythonOperator(
        task_id='ccl_to_redshift',
        python_callable=ccl_to_redshift,
        provide_context=True
    )

    obtener_ccl_task
