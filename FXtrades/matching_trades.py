import pandas as pd
import numpy as np
from argparse import ArgumentParser
import warnings

warnings.filterwarnings('ignore')


def parse_args(*argument_array):
    parser = ArgumentParser()
    parser.add_argument('--data-path', required=True,
                        help='The path to the data')
    parser.add_argument('--saving-path', required=True,
                        help='The path to save the predict')
    parser.add_argument('--bonds-active', required=True,
                        help='Activation key - True if dataset contain currency else False')
    parser.add_argument('--currency-active', required=True,
                        help='Activation key - True if dataset contain bonds else False')
    return parser.parse_args(*argument_array)


def preprocessing(data: pd.DataFrame, currency: bool, bonds: bool):
    data = data[data.Header == 'Data']
    data['Quantity'] = data['Quantity'].apply(
        lambda x: x.replace(',', '') if x is not np.nan else x).astype(float)
    data['Proceeds'] = data['Proceeds'].apply(
        lambda x: x.replace(',', '') if x is not np.nan else x).astype(float)
    data['Date/Time'] = data['Date/Time'].astype('datetime64[ns]')
    data = data.sort_values(['Symbol', 'Date/Time'])
    print('Data successfully processed')

    if currency and bonds:
        forex = data[data['Asset Category'] == 'Forex']
        bonds = data[data['Asset Category'] == 'Bonds']

        bonds.Symbol = bonds.Symbol.apply(
            lambda x: ' '.join(x.split(' ')[:-1]))
        data_bonds = bonds[bonds.Symbol.duplicated(keep=False)].reset_index(
            drop=True)
        data_currency = forex[forex.Symbol.duplicated(keep=False)].reset_index(
            drop=True)
        print('The data is successfully divide')
        return data_currency, data_bonds

    elif currency:
        data_currency = data[data.Symbol.duplicated(keep=False)].reset_index(
            drop=True)
        return data_currency

    data.Symbol = data.Symbol.apply(lambda x: ' '.join(x.split(' ')[:-1]))
    data_bonds = data[data.Symbol.duplicated(keep=False)].reset_index(
        drop=True)
    return data_bonds


def matching_trades(data: pd.DataFrame, path: str):
    """
        Compares the opening and closing of trades,
         calculates the profit and saves.

       Parameters
       ----------
       data : pd.DataFrame
       path : str
            The path to save the result.

       Returns
       -------
        bond_trading.csv if bonds=True
        trading_currencies.csv if currency=True
    """

    d = {}
    count = 0
    predict = pd.DataFrame(
        columns=['Symbol', 'opening_trades', 'close_trades', 'quantity',
                 'proceeds'])
    for i in data.index:
        symbol = data.Symbol[i]
        if symbol not in d:
            d[symbol] = {'symbol': symbol,
                         'time_start': data['Date/Time'][i],
                         'time_end': None,
                         'quantity': np.abs(data.Quantity[i]) / 2,
                         'proceeds': data.Proceeds[i]}
            count = data.Quantity[i]
        else:
            d[symbol]['time_end'] = data['Date/Time'][i]
            d[symbol]['quantity'] += np.abs(data.Quantity[i] / 2)
            d[symbol]['proceeds'] += data.Proceeds[i]
            count += data.Quantity[i]

            if count == 0:
                predict = predict.append(
                    pd.Series(d[symbol].values(), index=predict.columns),
                    ignore_index=True)
                del d[symbol]
    predict.to_csv(path, index=False)
    print('\n')
    print("Result is successfully saved")
    return predict


def main():
    args = parse_args()
    currency = args.currency_active
    bonds = args.bonds_active
    path = args.saving_path

    df = pd.read_csv(args.data_path)
    if currency and bonds:
        data_currency, data_bonds = preprocessing(df, currency, bonds)
        print(matching_trades(data_bonds, path + 'bond_trading.csv'))
        print(matching_trades(data_currency, path + 'trading_currencies.csv'))

    elif currency:
        data_currency = preprocessing(df, currency, bonds)
        print(matching_trades(data_currency, path + 'trading_currency.csv'))
    else:
        data_bonds = preprocessing(df, currency, bonds)
        print(matching_trades(data_bonds, path + 'bond_trading.csv'))


if __name__ == '__main__':
    main()
