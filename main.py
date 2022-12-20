import psycopg2
from sqlalchemy import create_engine, text
from auth import login, create_new_db, drop_db
from tkinter import *
from app import App
import tkinter as tk
import logging

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)
    app = App()
    app.mainloop()
    # engine = create_engine(f'postgresql://admin:admin@localhost/user_db')
    # conn = engine.connect()
    # res = tuple(conn.execute('SELECT is_in_items(\'\'\'keyboard\'\'\', 4)'))
    # print(res[0][0])


    # def is_enough_items_for_order(items: str):
    #     items = items.split(',')
    #     items_dct = {}
    #     for i in range(len(items)):
    #         while items[i][0] == ' ':
    #             items[i] = items[i][1:]
    #         while items[i][-1] == ' ':
    #             items[i] = items[i][:-1]
    #
    #     for item in items:
    #         if item not in items_dct:
    #             items_dct[item] = items.count(item)
    #
    #     return items_dct
    #
    #
    # is_enough_items_for_order('keyboard,      headphones')


