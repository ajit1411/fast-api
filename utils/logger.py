import logging
from datetime import datetime

def error(api, title, error):
    logging.error(f"{api} Error [{datetime.now()}] : {title} :: {error}")