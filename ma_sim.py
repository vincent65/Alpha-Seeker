from cgi import print_environ
from concurrent.futures import process
from inspect import getclosurevars
import pandas as pd
import utils
import instrument

pd.set_option("display.max_columns", None)

def is_trade(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:
        return -1
    return 0

def get_col_ma(ma):
    return f"MA_{ma}"

def evaluate_pair(i_pair, mashort, malong, price_data):
    #determine trades
    price_data['DIFF'] = price_data[get_col_ma(mashort)] - price_data[get_col_ma(malong)]
    price_data['DIFF_PREV'] = price_data.DIFF.shift(1)
    price_data['IS_TRADE'] = price_data.apply(is_trade, axis = 1)
    
    #calculate gains
    df_trades = price_data[price_data.IS_TRADE!=0].copy()
    df_trades["DELTA"] = (df_trades.mid_c.diff() / i_pair.pipLocation).shift(-1)
    df_trades["GAIN"] = df_trades["DELTA"] * df_trades["IS_TRADE"]
    
    print(f"{i_pair.name} {mashort} {malong} trades:{df_trades.shape[0]} gain:{df_trades['GAIN'].sum():.0f}")    
    
    return df_trades['GAIN'].sum()
    
def get_price_data(pair, granularity):
    df = pd.read_pickle(utils.get_hist_data_filename(pair, granularity))
    non_cols = ['time', 'volume']
    mod_cols = [x for x in df.columns if x not in non_cols]
    df[mod_cols] = df[mod_cols].apply(pd.to_numeric)
    return df[['time', 'mid_c']].copy()

def process_data(ma_short, ma_long, price_data):
    set1 = set(ma_short)
    set2 = set(ma_long)
    ma_list = list(set1.union(set2))
    #calculate the moving averages
    for ma in ma_list:
        price_data[get_col_ma(ma)] = price_data.mid_c.rolling(window=ma).mean()
    return price_data

def run():
    pairname = "GBP_JPY"
    granularity = "H1"
    ma_short = {8,16,32,64}
    ma_long = {32,64,96,128,256}
    
    i_pair = instrument.Instrument.get_instrument_by_name(pairname)
    price_data = get_price_data(pairname, granularity)
    price_data = process_data(ma_short, ma_long, price_data)
    
    best = -9999999
    best_short = 0
    best_long = 0   
    
    for long in ma_long:
        for short in ma_short:
            if short >= long:
                continue
            #evaluate performance of 
            res = evaluate_pair(i_pair, short, long, price_data.copy())
            if res >= best:
                best = res
                best_short = short
                best_long = long
    
    print(f"Best:{best:.0f} MASHORT:{best_short:.0f} MALONG:{best_long:.0f}")
    
if __name__ == "__main__":
    run()