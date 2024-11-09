import functools
import sqlite3
import pathlib

path = pathlib.Path('DataBase/user_data.db').resolve()

def db_conn_wrap(func, db=path):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        val = func(*args, **kwargs, conn=connection, cursor=cursor)
        connection.close()
        return val

    return wrapper
