import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from tkinter import messagebox
from sqlalchemy_utils.functions import database_exists, drop_database


def login(username, password, dbname):
    engine = create_engine(f"postgresql+psycopg2://{username}:{password}@localhost/{dbname}",
                           echo='debug')
    conn = engine.connect()
    conn.close()
    # conn = psycopg2.connect(f"host='localhost' dbname={dbname} user={username} password={password}")
    return engine


def create_new_db(db_name, engine, username, password):
    if not database_exists(f'postgresql://{username}:{password}@localhost/{db_name}'):
        conn = engine.connect()
        conn.execute(text('SELECT f_create_db(:param)'), param=db_name)
        conn.close()
        messagebox.showinfo(title='Success', message='User database was successfuly created')
    else:
        messagebox.showerror(title='Error', message='User database already exists')


def drop_db(db_name, engine, username, password):
    if database_exists(f'postgresql://{username}:{password}@localhost/{db_name}'):
        drop_database(f'postgresql://{username}:{password}@localhost/{db_name}')
        conn = engine.connect()
        conn.execute(text('SELECT f_drop_roles()'))
        conn.close()
        messagebox.showinfo(title='Success', message='User database was successfuly deleted')
    else:
        messagebox.showerror(title='Error', message='User database does not exist')


def registrate_user(username, password, role, engine):
    # conn.execute(text('SELECT create_user(:param1, :param2, :param3);').bindparams(
    #              param1=username, param2=f'\'{password}\'', param3=role))
    conn = engine.connect()
    conn.execute(f'CREATE USER {username} WITH ROLE {role} LOGIN PASSWORD \'{password}\';'
                 f'INSERT INTO users (username, role) VALUES (\'{username}\', \'{role}\');')
    conn.close()

    # conn.exec_driver_sql('SELECT create_user(%(param1)s, %(param2)s, %(param3)s);',
    #                      dict(param1=username, param2=f'\'{password}\'', param3=role))


def check_role(username):
    engine = login('admin', 'admin', 'user_db')
    conn = engine.connect()
    res = conn.execute(f'SELECT role FROM users WHERE username=\'{username}\'')
    for row in res:
        return row[0]

