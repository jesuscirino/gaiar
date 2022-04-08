import logging
from binance.spot import Spot as Client

from config import SECRET_KEY as secret
from config import API_KEY as key
from config import BASE_URL as base

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
install()

import pandas as pd
def debugit(msg):

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    #logging.info(msg)
    logging.debug(msg)

c = Console()



if __name__ == "__main__":
    client = Client(key, secret, base_url=base)
    account_info = client.account(recvWindow=6000)
    df_balances = pd.DataFrame(account_info['balances'])
    df_balances['free'] = pd.to_numeric(df_balances['free'],errors='coerce').fillna(0)
    df_balances['locked'] = pd.to_numeric(df_balances['free'],errors='coerce').fillna(0)
    c.print(account_info.keys())
    c.print(df_balances.info())
    c.print(df_balances[df_balances['free']>0])
    #c.print(df_balances[df_balances['asset']=='XRP'])
    del df_balances