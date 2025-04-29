import logging
import sqlite3

from numpy.ma.core import append


def user_exists(user_id: int) -> bool:
    with sqlite3.connect('db/my_money.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM register_users WHERE user_token = ?",
                       (user_id,))
        return cursor.fetchone() is not None

def user_base_categories_exp_exists(user_id: int) -> bool:
    with sqlite3.connect('db/my_money.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM type_categories_expenses "
                       "WHERE user_token = ? AND category = ?",
                       (user_id, 'other'))
        return cursor.fetchone() is not None

def user_base_categories_inc_exists(user_id: int) -> bool:
    with sqlite3.connect('db/my_money.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM type_categories_income "
                       "WHERE user_token = ? AND category = ?",
                       (user_id, 'other'))
        return cursor.fetchone() is not None

def user_nick(user_id: int) -> bool:
    rows = []
    with sqlite3.connect('db/my_money.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT nick_name FROM register_users "
                       "WHERE user_token = ?",
                       (user_id,))
        rows.append((cursor.fetchall()[0]))
        nick = (rows[0])[0]
        return nick

def user_categories(user_id: int, category: str, type: str) -> bool:
    with sqlite3.connect('db/my_money.db') as conn:
        logging.info(f'id = {user_id} \n'
                     f'category = {category}')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM type_categories_{type} "
                       "WHERE user_token = ? AND category = ?",
                       (user_id, category))
        return cursor.fetchone() is not None