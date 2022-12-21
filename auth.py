import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from tkinter import messagebox
from sqlalchemy_utils.functions import database_exists, drop_database
from math import tanh, ceil


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
        '''Подключаюсь к user_db, выбираю всех юзеров из таблицы и дропаю их,
        надо переписать, используя хранимую процедуру'''
        #TODO: сделать в бд хранимую функцию get_all_users() и drop_role(role_name), возможно с триггером
        conn = create_engine(f'postgresql://{username}:{password}@localhost/user_db').connect()
        res = conn.execute('SELECT username FROM users')
        users = []
        for row in res:
            users.append(row[0])
        for user in users:
            conn.execute(f'DROP ROLE {user};')
        conn.close()

        drop_database(f'postgresql://{username}:{password}@localhost/{db_name}')
        conn = engine.connect()
        conn.execute(text('SELECT f_drop_roles();'))
        conn.close()
        messagebox.showinfo(title='Success', message='User database was successfuly deleted')
    else:
        messagebox.showerror(title='Error', message='User database does not exist')


def registrate_user(username, password, role, engine):
    # conn.execute(text('SELECT create_user(:param1, :param2, :param3);').bindparams(
    #              param1=username, param2=f'\'{password}\'', param3=role))
    conn = engine.connect()
    conn.execute(f'CREATE USER {username} LOGIN PASSWORD \'{password}\';'
                 f'GRANT {role} TO {username};'
                 f'ALTER ROLE {username} INHERIT;'
                 f'INSERT INTO users (username, role) VALUES (\'{username}\', \'{role}\');')
    conn.close()


def check_role(username):
    engine = login('admin', 'admin', 'user_db')
    conn = engine.connect()
    res = conn.execute(f'SELECT role FROM users WHERE username=\'{username}\'')
    for row in res:
        return row[0]


def is_in_storage(item, quantity, engine) -> bool:
    conn = engine.connect()
    res = tuple(conn.execute(text('SELECT is_in_items(:item, :quantity)'),
                             item=f'\'{item}\'', quantity=quantity))[0][0]
    conn.close()
    return res


def str_to_dict(items: str) -> dict:
    items = items.split(',')
    items_dct = {}
    for i in range(len(items)):
        while ' ' in items[i] and items[i][0] == ' ':
            items[i] = items[i][1:]
        while ' ' in items[i] and items[i][-1] == ' ':
            items[i] = items[i][:-1]

        if items[i] == '':
            items.pop(i)

    for item in items:
        if item not in items_dct:
            items_dct[item] = items.count(item)

    return items_dct


def is_enough_items_for_order(items: str, engine) -> bool:

    items_dct = str_to_dict(items)

    for item, cnt in items_dct.items():
        if not is_in_storage(item, cnt, engine):
            return False

    return True


def get_price(item_name, engine):
    conn = engine.connect()
    res = tuple(conn.execute(text('SELECT get_price(:item_name)'), item_name=f'\'{item_name}\''))
    conn.close()
    return res[0][0]


def get_weight(item_name, engine):
    conn = engine.connect()
    res = tuple(conn.execute(text('SELECT get_weight(:item_name)'), item_name=f'\'{item_name}\''))
    conn.close()
    return res[0][0]


def take_from_storage(item_name, quantity, engine):
    conn = engine.connect()
    conn.execute(f'UPDATE item SET quantity=quantity-{quantity} WHERE name=\'{item_name}\';')
    conn.close()


def add_item_to_order(purchase_id, item_name, quantity, engine):
    conn = engine.connect()
    conn.execute(f'INSERT INTO purchase_item(purchase_id, item_name, quantity) VALUES({purchase_id}, \'{item_name}\', {quantity})')
    conn.close()


def get_last_order_id(engine):
    conn = engine.connect()
    res = tuple(conn.execute('SELECT get_last_order_id();'))[0][0]
    conn.close()
    return res


def create_order(buyer_name, status, items: str, engine):

    cur_order_id = get_last_order_id(engine) + 1

    items_dct = str_to_dict(items)

    weight = 0
    price = 0
    for k, v in items_dct.items():
        k = k.strip().replace('\n', '')
        if k == '':
            continue

        add_item_to_order(cur_order_id, k, v, engine)
        weight += v*get_weight(k, engine)
        price += v*get_price(k, engine)
        take_from_storage(k, v, engine)

    price = ceil(float(price) + 5 * tanh(weight/20 - 1) + 5)

    conn = engine.connect()
    # conn.execute(text('SELECT create_order(:buyer_name, :weight, :price, :status);'),
    #              buyer_name=f'\'buyer_name\'', weight=float(weight), price=price, status=f'\'status\'')
    conn.execute(f'INSERT INTO purchase(buyer_name, weight, price, status) VALUES(\'{buyer_name}\', {weight}, {price} , \'{status}\');')

    conn.close()


