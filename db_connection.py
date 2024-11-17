import mysql.connector


def connect_to_db():
    conn = mysql.connector.connect(
        host="192.168.1.111",
        user="dbuser1",
        # user="dbeaver",
        password="1234",
        port='3306',
        database='LicPyqt'
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM employee.salary LIMIT 15')
    a = cur.fetchall()
    for i in a:
        print(i)

    return conn