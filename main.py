import aiohttp
import asyncio
import os
import tkinter
import tkinter.font as font
from dotenv import load_dotenv

from lib import database

#init environment
load_dotenv()

#vars
loop = asyncio.get_event_loop()
session = aiohttp.ClientSession()
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

    if manage:
        root.title(u"受付管理システム (管理用)")
    else:
        root.title(u"受付管理システム (一般用)")
    root.geometry("400x400")

    
    
if __name__ == "__main__":
    pass
