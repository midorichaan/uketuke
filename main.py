import aiohttp
import asyncio
import os
import tkinter
import tkinter.font as font
from logging import basicConfig, getLogger, INFO
from dotenv import load_dotenv

from lib import database

#init environment
load_dotenv()
basicConfig(
    level=INFO, 
    format="%(asctime)s - %(name)s - [%(levelname)s]: %(message)s"
)

#vars
loop = asyncio.get_event_loop()
logger = getLogger("discord")
session = aiohttp.ClientSession(loop=loop)
db = database.Database(
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWD"],
    db=os.environ["DB_DATABASE"]
)
root = tkinter.Tk()
font = font.Font(root, family="無心", size=20)

#programs
def setup_root(manage: bool=False):
    global root, logger
    logger.info("SETUP: setting up...")

    if manage:
        logger.info("SETUP: logged in as root")
        root.title(u"受付管理システム (管理用)")
    else:
        logger.info("SETUP: logged in as user")
        root.title(u"受付管理システム (一般用)")
    root.geometry("400x400")

    
    
if __name__ == "__main__":
    setup_root()
