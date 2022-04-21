import mplfinance as mpf
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
    df_info = df_info.tz_localize("UTC").tz_convert("America/Mexico_City")

    return {'balances': df_balances[df_balances['free']>0], \
             'info': df_info}

import pandas as pd

if __name__ == "__main__":
    c = Console()
    client = Client(key, secret, base_url=base)
    c.print(account_info(client))
    p = {'symbol':"BNBBUSD", 'interval':"1m", 'limit':None, 'start': (2022,4,13,6,00),'end': None}
    df = _._get_klines(client.klines,p)
    c.print(df.tail())
    forecast = _._df_forecast(df, frecuency='1T', n_futures=500)
    c.print( forecast.info())
    c.print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())
    c.print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(8))


    kwargs = dict(type='candle',mav=(14,56),volume=True,figratio=(4,3),figscale=0.95)
    # Create my own `marketcolors` to use with the `nightclouds` style:
    mc = mpf.make_marketcolors(up='lime',down='r',inherit=True)

    # Create a new style based on `nightclouds` but with my own `marketcolors`:
    s  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=mc)

    df= df.set_index("Timestamp")
    #df= df.tz_localize("UTC").tz_convert("America/Mexico_City")
    mpf.plot(df, **kwargs, style=s)


    
     
    #c.print(pd.to_datetime(1649461080000, unit='ms'))
    #i = pd.date_range("2022-04-08 18:45:00", periods=1, freq="T")
    #c.print(type((i - pd.Timestamp("1970-01-01 00:00:00")) // pd.Timedelta("1ms")))