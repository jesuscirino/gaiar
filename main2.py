import pandas as pd
import mplfinance as mpf
from binance.spot import Spot as Client

from datetime import datetime
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
    df_info = pd.DataFrame(_info).astype({'updateTime':'datetime64[ms]'})
    df_info = df_info.set_index("updateTime")
    df_info = df_info.tz_localize("UTC").tz_convert("America/Mexico_City")

    return {'balances': df_balances[df_balances['free']>0], \
             'info': df_info}

def save_csv(file_name: str, symbol:str, interval: str, start: tuple) -> pd.DataFrame:

    p = {'symbol':symbol,'interval':interval,'start':start , 'end': None}
    df = _._get_klines(client.klines,p)
    df.to_csv(file_name)
    return df
def plot_candle(df: pd.DataFrame, df_forecast: pd.DataFrame, df_forecastL: pd.DataFrame, df_forecastH: pd.DataFrame):
    df= df.set_index("Timestamp")
    df_forecast= df_forecast.set_index("ds")
    yhat = [mpf.make_addplot(df_forecast['yhat']),\
        mpf.make_addplot(df_forecast['yhat_lower']),\
        mpf.make_addplot(df_forecast['yhat_upper'])]
    kwargs = dict(type='candle',volume=False,figsize=(10,6),figscale=0.95)
    #kwargs = dict(type='candle',mav=(14,56),volume=True,figratio=(4,3),figscale=0.95)
    # Create my own `marketcolors` to use with the `nightclouds` style:
    mc = mpf.make_marketcolors(up='lime',down='r',inherit=True)

    # Create a new style based on `nightclouds` but with my own `marketcolors`:
    s  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=mc)
    #df= df.tz_localize("UTC").tz_convert("America/Mexico_City")
    mpf.plot(df, **kwargs, style=s, addplot=yhat)

if __name__ == "__main__":
    c = Console()
    client = Client(key, secret, base_url=base)
    c.print(account_info(client))
    #df = save_csv('BTCUSDT-1h.csv', 'BTCUSDT', '1h', (2017,8,14,0,0))
    df = pd.read_csv('BTCUSDT-1h.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df[df['Timestamp']>=datetime(2021,1,2,0,0)]
    df = df[df['Timestamp']<datetime(2022,4,24,7,0)]
    #df = df.between_time('2022-3-17-0-0', '2022-4-11-0-0')
    for i in range(4):
        df = pd.concat([df,df[-1:]])
    c.print(df.head())
    c.print(df.tail(1))
    c.print(df.info())
    forecast = _._df_forecast(df, "Close", n_futures=4, frequency='1h')
    #f_low = _._df_forecast(df, "Low", n_futures=0, frequency='1h')
    #f_high = _._df_forecast(df, "High", n_futures=0, frequency='1h')
    c.print( forecast.info())
    #c.print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head(1))
    #c.print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(1))

    #plot_candle(df, forecast, f_low, f_high )
    plot_candle(df, forecast, forecast, forecast )



    #c.print(pd.to_datetime(1649461080000, unit='ms'))
    #i = pd.date_range("2022-04-08 18:45:00", periods=1, freq="T")
    #c.print(type((i - pd.Timestamp("1970-01-01 00:00:00")) // pd.Timedelta("1ms")))
