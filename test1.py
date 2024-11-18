from Lyc_PyQt.db_connection import db_conn_wrap


@db_conn_wrap
def app(*args, **kwargs):
    print(kwargs)

app()
