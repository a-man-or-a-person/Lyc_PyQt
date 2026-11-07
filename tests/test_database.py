import os
import sqlite3

from db_connection import initialize, hash_password, authenticate_user, user_table, db_conn_wrap


def test_passwords_unknown_users_and_sql_input():
    with sqlite3.connect(':memory:') as conn:
        initialize(conn)
        hashed = hash_password('example-only')
        assert hashed != 'example-only'
        conn.execute('INSERT INTO Users VALUES (1, ?, ?)', ("o'connor", hashed))
        assert authenticate_user(conn, "o'connor", 'example-only') == 1
        assert authenticate_user(conn, "o'connor", 'wrong') is None
        assert authenticate_user(conn, "' OR 1=1 --", 'example-only') is None
        assert authenticate_user(conn, 'unknown', 'example-only') is None


def test_legacy_password_upgrades_only_after_success():
    with sqlite3.connect(':memory:') as conn:
        initialize(conn)
        conn.execute('INSERT INTO Users VALUES (1, ?, ?)', ('demo', 'legacy-only'))
        assert authenticate_user(conn, 'demo', 'wrong') is None
        assert conn.execute('SELECT password FROM Users').fetchone()[0] == 'legacy-only'
        assert authenticate_user(conn, 'demo', 'legacy-only') == 1
        assert conn.execute('SELECT password FROM Users').fetchone()[0].startswith('pbkdf2_sha256$')


def test_table_access_checks_ownership(monkeypatch):
    with sqlite3.connect(':memory:') as conn:
        initialize(conn)
        conn.execute('INSERT INTO tables VALUES (1, 2, ?)', ('expenses',))
        monkeypatch.setenv('APP_USER_ID', '1')
        try:
            user_table(conn.cursor(), 'expenses')
        except ValueError:
            pass
        else:
            raise AssertionError('Other user table accepted')
        monkeypatch.setenv('APP_USER_ID', '2')
        assert user_table(conn.cursor(), 'expenses') == '"expenses"'
