from datetime import datetime
from datetime import timedelta
import logging
import pandas as pd
from prophet import Prophet
from rich.logging import RichHandler
from rich.progress import track
from rich.traceback import install
install()
def __get_dt(intervalo: str):
    if 'm' in intervalo:
        return timedelta(minutes=int(intervalo[0]))
    if 'h' in intervalo:
        return timedelta(hours=int(intervalo[0]))
    if 'd' in intervalo:
        return timedelta(days=int(intervalo[0]))
    if 'w' in intervalo:
        return timedelta(weeks=int(intervalo[0]))
    else:
         return timedelta(-1)
def _debugit(msg: str):

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    #logging.info(msg)
    logging.debug(msg)

def _get_klines(client_klines , params: dict) -> pd.DataFrame:
    start = datetime(*params['start'])
    end   = datetime.now() if params['end'] is None else datetime(*params['end'])

    list_data = []
    intervalo = params['interval']
    dt =  __get_dt(intervalo)
    aux_start = start
    aux_end = end
    while( (end - aux_start) >= timedelta(0)):
        if ((end - aux_start)>dt*400):
            aux_end = aux_start + dt*400
        _list = client_klines(symbol=params['symbol'], \
            interval=intervalo,limit=None, \
            startTime=int(aux_start.timestamp()*1000), \
            endTime=int(aux_end.timestamp()*1000))
        list_data.extend(_list)
        for n in track(range(1), description="..."+str(aux_start)): 
            pass
        aux_start = aux_end + dt
        aux_end = end
    
    columns=['Timestamp','Open','High','Low','Close','Volume','Close_time','Quote_Asset_Volume', \
            'Trades','Taker_buy_base_asset_vol','Taker_buy_quote_asset_vol','x']
    df = pd.DataFrame(list_data, columns=columns)\
            .astype({'Timestamp':'datetime64[ms]', 'Open':'float', 'High':'float', 'Low':'float', 'Close':'float',\
                     'Volume':'float'})
    return df

def _df_forecast(df: pd.DataFrame, type_price:str,  n_futures: int, frequency:str)-> pd.DataFrame:
    df['y'] = df[type_price].copy()
    df['ds'] = df['Timestamp']
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=n_futures, freq=frequency)
    forecast = m.predict(future)
    #m.plot(forecast)
    return  forecast

def _mark(msg):
    """ Solo útil para marcar funciones en la salida de la terminal
    """
    for n in track(range(1), description="..."+str(msg)): 
        pass
