from asyncio import as_completed
import pandas as pd
import utils

class Instrument():
    def __init__(self, ob):
        self.name = ob['name']
        self.ins_type = ob['type']
        self.displayName = ob['displayName']
        self.pipLocation = pow(10, ob['pipLocation'])
        self.marginRate = ob['marginRate']
    
    # def ___repr__(self):
    #     return str(vars[self])
    
    @classmethod
    def get_instruments_df(cls):
        return pd.read_pickle(utils.get_instruments_data_filename())
    
    @classmethod
    def get_instruments_list(cls):
        df = cls.get_instruments_df()
        return [Instrument(x) for x in df.to_dict(orient='records')]
        
    

if __name__ == '__main__':
    df = Instrument.get_instruments_df()
    ll = Instrument.get_instruments_list()
    
    print(ll)