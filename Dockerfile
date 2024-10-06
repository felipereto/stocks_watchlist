FROM apache/airflow:2.10.1

COPY requirements.txt .

USER root
RUN apt-get update && apt-get install -y postgresql-client libpq-dev

USER airflow
RUN pip install  -r requirements.txt
