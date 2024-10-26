# Stocks Watchlist

Este proyecto permite realizar un seguimiento de las cotizaciones de acciones y calcular la ganancia generada por las inversiones. Utiliza la API de Yahoo Finance y la API de Cotización de CCL, almacenando la información en una base de datos Redshift para su posterior análisis y seguimiento de rendimiento.

## Propósito

Stocks Watchlist está diseñado para inversores que desean un seguimiento automatizado y detallado de sus portafolios, con cálculos de rentabilidad actualizados y análisis de rendimiento diario. La integración con Yahoo Finance y la API de Cotización de CCL permite un análisis constante en tiempo real para una toma de decisiones informada.

## Características

- **Integración con la API de Yahoo Finance** para obtener cotizaciones diarias de acciones.
- **Integración con la API de Cotización de CCL** para obtener el tipo de cambio.
- **Almacenamiento en Redshift** para gestionar y analizar los datos históricos de precios y transacciones.
- **Cálculo de ganancias y seguimiento de inversiones**.
- **Automatización mediante DAGs de Airflow** para ejecutar las tareas de ingesta y almacenamiento de datos diariamente.

## Tabla de Contenidos

- [Propósito](#propósito)
- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [DAG y Funciones](#dag-y-funciones)
  - [Descripción del DAG de Airflow](#descripción-del-dag-de-airflow)
  - [Descripción de Funciones](#descripción-de-funciones)
- [Uso](#uso)
- [Estructura de la Base de Datos](#estructura-de-la-base-de-datos)
  - [Relaciones y Flujo de Datos](#relaciones-y-flujo-de-datos)
- [Tests](#tests)
- [Continuous Integration](#continuous-integration)


## Requisitos Previos

1. **Docker** instalado en tu máquina.
2. **Credenciales de Redshift** configuradas en Airflow bajo el nombre de `redshift_conn`. Deberás configurar la conexión en la interfaz de Airflow una vez que el contenedor esté en funcionamiento. Ver los pasos en [Instalación](#instalación).
3. **Python 3.8 o superior** instalado en tu máquina.


## Instalación

Para ejecutar el proyecto, sigue estos pasos:

1. **Clona el repositorio**:

    ```bash
    git clone https://github.com/felipereto/stocks_watchlist.git
    cd stocks_watchlist
    ```

2. **Configura y ejecuta los contenedores de Docker**:

    Ejecuta los siguientes comandos para iniciar Airflow y los servicios necesarios:

    ```bash
    docker compose up airflow-init
    docker compose up
    ```

3. **Configura las credenciales de Redshift en Airflow**:

    - Accede a la interfaz web de Airflow en [http://localhost:8080](http://localhost:8080).
    - Usuario y clave por defecto para Airflow: `airflow / airflow`.
    - Ve a la sección **Admin > Connections** en la interfaz de Airflow.
    - Crea una nueva conexión:
      - **Connection Id**: `redshift_conn`
      - **Connection Type**: `Amazon Redshift`
      - **Host**: `redshift-pda-cluster.cnuimntownzt.us-east-2.redshift.amazonaws.com`
      - **Database**: `pda`
      - **User** y **Password**: según credenciales de Redshift enviadas por privado.
      - **Port**: `5439`.

## DAG y Funciones

El proyecto utiliza un **DAG de Airflow** que automatiza la recolección y carga de datos de cotizaciones de acciones y el tipo de cambio CCL en Redshift, además de calcular el rendimiento de las inversiones. A continuación, se describe la estructura del DAG y las funciones principales involucradas.

### Descripción del DAG de Airflow

El DAG `dag_cargar_cotizaciones` está configurado para ejecutarse diariamente y consta de tres tareas principales:

1. **Obtener y cargar cotizaciones de acciones**: Utiliza la función `stocks_to_redshift` para obtener datos de cotización de varios tickers y cargarlos en Redshift.
2. **Obtener y cargar el tipo de cambio CCL**: Utiliza la función `ccl_to_redshift` para obtener el valor del tipo de cambio CCL del día y cargarlo en Redshift.
3. **Calcular el rendimiento de las inversiones**: Utiliza la función `execute_query` para calcular el rendimiento actual de las inversiones con base en las transacciones y cotizaciones almacenadas en Redshift.

**Objetivo del DAG**: El DAG está diseñado para que los datos procesados y almacenados en Redshift puedan ser utilizados para evaluar el rendimiento de las acciones compradas. El resultado final se almacena en la tabla `stocks_holding`, que muestra el rendimiento de cada acción en términos de rentabilidad. Esta tabla facilita el análisis de las ganancias y pérdidas, usando también el historial de precios y el tipo de cambio, mientras el resto de las tablas (`stocks_transactions`, `stocks_prices_daily`, `dolar_ccl`, `param_ticker`) sirven como soporte para mantener el registro histórico y sectorial de las transacciones y cotizaciones.

### Descripción de Funciones

Las funciones principales están organizadas en tres módulos para mejorar la estructura y facilitar el mantenimiento del código:

1. **`main_tasks.py`**:
   - **stocks_to_redshift**: Obtiene datos de cotización diarios para una lista de tickers de acciones desde Yahoo Finance y los carga en la tabla `stocks_prices_daily` en Redshift mediante la función `load_data_to_redshift`.
   - **ccl_to_redshift**: Obtiene el valor del tipo de cambio CCL para la fecha de ejecución y lo carga en la tabla `dolar_ccl` en Redshift mediante la función `load_data_to_redshift`.
   - **execute_query**: Ejecuta una consulta en Redshift para calcular el rendimiento actual de las inversiones. Esta función inserta los resultados en la tabla `stocks_holding`.

2. **`data_extraction.py`**:
   - **obtener_datos_dolar**: Recupera los datos de tipo de cambio CCL desde una API externa y los transforma en un DataFrame.
   - **get_daily_stock_data**: Obtiene datos de cotización diaria de acciones desde Yahoo Finance para un rango de fechas y una lista de tickers.

3. **`redshift_operations.py`**:
   - **load_data_to_redshift**: Carga un DataFrame en una tabla de Redshift, utilizando una conexión segura mediante BaseHook en Airflow.
   - **redshift_connection**: Decorador que gestiona la conexión a Redshift, garantizando que la conexión se cierre adecuadamente. 


## Uso

Con los contenedores de Docker en funcionamiento, puedes iniciar el DAG de Airflow para obtener y almacenar los datos de cotizaciones y CCL en Redshift. 

- **DAG principal**: `dag_cargar_cotizaciones`
  - Configurado para ejecutarse diariamente y obtener los precios de acciones y el tipo de cambio CCL, almacenando la información en las tablas correspondientes.
  - Proceso:
    1. Llama a las APIs de Yahoo Finance y Cotización de CCL.
    2. Realiza transformaciones de datos para compatibilidad con Redshift.
    3. Inserta los datos en las tablas de Redshift.

## Estructura de la Base de Datos

Las tablas en Redshift se estructuran para facilitar el seguimiento y análisis de las inversiones, brindando una visión completa de las transacciones, precios históricos y rendimiento del portafolio. A continuación se detallan las tablas principales, su propósito y relaciones:

- **`dolar_ccl`**: Almacena el valor diario del tipo de cambio CCL (Contado con Liquidación), que se utiliza para calcular valores en USD y evaluar rendimientos.
  - **Columnas**: 
    - `date`: Fecha de la cotización.
    - `ccl_value`: Valor del tipo de cambio CCL para esa fecha.

- **`stocks_transactions`**: Contiene el historial detallado de transacciones de compra y venta de acciones, permitiendo el seguimiento de los movimientos de portafolio y los costos asociados.
  - **Columnas**: 
    - `ticker`: Símbolo bursátil de la acción.
    - `type`: Tipo de transacción (compra o venta).
    - `date`: Fecha de la transacción.
    - `nominal_quantity`: Cantidad nominal de acciones transaccionadas.
    - `face_value`: Valor nominal de la transacción.
    - `gross_cost`: Costo bruto de la transacción en la moneda local.

- **`stocks_prices_daily`**: Guarda el precio diario de cada acción, proporcionando una base para calcular el valor actual del portafolio y sus variaciones.
  - **Columnas**: 
    - `date`: Fecha de la cotización.
    - `ticker`: Símbolo bursátil de la acción.
    - `Adj_Close`: Precio de cierre ajustado, incluyendo dividendos.
    - `Close`, `High`, `Low`, `Open`: Precios de cierre, máximo, mínimo y apertura del día.
    - `Volume`: Volumen de transacciones.

- **`param_ticker`**: Tabla de referencia con información adicional sobre cada acción, incluyendo el sector al que pertenece, lo que facilita el análisis por industria y diversificación del portafolio.
  - **Columnas**: 
    - `id_ticker`: Identificador único del ticker.
    - `description`: Descripción o nombre de la empresa.
    - `industry`: Industria a la que pertenece.

- **`stocks_holding`**: Calcula el rendimiento y valor actual de las inversiones, usando el historial de precios y transacciones para mostrar el desempeño del portafolio.
  - **Columnas**: 
    - `ticker`: Símbolo bursátil de la acción.
    - `date`: Fecha de cálculo.
    - `gross_cost`: Costo bruto de las acciones adquiridas en moneda local.
    - `gross_cost_usd`: Costo bruto convertido a USD utilizando el tipo de cambio CCL.
    - `last_price_usd`: Último precio de la acción en USD.
    - `current_holding`: Valor actual de la tenencia.
    - `profit`: Ganancia o pérdida en USD.
    - `var_perc`: Porcentaje de variación entre el costo y el valor actual.

### Relaciones y Flujo de Datos

- **Relación de Precios y Transacciones**: `stocks_transactions` se une a `stocks_prices_daily` mediante el campo `ticker` para obtener el valor de la acción en el momento de cada transacción.
- **Conversión a USD**: `dolar_ccl` se usa en cálculos de `stocks_holding` para convertir los costos a USD y calcular las ganancias en dólares.
- **Análisis Sectorial**: `param_ticker` permite clasificar y agrupar las inversiones por industria, lo cual es útil para analizar la diversificación y exposición sectorial del portafolio.

Este diseño permite realizar un análisis integral del portafolio, incluyendo el rendimiento diario, análisis sectorial y el seguimiento del impacto de las fluctuaciones del tipo de cambio en el valor de las inversiones.


## Tests

Para ejecutar las pruebas con `poetry`, sigue estos pasos:

1. Ir a la carpeta de `tests`:

    ```bash
    cd tests
    ```

2. Instalar las dependencias necesarias para pruebas:

    ```bash
    poetry install
    ```

3. Ejecutar las pruebas:

    ```bash
    poetry run pytest
    ```

Los tests validan las siguientes funciones clave del proyecto:

- **Conexión a las APIs** de Yahoo Finance y Cotización de CCL.
- **Transformación de datos** antes de la ingesta en Redshift.
- **Inserción de datos** en las tablas de Redshift.

## Continuous Integration

Este proyecto utiliza **GitHub Actions** para la integración continua. El archivo `.yaml` incluye:

- **Linting** con Flake8 para garantizar la calidad del código.
- **Ejecutar tests** con pytest para asegurar que el código esté libre de errores.
