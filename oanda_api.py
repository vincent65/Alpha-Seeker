from sqlite3 import DateFromTicks
import requests
import pandas as pd
import defs
import utils
from dateutil.parser import *


class OandaAPI():
    
    def __init__(self):
        self.session = requests.Session()
        
    def fetch_instruments(self):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments"
        response = self.session.get(url, headers=defs.SECURE_HEADER)
        return response.status_code, response.json()
    
    def get_instruments_df(self):
        code, data = self.fetch_instruments()
        if code == 200:
            df = pd.DataFrame.from_dict(data['instruments'])
            return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]
        else:
            return None
        
    def save_instruments(self):
        instrument_df = self.get_instruments_df()
        if instrument_df is not None:
            instrument_df.to_pickle("instruments.pkl")
    
    #hist dat fetching; historical data is still limited to a max of 5000 candles
    def fetch_candles(self, pair_name, count=None, granularity="H1", date_from = None, date_to = None, as_df = False):
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"
        params = dict(
            granularity = granularity,
            price = "MBA"
        )
        
        if date_from is not None and date_to is not None:
            params['to'] = int(date_to.timestamp())
            params['from'] = int(date_from.timestamp())
        #of dates are not specified get last however many trades
        elif count is not None:
            params['count'] = count
        else:
            params['count'] = 300
            
        response = self.session.get(url, params=params, headers = defs.SECURE_HEADER)
        
        if response.status_code != 200:
            return response.status_code, None
        if as_df==True:
            json_data = response.json()['candles']
            return response.status_code, OandaAPI.candles_to_df(json_data)
        return response.status_code, response.json()
    @classmethod
    def candles_to_df(cls, json_data):
        prices = ['mid', 'bid', 'ask'] 
        ohlc = ['o', 'h', 'l', 'c']
        candle_data = []

        for candle in json_data:
            if candle['complete'] == False:
                continue
            new_dict = {}
            new_dict['time'] = candle['time']
            new_dict['volume'] = candle['volume']
            for price in prices:
                for oh in ohlc:
                    new_dict[f'{price}_{oh}'] = float(candle[price][oh])
            candle_data.append(new_dict)
        df = pd.DataFrame.from_dict(candle_data)
        df["time"] = [parse(x) for x in df.time]
        return df
    
    
if __name__ == '__main__':
    api = OandaAPI()
    # api.save_instruments()
    date_from = utils.get_utc_dt_from_string("2022-06-06 17:00:00")
    date_to = utils.get_utc_dt_from_string("2022-06-20 17:00:00")
    res, df = api.fetch_candles("EUR_USD", date_from=date_from, date_to = date_to, as_df=True)
    print(df.info())