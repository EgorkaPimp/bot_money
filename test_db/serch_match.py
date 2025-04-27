import sqlite3

def user_exists(user_id: int) -> bool:
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM register_users WHERE user_token = ?",
                       (user_id,))
        return cursor.fetchone() is not None

def user_base_categories_exp_exists(user_id: int) -> bool:
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM type_categories_expenses "
                       "WHERE user_token = ? AND category = ?",
                       (user_id, 'other'))
        return cursor.fetchone() is not None

def user_base_categories_inc_exists(user_id: int) -> bool:
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM type_categories_income "
                       "WHERE user_token = ? AND category = ?",
                       (user_id, 'other'))
        return cursor.fetchone() is not None
