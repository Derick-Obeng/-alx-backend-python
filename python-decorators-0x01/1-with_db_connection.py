import sqlite3
import functools
import os
from dotenv import load_dotenv

# ✅ Load env variables from .env
load_dotenv()
DB_PATH = os.getenv("DB_PATH")

# ✅ Decorator that injects DB connection from env
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_PATH)  # Use env-configured path
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# ✅ Call the function (conn is handled for you)
user = get_user_by_id(user_id=1)
print(user)
