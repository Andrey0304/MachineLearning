import pandas as pd
from preprocessing import data_separation, multiplier_comparison
from preprocessing import preprocessing_of_trades, preprocessing_of_dividends
from matching_trades import matching_trades

base_currency = {
    'USD': 1,
    'AUD': 0.77135,
    'GBP': 1.4112,
    'EUR': 1.21212,
    'NZD': 0.71454,
    'CAD': 0.81,
    'CHF': 1.09,
    'JPY': 0.0090,
    'HKD': 0.13
}

data = pd.read_csv('/home/andrey/PycharmProjects/Trades/data/full_statement.csv')
all_data = data_separation(data)

data_trades = preprocessing_of_trades(all_data['Trades'])
financial_instrument = all_data['Financial Instrument Information']
multiplier = multiplier_comparison(financial_instrument)

if 'Dividends' in all_data.keys():
    data_dividends = preprocessing_of_dividends(all_data['Dividends'],
                                                base_currency)
else:
    data_dividends = None

result = matching_trades(data_trades=data_trades,
                         data_dividends=data_dividends,
                         financial_instrument=financial_instrument,
                         multiplier=multiplier,
                         base_currency=base_currency)

result.to_csv('/home/andrey/PycharmProjects/Trades/data/matching_trades.csv',
              index=False)
