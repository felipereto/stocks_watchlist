Stocks Watchlist

Este proyecto permite realizar un seguimiento de las cotizaciones de acciones y calcular la ganancia generada por las inversiones. Utiliza la API de Yahoo Finance y la API de Cotización de CCL, almacenando la información en una base de datos Redshift.


Características:

- Integración con la API de Yahoo Finance para obtener cotizaciones diarias de acciones.
- Integración con la API de Cotización de CCL.
- Almacenamiento de datos en Redshift para su posterior análisis.
- Seguimiento de las inversiones y cálculo de ganancias.
- Automatización de las tareas mediante DAGs de Airflow.


Requisitos previos:

1. Docker instalado en tu máquina.
2. Credenciales de Redshift configuradas en Airflow bajo el nombre de `redshift_conn` (se proporcionarán de forma privada).
3. Un entorno compatible con Python 3.8 o superior.


Instalación:

Para ejecutar el proyecto, sigue estos pasos:

1. Clona el repositorio:

    git clone https://github.com/felipereto/stocks_watchlist.git

2. Abre Docker y ejecuta la imagen con el siguiente Dockerfile:

	hacer docker compose up airflow-init y después docker compose up

3. Configura las credenciales de Redshift en Airflow:

- Accede a la interfaz de Airflow.
- Ve a "Connections" y crea una nueva conexión llamada redshift_conn.
- Agrega las credenciales de Redshift proporcionadas.


Uso:

Una vez que la imagen de Docker está corriendo, se pueden iniciar los DAGs de Airflow para obtener y almacenar los datos de cotizaciones y CCL en Redshift. Los DAGs disponibles son:

- DAG para cargar cotizaciones: dag_cargar_cotizaciones
- DAG para cargar CCL: dag_ccl

Ambos DAGs están configurados para ejecutarse diariamente.


Estructura de la Base de Datos:

- Tabla de cotización de CCL:
- Tabla de transacciones de acciones:
- Tabla de precios de acciones diarios:
- Tabla de tickers paramétrica:


Tests:

Para ejecutar las pruebas:
- Configura un entorno virtual con pyenv y asegúrate de instalar las dependencias del archivo requirements.txt:
    pyenv virtualenv 3.10.0 airflow_env
    pyenv activate airflow_env
    pip install -r requirements.txt
- Desde la carpeta Testing, ejecuta pytest:
    cd Testing
    pytest
Los tests están diseñadas para validar las siguientes funciones principales:
    - Las llamadas a las APIs de Yahoo Finance y Cotización de CCL.
    - Las transformaciones previas a la ingesta de datos en Redshift.


Continuous Integration:

Este proyecto utiliza GitHub Actions para continuous integration. Los archivos .yaml incluyen:
    Linting con Flake8
    Tests con pytest
