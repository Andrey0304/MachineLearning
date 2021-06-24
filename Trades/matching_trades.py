from preprocessing import signum
import pandas as pd
import numpy as np
import json
import warnings

warnings.filterwarnings('ignore')


def matching_trades(data, multiplier, base_currency):
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
                 'Multiplier',
                 'Type']
    )
    for i in data.index:
        instrument = data.Symbol[i]
        quantity = data.Quantity[i]
        price = data['T. Price'][i]
        if instrument not in d:
            category = data['Asset Category'][i]
            d[instrument] = {'Instrument': instrument,
                             'Currency': data['Currency'][i],
                             'Result': None,
                             'Quantity': None,
                             'EntryDt': data['Date/Time'][i],
                             'Entry': price,
                             'Closure Dt': None,
                             'Closure': None,
                             'Result in BC': None,
                             'Multiplier': multiplier[category][
                                 multiplier[category][
                                     'Symbol'] == instrument].Multiplier.item() if category in multiplier.keys() else 1,
                             'Type': category}

            sign = signum(data.Quantity[i])
            count = quantity
        elif signum(quantity) * count < 0:
            d[instrument]['Closure Dt'] = data['Date/Time'][i]
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

    return predict
