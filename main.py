from binance.spot import Spot as Client

from config import SECRET_KEY as secret
from config import API_KEY as key
from config import BASE_URL as base
import aux.gr as _

from rich.console import Console
from rich.traceback import install
install()

import pandas as pd




if __name__ == "__main__":
    client = Client(key, secret, base_url=base)
    account_info = client.account(recvWindow=6000)
    df_balances = pd.DataFrame(account_info['balances']).astype({'free':'float', 'locked':'float'})
    #df_balances['free'] = pd.to_numeric(df_balances['free'],errors='coerce').fillna(0)
    #df_balances['locked'] = pd.to_numeric(df_balances['free'],errors='coerce').fillna(0)
    c = Console()
    c.print(account_info.keys())
    c.print(df_balances.info())
    c.print(df_balances[df_balances['free']>0])
    c.print(client.klines("XRPBNB", interval="1m", limit=1))
    p = {'symbol':"XRPBUSD", 'interval':"1m", 'limit':2}
    c.print(_._get_klines(client.klines,p))
    
    c.print(pd.to_datetime(1649461080000, unit='ms'))
    i = pd.date_range("2022-04-08 18:45:00", periods=1, freq="T")
    c.print(type((i - pd.Timestamp("1970-01-01 00:00:00")) // pd.Timedelta("1ms")))
    del df_balances