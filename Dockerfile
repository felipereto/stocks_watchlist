# Dockerfile para Airflow con Python 3.10
FROM apache/airflow:2.10.1-python3.10

# Instalar dependencias del sistema como usuario root
USER root
RUN apt-get update && apt-get install -y postgresql-client libpq-dev gcc

# Cambiar al usuario airflow
USER airflow

# Copiar archivos y carpetas necesarias al contenedor
COPY requirements.txt .
COPY dags /opt/airflow/dags
COPY functions /opt/airflow/functions
COPY config /opt/airflow/config

# Configurar el PYTHONPATH para incluir /opt/airflow y /opt/airflow/functions
ENV PYTHONPATH="/opt/airflow:/opt/airflow/functions:${PYTHONPATH}"

# Instalar las dependencias de Python
RUN pip install -r requirements.txt
