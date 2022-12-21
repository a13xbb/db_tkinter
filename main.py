import psycopg2
from sqlalchemy import create_engine, text
from auth import login, create_new_db, drop_db, take_from_storage, get_weight, get_price
from tkinter import *
from app import App
import tkinter as tk
import logging

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)
    app = App()
    app.mainloop()
    # engine = create_engine(f"postgresql+psycopg2://qeq:111@localhost/user_db")
    # conn = engine.connect()
    # conn.execute('INSERT INTO item(name, weight, quantity, price) VALUES(\'mouse\', 22, 44, 55);')
    # conn.close()
    # print(get_weight('keyboard', engine))
    # conn = engine.connect()
    # conn.execute('INSERT INTO purchase(buyer_name, weight, price, status) VALUES(\'aboba\', 22, 43, \'paid\')')
    # conn.close()

