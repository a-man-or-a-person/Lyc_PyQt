import Lyc_PyQt.db_connection


conn = Lyc_PyQt.db_connection.connect_db()

cur = conn.cursor()

cur.execute('INSERT INTO csv_files(name) VALUES ("name1")')
cur.execute(
    """
    SELECT * FROM csv_files
"""
)
a = cur.fetchall()
conn.commit()
print(a)
