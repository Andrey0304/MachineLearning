from preprocessing import signum
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')


def matching_trades(data_trades,
                    data_dividends,
                    financial_instrument,
                    multiplier,
                    base_currency):
    d = {}
    count = 0
    predict = pd.DataFrame(
        columns=['Instrument',
                 'Currency',
                 'Result',
                 'Quantity',
                 'EntryDt',
                 'Entry',
                 'Closure Dt',
                 'Closure',
                 'Result in BC',
                 'Dividends',
                 'Multiplier',
                 'Type']
    )
    for i in data_trades.index:
        instrument = data_trades.Symbol[i]
        quantity = data_trades.Quantity[i]
        price = data_trades['T. Price'][i]
        sign = signum(quantity)
        if instrument not in d:
            category = data_trades['Asset Category'][i]
            d[instrument] = {'Instrument': instrument,
                             'Currency': data_trades['Currency'][i],
                             'Result': None,
                             'Quantity': None,
                             'EntryDt': data_trades['Date/Time'][i],
                             'Entry': price,
                             'Closure Dt': None,
                             'Closure': None,
                             'Result in BC': None,
                             'Dividends': None,
                             'Multiplier': 1,
                             'Type': category}

            if category in multiplier.keys():
                d[instrument]['Multiplier'] = multiplier[category][
                    multiplier[category][
                        'Symbol'] == instrument].Multiplier.item()

            count = quantity
        elif sign * count < 0:
            d[instrument]['Closure Dt'] = data_trades['Date/Time'][i]
            d[instrument]['Quantity'] = -quantity
            d[instrument]['Closure'] = price
            d[instrument]['Result'] = np.abs(quantity) * (
                    d[instrument]['Closure'] - d[instrument]['Entry']) * \
                                      d[instrument]['Multiplier']
            d[instrument]['Result in BC'] = d[instrument]['Result'] * \
                                            base_currency[
                                                d[instrument]['Currency']]
            predict = predict.append(
                pd.Series(d[instrument].values(), index=predict.columns),
                ignore_index=True)

            count += quantity
        else:
            d[instrument]['Entry'] = (count * d[instrument][
                'Entry'] + quantity * price) / (count + quantity)
            count += quantity

    predict = group_by_day(predict)

    if data_dividends is not None:
        for symbol in predict[predict.Type == 'Stocks'].Instrument:
            sec_id = \
                financial_instrument[financial_instrument.Symbol == symbol][
                    'Security ID'].item()
            if sec_id in data_dividends['Security ID'].values:
                index = data_dividends[
                    data_dividends['Security ID'] == sec_id].index
                amount = data_dividends.Amount[index].item()
                predict['Dividends'][predict.Instrument == symbol] = amount

    return predict


def group_by_day(data):
    data = data.sort_values(
        ['Type', 'Instrument', 'Closure Dt', 'Quantity']).reset_index(
        drop=True)
    j = 0
    drop_index = []
    for i in data.index[1:]:
        value_1 = data.iloc[j][['Instrument', 'Closure Dt']]
        value_2 = data.iloc[i][['Instrument', 'Closure Dt']]
        if value_2.equals(value_1) and data.Quantity[i] * data.Quantity[j] > 0:
            data['Closure'][i] = (data['Closure'][i] * data['Quantity'][i] +
                                  data['Closure'][j] * data['Quantity'][j]) / (
                                             data['Quantity'][i] +
                                             data['Quantity'][j])
            data['Quantity'][i] += data['Quantity'][j]
            data['Result'][i] += data['Result'][j]
            data['Result in BC'][i] += data['Result in BC'][j]
            drop_index.append(j)
        j = i
    data.drop(index=drop_index, inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data
