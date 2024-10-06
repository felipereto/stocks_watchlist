from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from stocks_to_redshift import stocks_to_redshift
from airflow.hooks.base import BaseHook
import yfinance as yf
from datetime import date
import json


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
    description='DAG para cargar cotizaciones en Redshift',
    schedule_interval="@daily"
) as dag:

    obtener_cotizaciones_task = PythonOperator(
        task_id='obtener_y_preparar_cotizaciones',
        python_callable=stocks_to_redshift,
        provide_context=True
    )

    obtener_cotizaciones_task