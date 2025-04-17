import logging
import sqlite3

def init_db():
    with sqlite3.connect('db/my_money.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registered (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                nickname TEXT,
                name TEXT,
                last_name TEXT,
                date TEXT,
                time_register TEXT
            )
        ''')
        conn.commit()

async def add_user(user_id, nick_name, name,
             last_name, date, time_register):
    init_db()
    with sqlite3.connect('db/my_money.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registered (user_id, nickname, name, "
                       "last_name, date, time_register)"
                       "VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, nick_name, name,
                        last_name, date, time_register))
        conn.commit()
        logging.info(f'Add user {name} {last_name}')

