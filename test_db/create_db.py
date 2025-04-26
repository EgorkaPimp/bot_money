import logging
import sqlite3
# from serch_match import base_categories_exists, base_categories_income ,user_exists

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

        # if base_categories_exists():
        #     logging.info(f'Base categories exists')
        #     print(f'Base categories exists')
        # else:
        #     if user_exists(1):
        #         cursor.execute("INSERT INTO register_users (user_token, nick_name, name, "
        #                        "last_name, date, time_register)"
        #                        "VALUES (?, ?, ?, ?, ?, ?)",
        #                        (1, 'bot_god', 'bot_god',
        #                         None, None, None))
        #         conn.commit()
        #         logging.info(f'Add user GOD_BOT')
        #
        #     base_categories = ['food', 'transport', 'entertainment', 'health',
        #                      'clothing', 'home', 'other']
        #
        #     for category in base_categories:
        #         cursor.execute("INSERT INTO type_categories_expenses (user_token, nick_name, category)"
        #                        "VALUES (?, ?, ?)",
        #                        (1, 'bot_god', category))
        #         conn.commit()
        #
        # if base_categories_income():
        #     logging.info(f'Base categories income')
        #     print(f'Base categories income')
        # else:
        #     if user_exists(1):
        #         cursor.execute("INSERT INTO register_users (user_token, nick_name, name, "
        #                        "last_name, date, time_register)"
        #                        "VALUES (?, ?, ?, ?, ?, ?)",
        #                        (1, 'bot_god', 'bot_god',
        #                         None, None, None))
        #         conn.commit()
        #         logging.info(f'Add user GOD_BOT')
        #
        #     base_categories = ['salary', 'other']
        #
        #     for category in base_categories:
        #         cursor.execute("INSERT INTO type_categories_income (user_token, nick_name, category)"
        #                        "VALUES (?, ?, ?)",
        #                        (1, 'bot_god', category))
        #         conn.commit()