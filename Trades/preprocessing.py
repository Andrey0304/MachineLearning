import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')


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
    data['Date/Time'] = pd.to_datetime(data['Date/Time']).dt.date

    return data


def preprocessing_of_dividends(div, bc):
    div = div.dropna()
    div.drop(index=0, inplace=True)
    div.Description = div.Description.apply(
        lambda x: x[x.find('(') + 1:x.find(')')])
    div.reset_index(drop=True, inplace=True)
    div = div.rename(columns={'Description': 'Security ID'})
    div.Amount = div.Amount.astype(float)
    div.Amount = div.Amount.apply(
        lambda x: x * bc[div.Currency[div.Amount == x].item()])

    return div
