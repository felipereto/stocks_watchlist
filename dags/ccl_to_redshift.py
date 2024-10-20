from load_data_to_redshift import load_data_to_redshift
from dolar_ccl import obtener_datos_dolar


def ccl_to_redshift(**context):

    end_date = context['ds']

    df = obtener_datos_dolar(end_date)
    table_name = 'pda."2024_felipe_miguel_reto_schema".dolar_ccl'
    load_data_to_redshift(df, table_name)
