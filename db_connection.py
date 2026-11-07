import functools
import hashlib
import hmac
import os
import pathlib
import secrets
import sqlite3

path = pathlib.Path(os.getenv('EXPENSE_DB_PATH', '.data/user_data.db')).resolve()


def initialize(connection):
    connection.execute('CREATE TABLE IF NOT EXISTS Users (userid INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)')
    connection.execute('CREATE TABLE IF NOT EXISTS tables (tableid INTEGER PRIMARY KEY, userid INTEGER NOT NULL, table_name TEXT UNIQUE NOT NULL)')
    connection.commit()


def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000).hex()
    return f'pbkdf2_sha256$600000${salt}${digest}'


def authenticate_user(connection, username, password):
    row = connection.execute('SELECT userid, password FROM Users WHERE username = ?', (username,)).fetchone()
    if row is None:
        return None
    user_id, stored = row
    if stored.startswith('pbkdf2_sha256$'):
        try:
            _, iterations, salt, expected = stored.split('$')
            if int(iterations) != 600000:
                return None
            actual = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000).hex()
            valid = hmac.compare_digest(actual, expected)
        except (ValueError, TypeError):
            return None
    else:
        valid = hmac.compare_digest(password.encode(), stored.encode())
        if valid:
            connection.execute('UPDATE Users SET password = ? WHERE userid = ?', (hash_password(password), user_id))
            connection.commit()
    return user_id if valid else None


def user_table(cursor, name):
    if not cursor.execute('SELECT 1 FROM tables WHERE table_name = ? AND userid = ?', (name, os.getenv('APP_USER_ID'))).fetchone():
        raise ValueError('Table does not belong to the current user')
    return '"' + name.replace('"', '""') + '"'


def db_conn_wrap(func, db=path):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pathlib.Path(db).parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(db)
        try:
            initialize(connection)
            return func(*args, **kwargs, conn=connection, cursor=connection.cursor())
        finally:
            connection.close()
    return wrapper
