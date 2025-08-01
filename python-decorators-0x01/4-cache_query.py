import time
import sqlite3
import functools
from dotenv import load_dotenv
import os

# ✅ Load environment variables (if using .env for DB path)
load_dotenv()
DB_PATH = os.getenv("DB_PATH", "users.db")

# ✅ Connection decorator (copied from previous task)
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_PATH)
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ Global cache dictionary
query_cache = {}

# ✅ Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query in query_cache:
            print("[CACHE] Returning cached result.")
            return query_cache[query]
        print("[CACHE MISS] Executing and caching result.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ First call - caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# ✅ Second call - uses cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
