# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import os
import sys
import time
import tkinter as tk
import tkinter.font as font

from dotenv import load_dotenv
from lib import database
from logging import basicConfig, getLogger, INFO

#load .env
load_dotenv()

#logger
basicConfig(
	level=INFO,
	format="%(asctime)s - %(name)s - [%(levelname)s]: %(message)s"
)

#global vars
loop = asyncio.get_event_loop()
session = aiohttp.ClientSession()
logger = getLogger("manage-system")
db = database.Database(
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWD"],
    db=os.environ["DB_DATABASE"]
)

class Application(tk.Tk):

    def __init__(self, *, managed: bool=False):
        super().__init__()

        self.entries = {}
        self._managed = managed
        self._id = None
        self._font = font.Font(self, family="無心", size=20)
        self._init()

    #_get_id_from_db
    async def _get_id_from_db(self):
    	query = await db.fetchall("SELECT * FROM uketuke")
    	self._id = len(query) + 1

    #post_dara
    async def post_data(self, id: int, name: str):
        try:
            async with session.request(
                "POST", 
                "https://api.midorichan.cf/v1/special/bunkasai",
                headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
                json={"id": id, "name": name}
            ) as r:
                if r.status == 200:
                    return True
                else:
                    return False
        except Exception as exc:
            logger.error(exc)
            return False

    #_get_id
    def _get_id(self):
        loop.run_until_complete(self._get_id_from_db())
        return self._id

    #_submit_data
    def _submit_data(self):
        logger.info("APP: data submitted")
        data = {
            "name": self.entries["name_entry"].get(),
            "id": self._get_id()
        }
        logger.info(f"APP: submitted data - {data}")
        self._delete_text()

        if not data["name"]:
            logger.warning("APP: name is a required argument that is missing")
       	    return
       	else:
       	    query = self.post_data(data["id"], data["name"])
            loop.run_until_complete(query)

    #_delete_text
    def _delete_text(self):
    	logger.info("APP: text 'name' cleared")
    	self.entries["name_entry"].delete(0, tk.END)

    #_init
    def _init(self):
        if self._managed:
            logger.info("APP: application run as staff")
            self.title("受付管理システム (管理用)")

            #label
            name_label = tk.Label(self, text="名前", font=self._font)
            #text box
            name_entry = tk.Entry()
            name_entry.configure(state="normal", width=30)
            #buttons
            submit = tk.Button(text="完了", width=20, command=self._submit_data)
            cancel = tk.Button(text="キャンセル", width=20, command=self._delete_text)

            #add data
            self.entries["name_label"] = name_label
            self.entries["name_entry"] = name_entry
            self.entries["submit_button"] = submit
            self.entries["cancel_button"] = cancel
  
            #place items
            """
            for k, v in self.entries.items():
                if "entry" in str(k):
                    v.pack()             
                elif "label" in str(k):
                    v.pack()
                elif "button" in str(k):
                    v.grid()
            """
            self.entries["name_label"].pack()
            self.entries["name_entry"].pack()
            self.entries["submit_button"].pack()
            self.entries["cancel_button"].pack()
        else:
            logger.info("APP: application run as user")
            self.title("受付システム (一般用)")



        exit = tk.Button(text="終了", width=20, command=lambda: self.quit())
        self.entries["exit_button"] = exit
        self.entries["exit_button"].pack()

        self.geometry("600x400")
        self.resizable(False, False)

#handle_argunent
def handle_argument(args):
    if len(args) == 2:
        if args[1] == "-staff":
            return True
        elif args[1] == "-user":
            return False
        else:
            return
    else:
	    return

if __name__ == "__main__":
    args = sys.argv
    val = handle_argument(args)
    app = None

    if not val == None:
        try:
            app = Application(managed=val)
            app.mainloop()
            logger.info("RUN: successfully runned application")
        except Exception as exc:
            logger.error(f"RUN: {exc}")
            app.quit()
            logger.info("RUN: application exited")
    else:
        logger.error("RUN: invalid argument")