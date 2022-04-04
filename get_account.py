import logging
from binance.spot import Spot as Client

from config import SECRET_KEY as secret
from config import API_KEY as key
from config import BASE_URL as base

from rich.console import Console
from rich.logging import RichHandler

def debugit(msg):

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    #logging.info(msg)
    logging.debug(msg)

con = Console()

client = Client(key, secret, base_url=base)
#logging.info(client.account(recvWindow=6000))
con.log(client.account(recvWindow=6000))
#debugit(client.account(recvWindow=6000))