import pandas as pd
from functions.main_tasks import obtener_datos_dolar


def test_obtener_datos_dolar(mocker):
    mock_data = [
        ['fecha', 'DOLAR CCL'],
        ['14/10/2024', 1180.14]
    ]

    mock_response = mocker.patch('requests.get')
    mock_response.return_value.json.return_value = mock_data

    period_date = '2024/10/14'
    df = obtener_datos_dolar(period_date)

    df = df.reset_index(drop=True)

    expected_df = pd.DataFrame({
        'fecha': ['2024-10-14'],
        'dolar_ccl': [1180.14]
    })

    pd.testing.assert_frame_equal(df, expected_df)
