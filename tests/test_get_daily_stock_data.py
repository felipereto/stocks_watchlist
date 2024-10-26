import pandas as pd
from functions.main_tasks import get_daily_stock_data


def test_get_daily_stock_data(mocker):
    # Defino el DataFrame esperado
    expected_data = pd.DataFrame({
        'Date': ['2024-10-03'],
        'Ticker': ['BBAR.BA'],
        'Adj_Close': [4550.0],
        'Close': [4550.0],
        'High': [4585.0],
        'Low': [4260.0],
        'Open': [4260.0],
        'Volume': [241218]
    })
    expected_data['Date'] = pd.to_datetime(expected_data['Date'])

    # Simulo los datos que devolvería yfinance
    mock_yf_download = mocker.patch('functions.stocks_prices_daily.yf.download')
    mock_yf_download.return_value = pd.DataFrame({
        'Adj Close': [4550.0],
        'Close': [4550.0],
        'High': [4585.0],
        'Low': [4260.0],
        'Open': [4260.0],
        'Volume': [241218],
        'Date': pd.to_datetime(['2024-10-03'])
    }).set_index('Date')

    result = get_daily_stock_data('2024-10-03', '2024-10-04', ["BBAR.BA"])

    pd.testing.assert_frame_equal(result, expected_data)
