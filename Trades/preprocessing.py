import pandas as pd
import numpy as np
import json
import warnings

warnings.filterwarnings('ignore')


# with open('/home/andrey/Desktop/Features.json', 'w') as f:
#     json.dump(features, f)
def data_separation(data):
    all_data = {}
    for names in ['Trades',
                  'Interest',
                  'Dividends',
                  'Financial Instrument Information']:
        if names in data.Statement.values:
            d = data[data.Statement == names].reset_index(drop=True)
            d.columns = d.iloc[0]
            d = d[d.columns.dropna()]
            all_data[names] = d
    return all_data


def multiplier_comparison(df):
    index = df[df.Header == 'Header'].index.append(pd.Index([df.shape[0]]))

    j = index[0]
    multiplier = {}
    for i in index[1:]:
        d = df.loc[j:i - 1].reset_index(drop=True)
        d.columns = d.iloc[0]
        d.drop(index=0, inplace=True)
        d = d.reset_index(drop=True)
        d['Multiplier'] = d['Multiplier'].apply(
            lambda x: x.replace(',', '')).astype(float)
        if d['Asset Category'][0] in ['Stocks', 'Futures', 'Bonds']:
            multiplier[d['Asset Category'][0]] = d[['Symbol', 'Multiplier']]
        else:
            multiplier[d['Asset Category'][0]] = d[
                ['Description', 'Multiplier']].rename(
                columns={'Description': 'Symbol'})
        j = i
    return multiplier


def signum(num):
    return -1 if num < 0 else 1


def preprocessing_of_trades(data):
    data = data[data['DataDiscriminator'] == 'Order']
    if 'Bonds' in data['Asset Category'].values:
        data.Symbol[data['Asset Category'] == 'Bonds'] = data.Symbol[
            data['Asset Category'] == 'Bonds'].apply(
            lambda x: ' '.join(x.split(' ')[:-1]))
    data['Quantity'] = data['Quantity'].apply(
        lambda x: x.replace(',', '') if x is not np.nan else x).astype(float)
    data[['Proceeds', 'T. Price']] = data[['Proceeds', 'T. Price']].astype(
        float)
    #     data['Date/Time'] = data['Date/Time'].astype('datetime64[ns]')
    #     data = data.sort_values(['Symbol', 'Date/Time'])
    return data
