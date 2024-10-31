import functools
import sqlite3


def db_conn_wrap(func, db="user_data.db"):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        val = func(*args, **kwargs, conn=connection, cursor=cursor)
        connection.close()
        return val

    return wrapper
