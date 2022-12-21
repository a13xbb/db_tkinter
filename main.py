import psycopg2
from sqlalchemy import create_engine, text
from auth import login, create_new_db, drop_db, take_from_storage, get_weight, get_price, search_purchase_by_name
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
    # print(search_purchase_by_name('alex', engine))

    # conn = engine.connect()
    # res = tuple(conn.execute('SELECT get_last_order_id();'))[0][0]
    # conn.close()
    # print(res)


    # print(get_weight('keyboard', engine))
    # conn = engine.connect()
    # conn.execute('INSERT INTO purchase(buyer_name, weight, price, status) VALUES(\'aboba\', 22, 43, \'paid\')')
    # conn.close()

# TODO:
#   1) реализовать поиск заказа по id, имени покупателя и статусу
#   2) реализовать страницу manage items (добавлять или обновлять предмет (name, quantity))
#       Add items [already registered] (name, quantity) if not exists - error;
#       Register Item [new] (name, weight, price) if exists - upd or add; price <=0, weight <=0
#   3) реализовать страницу accountant:
#       toggle purchase status
#       search transaction by buyer_name
