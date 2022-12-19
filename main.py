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

    # engine = create_engine(f"postgresql+psycopg2://admin:admin@localhost/user_db",
    #                        echo='debug')
    # conn = engine.connect()
    # # conn.execute(text('SELECT create_user(:param1, :param2, :param3)').bindparams(
    # #     param1='Ivan', param2='\'pswd\'', param3='accountant'))
    # conn.execute('CREATE USER ivan WITH ROLE accountant LOGIN PASSWORD \'pswd\';')
    # conn.close()

