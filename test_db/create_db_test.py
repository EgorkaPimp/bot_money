import logging
import sqlite3

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
            CREATE TABLE IF NOT EXISTS type_categories_expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_token INTEGER,
                nick_name TEXT,
                category TEXT,
                FOREIGN KEY (user_token) REFERENCES register_users(user_token)
                    ON DELETE CASCADE
            )
        ''')
        conn.commit()

        cursor.execute('''
               CREATE TABLE IF NOT EXISTS type_categories_income (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_token INTEGER,
                   nick_name TEXT,
                   category TEXT,
                   FOREIGN KEY (user_token) REFERENCES register_users(user_token)
                       ON DELETE CASCADE
               )
           ''')
        conn.commit()
