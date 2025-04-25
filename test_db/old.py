import logging
import sqlite3
from serch_match import user_exists

def init_db():
    with sqlite3.connect('test.db') as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS register_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_token INTEGER UNIQUE,
                nick_name TEXT,
                name TEXT,
                last_name TEXT,
                date TEXT,
                time_register TEXT
            )
        ''')
        conn.commit()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS type_category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_token INTEGER,
                nick_name TEXT,
                category TEXT,
                FOREIGN KEY (user_token) REFERENCES register_users(user_token)
                    ON DELETE CASCADE
            )
        ''')
        conn.commit()

def add_user(user_id, nick_name, name,
             last_name, date, time_register):
    init_db()
    if user_exists(user_id):
        logging.info(f'User {user_id}:{nick_name} exists')
        print(f'User {user_id}:{name}_{last_name} exists')
    else:
        with sqlite3.connect('test.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO register_users (user_token, nick_name, name, "
                           "last_name, date, time_register)"
                           "VALUES (?, ?, ?, ?, ?, ?)",
                           (user_id, nick_name, name,
                            last_name, date, time_register))
            conn.commit()
            logging.info(f'Add user {name} {last_name}')


def category(cat, user_id, nick_name):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO type_category (user_token, nick_name, category)"
                       "VALUES (?, ?, ?)",
                       (user_id, nick_name, cat))
        conn.commit()
        logging.info(f'Add new category for {user_id}:{nick_name}')