## Repo Structure 

- `notebooks` - a folder with jupyter notebooks
- `data` - a folder which contains code responsible for gathering raw data from data sources
- `matching_trades.py` - a file which contains scripts for data, all the 'scripts' must be run from the project directory


## Data 

TODO: 

Please describe technical steps for data gathering.
Write samples for running scripts.
For example: 

```shell script
python3 matching_trades.py --data-path make-dataset-path --saving-path make-saving-path --currency-active True(if dataset contain currency else False)  --bonds-active True(if dataset contain bonds else False)
```

## Result 

The result will be saved in `--saving-path` (default `FXtrades/outputs/`) as `bond_trading.csv` (if `--bonds-active`=`True`) and `trading_currencies.csv` (if `--currency-active`=`True`)
