import sqlite3
import sys

import PyQt6.QtWidgets

import project.UI.work_with_data_ui


class Table_work(project.UI.work_with_data_ui.TableWork):
    def __init__(self):
        super().__init__()
        self.connect_db()
        self.add_btn.clicked.connect(self.get_column_names)
        self.delete_btn.clicked.connect(self.get_all_items)
        self.category_combo_box.addItems(['first', 'second', 'third'])


    def connect_db(self):
        self.conn = sqlite3.connect('user_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS test_data(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                category TEXT NOT NULL,
                                value TEXT NOT NULL
                                )
                            ''')

    def add_item(self):
        add_item = '''
        INSERT INTO test_data (category, value)
        VALUES(?, ?)
        '''
        vals = ['fruits', 'grapes']
        self.cursor.execute(add_item, vals)
        self.conn.commit()
        print('Item added')

    def get_column_names(self, table='test_data'):
        a = 'SELECT * FROM {0} LIMIT 1'.format(table)

        print(self.cursor.execute(a).fetchall())
        print([x[0] for x in self.cursor.execute(a).description])


    def get_all_items(self):
        a = '''
        SELECT * FROM test_data
        '''
        data = self.cursor.execute(a).fetchall()
        print(data)
        if data:
            self.table.setColumnCount(len(data[0]))
            self.table.setHorizontalHeaderLabels(self.get_column_names('test_data'))
            # self.table.insertRow(row)

        # print(self.description_edit.text())
        # a = self.cursor.execute(a, [str(self.description_edit.text())])
        # print(a.fetchall())

    def add(self):
        print(self.category_combo_box.currentText())


if __name__ == '__main__':
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = Table_work()
    window.show()
    sys.exit(app.exec())
