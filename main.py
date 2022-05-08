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
c = Console()
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
    
    yhat = [mpf.make_addplot(df_forecast['yhat'], color='gray', width=3 ),\
        mpf.make_addplot(df_forecast['yhat_lower'], color='r', width=5 ),\
        mpf.make_addplot(df_forecast['trend_lower'], color='white', width=2 ),\
        mpf.make_addplot(df_forecast['trend_upper'], color='white', width=2 ),\
        mpf.make_addplot(df_forecast['yhat_upper'], color='g', width=5 )]
    kwargs = dict(type='candle',volume=False,figsize=(10,6),figscale=0.95)
    #kwargs = dict(type='candle',mav=(14,56),volume=True,figratio=(4,3),figscale=0.95)
    # Create my own `marketcolors` to use with the `nightclouds` style:
    mc = mpf.make_marketcolors(up='lime',down='r',inherit=True)

    # Create a new style based on `nightclouds` but with my own `marketcolors`:
    s  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=mc)
    #df= df.tz_localize("UTC").tz_convert("America/Mexico_City")
    mpf.plot(df, **kwargs, style=s, addplot=yhat)

def show_info_dataframe (df: pd.DataFrame, head:int, tail:int, is_forecast=False):
    if is_forecast:
        df = df[["ds","trend", "yhat_lower", "yhat_upper", "trend_lower", "trend_upper", "yhat"]]
    c.print(df.head(head))
    c.print(df.tail(tail))
    c.print(df.info())

def run_predict(symbol:str, temporality:str, futures:int, start:list, end:list, yhat_LH=False):
    client = Client(key, secret, base_url=base)
    c.print(account_info(client))
    #df = save_csv(f"{symbol}-{temporality}.csv", symbol, temporality, start )
    df = pd.read_csv(f"{symbol}-{temporality}.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df[df['Timestamp']>=datetime(*start)]
    df = df[df['Timestamp']<datetime(*end)]
    show_info_dataframe(df, 2, futures)
    for i in range(futures):
        df = pd.concat([df,df[-1:]])
    _._mark("data frame inicial")
    forecast = _._df_forecast(df, "Close", n_futures=futures, frequency=temporality.capitalize())
    show_info_dataframe(forecast, 2, futures, True)
    if yhat_LH:
        f_low = _._df_forecast(df, "Low", n_futures=0, frequency='1h')
        f_high = _._df_forecast(df, "High", n_futures=0, frequency='1h')
        plot_candle(df, forecast, f_low, f_high )
        return

    plot_candle(df, forecast, forecast, forecast )


if __name__ == "__main__":
    symbol = "BTCUSDT"
    temporality = "1d"
    start , end, futures, yhat_LH = [2022, 1, 23, 0, 0 ], [2022, 5, 6, 0, 0], 155, False

    run_predict(symbol, temporality, futures, start, end)