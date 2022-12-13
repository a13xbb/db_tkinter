import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from tkinter import messagebox
from sqlalchemy_utils.functions import database_exists, drop_database


def login(username, password):
    engine = create_engine(f"postgresql://{username}:{password}@localhost/super_db")
    conn = engine.connect()
    return conn


def create_new_db(db_name, conn):
    if not database_exists('postgresql://postgres@localhost/user_db'):
        conn.execute(text('SELECT f_create_db(:param)'), param=db_name)
        messagebox.showinfo(title='Success', message='User database was successfuly created')
    else:
        messagebox.showerror(title='Error', message='User database already exists')


def drop_db(db_name, conn):
    conn.execute(text('SELECT f_drop_db(:param)'), param=db_name)
