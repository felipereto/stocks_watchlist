import requests
import pandas as pd

def obtener_datos_dolar(period_date):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    url = f'https://mercados.ambito.com//dolarrava/cl/grafico/{period_date}/{period_date}'

    response = requests.get(url, headers=headers)

    data = response.json()

    df = pd.DataFrame(data[1:], columns=['fecha', 'dolar_ccl'])
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

    return df
