import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from tkinter import messagebox
from sqlalchemy_utils.functions import database_exists, drop_database


def login(username, password, dbname):
    engine = create_engine(f"postgresql://{username}:{password}@localhost/{dbname}")
    conn = engine.connect()
    return conn


def create_new_db(db_name, conn, username, password):
    if not database_exists(f'postgresql://{username}:{password}@localhost/{db_name}'):
        conn.execute(text('SELECT f_create_db(:param)'), param=db_name)
        messagebox.showinfo(title='Success', message='User database was successfuly created')
    else:
        messagebox.showerror(title='Error', message='User database already exists')


def drop_db(db_name, conn, username, password):
    if database_exists(f'postgresql://{username}:{password}@localhost/{db_name}'):
        drop_database(f'postgresql://{username}:{password}@localhost/{db_name}')
        conn.execute(text('SELECT f_drop_roles()'))
        messagebox.showinfo(title='Success', message='User database was successfuly deleted')
    else:
        messagebox.showerror(title='Error', message='User database does not exist')


def registrate_user(username, role):
    pass

