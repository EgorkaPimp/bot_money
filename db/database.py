import logging
import sqlite3
from .create_db import init_db
from .serch_match import user_exists, user_base_categories_exp_exists, user_base_categories_inc_exists

async def add_user(user_id, nick_name, name,
             last_name, date, time_register):
    init_db()
    if user_exists(user_id):
        logging.info(f'User {user_id}:{nick_name} exists')
        print(f'User {user_id}:{name}_{last_name} exists')
        return False
    else:
        with sqlite3.connect('db/my_money.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO register_users (user_token, nick_name, name, "
                           "last_name, date, time_register)"
                           "VALUES (?, ?, ?, ?, ?, ?)",
                           (user_id, nick_name, name,
                            last_name, date, time_register))
            conn.commit()
            logging.info(f'Add user {user_id}:{nick_name}')
            print(f'Add user {user_id}:{name}_{last_name}')

            if user_base_categories_exp_exists(user_id):
                logging.info(f'Base categories expenses exists')
                print(f'Base categories expenses exists')
            else:
                base_categories = ['food', 'transport', 'entertainment', 'health',
                                     'clothing', 'home', 'other']

                for category in base_categories:
                    cursor.execute("INSERT INTO type_categories_expenses (user_token, nick_name, category)"
                                   "VALUES (?, ?, ?)",
                                   (user_id, nick_name, category))
                    conn.commit()
                logging.info(f'Base categories expenses created')
                print(f'Base categories expenses created')
            if user_base_categories_inc_exists(user_id):
                logging.info(f'Base categories income exists')
                print(f'Base categories income exists')
            else:
                base_categories = ['salary', 'other']
                for category in base_categories:
                    cursor.execute("INSERT INTO type_categories_income (user_token, nick_name, category)"
                                   "VALUES (?, ?, ?)",
                                   (user_id, nick_name, category))
                    conn.commit()
                logging.info(f'Base categories income created')
                print(f'Base categories income created')
            return True

def delete_user(user_id):
    with sqlite3.connect('db/my_money.db') as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM register_users WHERE user_token = ?", (user_id,))
        conn.commit()

async def add_category(cat, user_id, nick_name, type_categories):
    with sqlite3.connect('db/my_money.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO type_categories_{type_categories} (user_token, nick_name, category)"
                       "VALUES (?, ?, ?)",
                       (user_id, nick_name, cat))
        conn.commit()
        logging.info(f'Add new category for {user_id}:{nick_name}')