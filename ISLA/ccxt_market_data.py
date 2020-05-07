'''
Author: www.backtest-rookies.com
 
MIT License
 
Copyright (c) 2018 backtest-rookies.com
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
 
import ccxt
from datetime import datetime, timedelta, timezone
import math
import argparse
import pandas as pd
 
def get_market_data(symbol: str, exchange_: str, timeframe: str, save=False, data_path=None):
    '''
    symbol: The Symbol of the Instrument/Currency Pair To Download. You can see the list with exchange.markets.keys()
    exchange: The exchange to download from. ex: binance, kraken, bitfinex ...
    timeframe: choices=['1m', '5m','15m', '30m','1h', '2h', '3h', '4h', '6h', '12h', '1d', '1M', '1y']
    save: if you want to save the dataframe in a csv
    data_path: the path to the data
    '''
    # Get our Exchange
    try:
        exchange = getattr (ccxt, exchange_) ()
    except AttributeError:
        print('-'*36,' ERROR ','-'*35)
        print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange_))
        print('-'*80)
        quit()

    # Check if fetching of OHLC Data is supported
    if exchange.has["fetchOHLCV"] != True:
        print('-'*36,' ERROR ','-'*35)
        print('{} does not support fetching OHLC data. Please use another exchange'.format(exchange_))
        print('-'*80)
        quit()

    # Check requested timeframe is available. If not return a helpful error.
    if (not hasattr(exchange, 'timeframes')) or (timeframe not in exchange.timeframes):
        print('-'*36,' ERROR ','-'*35)
        print('The requested timeframe ({}) is not available from {}\n'.format(timeframe,exchange_))
        print('Available timeframes are:')
        for key in exchange.timeframes.keys():
            print('  - ' + key)
        print('-'*80)
        quit()

    # Check if the symbol is available on the Exchange
    exchange.load_markets()
    if symbol not in exchange.symbols:
        print('-'*36,' ERROR ','-'*35)
        print('The requested symbol ({}) is not available from {}\n'.format(symbol,exchange_))
        print('Available symbols are:')
        for key in exchange.symbols:
            print('  - ' + key)
        print('-'*80)
        quit()


    # Get data
    data = exchange.fetch_ohlcv(symbol, timeframe)
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(data, columns=header).set_index('Timestamp')
    df = df.set_index(pd.to_datetime(df.index, unit='ms'))
    # Save it
    if save and data_path:
        symbol_out = symbol.replace("/","_")
        filename = '{}-{}-{}.csv'.format(exchange_, symbol_out,timeframe)
        df.to_csv(data_path + filename)
    return df
