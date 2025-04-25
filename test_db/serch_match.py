import sqlite3

def user_exists(user_id: int) -> bool:
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM register_users WHERE user_token = ?", (user_id,))
        return cursor.fetchone() is not None

