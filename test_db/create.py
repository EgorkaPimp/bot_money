import random
import sqlite3
import time

from old import add_user, category

user_id = 777
nick_name = 'god'
name = 'egor'
last_name = 'gorelov'
date = 'segodnya'
time_register = '11:11'

cat = 'test_'

def delete(user_id):
    with sqlite3.connect('test.db') as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM register_users WHERE user_token = ?", (user_id,))
        conn.commit()


def main(nick = None):
    if nick is None:
        nick = f'new_user{random.randint(1000, 100000)}'
    add_user(user_id, nick, name, last_name, date, time_register)
    for i in range(10):
        category(f'{cat}{i}', user_id, nick)

main()