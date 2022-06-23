#! /usr/bin/python
# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import os
import sys
import time
import tkinter as tk
import tkinter.font as font

from tkinter import messagebox
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
        self._cache = None
        self._managed = managed
        self._font = font.Font(self, family="無心", size=20)
        self._init()

    #_call_box
    def _call_box(self, text: str):
        messagebox.showinfo(text)

    #post_dara
    async def post_data(self, id: int, point: int):
        try:
            async with session.request(
                "POST", 
                "https://api.midorichan.cf/v1/special/bunkasai",
                headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
                json={"id": id, "point": point}
            ) as r:
                if r.status == 200:
                    return True
                else:
                    return False
        except Exception as exc:
            logger.error(exc)
            return False

    #_check_id
    async def _check_id(self, id: int):
        d = await db.fetchone(
            "SELECT * FROM uketuke WHERE id=%s",
            (id,)
        )
        self._cache = d

    #_submit_data
    def _submit_data(self):
        logger.info("APP: data submitted")

        n = self.entries["name_entry"].get()
        p = self.entries["point_entry"].get()

        if n is None or n == "":
            logger.warning("APP: missing entry 'name'")
            self._call_box("エラー: IDを入力してください")
            return
        if p is None or p == "":
            logger.warning("APP: missing entry 'point'")
            self._call_box("エラー： ポイントを入力してください")
            return

        loop.run_until_complete(self._check_id(n))
        
        if self._cache:
            logger.warning(f"APP: id {n} already exists")
            self._call_box("エラー： 入力されたIDはすでに存在します")
            return

        data = {
            "id": int(n),
            "point": int(p)
        }
        logger.info(f"APP: submitted data - {data}")
        self._delete_text()

        if not data["id"]:
            logger.warning("APP: id is a required argument that is missing")
       	    return
       	else:
       	    query = self.post_data(data["id"], data["point"])
            loop.run_until_complete(query)

    #_delete_text
    def _delete_text(self):
        logger.info("APP: text 'name' cleared")
        self.entries["name_entry"].delete(0, tk.END)
        logger.info("APP: text 'point' cleared")
        self.entries["point_var"].set(70)

    #_init
    def _init(self):
        if self._managed:
            logger.info("APP: application run as staff")
            self.title("受付管理システム (管理用)")

            #vars
            _s1 = tk.StringVar()
            _s2 = tk.IntVar()
            _s2.set(70)
            #label
            name_label = tk.Label(self, text="ID", font=self._font)
            point_label = tk.Label(self, text="ポイント", font=self._font)
            #text box
            name_entry = tk.Entry(self, font=self._font, textvariable=_s1, width=20, state="normal")
            point_entry = tk.Entry(self, font=self._font, textvariable=_s2, width=20, state="normal")
            #buttons
            submit = tk.Button(self, text="完了", width=20, font=self._font, command=self._submit_data)
            cancel = tk.Button(self, text="クリア", width=20, font=self._font, command=self._delete_text)

            #add data
            self.entries["name_label"] = name_label
            self.entries["name_entry"] = name_entry
            self.entries["point_label"] = point_label
            self.entries["point_entry"] = point_entry
            self.entries["submit_button"] = submit
            self.entries["cancel_button"] = cancel
            self.entries["name_var"] = _s1
            self.entries["point_var"] = _s2

            #place data
            self.entries["name_label"].pack()
            self.entries["name_entry"].pack()
            self.entries["point_label"].pack()
            self.entries["point_entry"].pack()
            self.entries["submit_button"].pack()
            self.entries["cancel_button"].pack()
        else:
            logger.info("APP: application run as user")
            self.title("受付システム (一般用)")

            _s = tk.StringVar()
            #label
            n_lv = tk.Label(self, text="ID", font=self._font)
            #entry
            n_ent = tk.Entry(self, font=self._font, textvariable=_s, width=20, state="normal")

            #add data
            self.entries["name_label"] = n_lv
            self.entries["name_entry"] = n_ent 

            #place data
            self.entries["name_label"].pack()
            self.entries["name_entry"].pack()

        exit = tk.Button(text="終了", width=20, font=self._font, command=lambda: self.quit())
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