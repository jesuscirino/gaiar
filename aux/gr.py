import logging
from rich.logging import RichHandler

def _debugit(msg):

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    #logging.info(msg)
    logging.debug(msg)

def _get_klines(client_klines , params: dict) -> list:
    return client_klines(symbol=params['symbol'], interval=params['interval'],limit=params['limit'])