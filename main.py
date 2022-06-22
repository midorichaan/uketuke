import aiohttp
import asyncio
import database
import os
import tkinter
import tkinter.font as font
from dotenv import load_dotenv

#init environment
load_dotenv()

#vars
loop = asyncio.get_event_loop()
session = aiohttp.ClientSession()
db = database.Database()
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
