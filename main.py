import aiohttp
import asyncio
import os
import sys
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
    global root
    logger.info("SETUP: setting up...")

    if manage:
        logger.info("SETUP: logged in as root")
        root.title(u"受付管理システム (管理用)")
    else:
        logger.info("SETUP: logged in as user")
        root.title(u"受付管理システム (一般用)")
    root.geometry("400x400")

#init_database
async def init_database():
    logger.info("SETUP: database init")
    await db.execute(
        "CREATE TABLE IF NOT EXISTS uketuke(user_id INTEGER, name TEXT, point BIGINT)",
    )

#handle_args
def handle_args(args):
    if args[1] and len(args) == 2:
        if args[1] == "-staff":
            return True
        elif args[1] == "-user":
            return False
    else:
        logger.error("INIT: setup failed (invalid args)")
        return
    
if __name__ == "__main__":
    args = sys.argv
    ret = handle_args(args)

    #setup
    setup_root(manage)
