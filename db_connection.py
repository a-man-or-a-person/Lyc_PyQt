import mysql.connector


def connect_db():

    connection = mysql.connector.connect(
        host="192.168.1.111",
        database="LicPyqt",
        user="licpr",
        password="1234"
    )
    return connection

