import random
import sqlite3
import time
import datetime

from old import add_user, add_category

last_try = 100

cat = 'test_'


def view(user_id, type_categoris):
    with sqlite3.connect('test.db') as conn:
        rows = []
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM type_categories_{type_categoris} "
                       "WHERE user_token = ?",
                       (user_id,))
        rows.append(cursor.fetchall())
    return rows



def main(nick = None,
          date='segodnya'):
    name = f'name_{last_try}'
    user_id = last_try
    last_name = f'smit_{last_try}'
    current_time = datetime.datetime.now()
    date =current_time.strftime("%D")
    time_register = current_time.strftime("%H:%M:%S")
    if nick is None:
        nick = f'new_user{random.randint(1000, 100000)}'
    add_user(user_id, nick, name, last_name, date, time_register)
    for i in range(random.randint(3, 20)):
        add_category(f'{cat}_{last_name}_{i}', user_id, nick, 'expenses')
    time.sleep(5)

