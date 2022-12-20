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

