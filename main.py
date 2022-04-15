from binance.spot import Spot as Client

from config import SECRET_KEY as secret
from config import API_KEY as key
from config import BASE_URL as base
import aux.gr as _

from rich.console import Console
from rich.traceback import install
install()
def account_info(client: Client) -> dict:
    _info = client.account(recvWindow=6000)
    df_balances = pd.DataFrame(_info.pop('balances')).astype({'free':'float', 'locked':'float'})
    #c.print(pd.DataFrame(account_info).astype({'updateTime':'datetime64[ms]'}))
    #df_info = pd.to_datetime(arg)
    df_info = pd.DataFrame(_info).astype({'updateTime':'datetime64[ms]'})
    df_info = df_info.set_index("updateTime")
    df_info = df_info.tz_localize("UTC")

    return {'balances': df_balances[df_balances['free']>0], \
             'info': df_info}

import pandas as pd

if __name__ == "__main__":
    c = Console()
    client = Client(key, secret, base_url=base)
    
    #df_balances['free'] = pd.to_numeric(df_balances['free'],errors='coerce').fillna(0)
    #df_balances['locked'] = pd.to_numeric(df_balances['free'],errors='coerce').fillna(0)
    c.print(account_info(client))
    #xrp = client.klines("XRPBNB", interval="1m", limit=1)
    p = {'symbol':"BNBBUSD", 'interval':"1m", 'limit':1}
    xrp = _._get_klines(client.klines,p)
    df_xrp = pd.DataFrame(xrp, columns=['a','b','c','d','e','f','h','i','j','k','l','m']).astype({'a':'datetime64[ms]'})
    df_xrp = df_xrp.set_index("a")
    df_xrp = df_xrp.tz_localize("UTC").tz_convert("America/Mexico_City")
    c.print(df_xrp)
    
    #c.print(pd.to_datetime(1649461080000, unit='ms'))
    #i = pd.date_range("2022-04-08 18:45:00", periods=1, freq="T")
    #c.print(type((i - pd.Timestamp("1970-01-01 00:00:00")) // pd.Timedelta("1ms")))