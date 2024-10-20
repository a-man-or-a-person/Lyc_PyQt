import sqlite3
import sys

import PyQt6.QtWidgets

import project.UI.work_with_data_ui


class Table_work(project.UI.work_with_data_ui.TableWork):
    def __init__(self):
        super().__init__()
        self.connect_db()
        self.add_btn.clicked.connect(self.get_all_items)
        self.delete_btn.clicked.connect(self.delete)
        self.category_combo_box.addItems(['first', 'second', 'third'])
        self.dev_btn = PyQt6.QtWidgets.QPushButton(parent=self, text='dev')
        self.dev_btn.clicked.connect(self.get_column_names)

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
        return [x[0] for x in self.cursor.execute(a).description]

    def get_all_items(self):
        a = '''
        SELECT * FROM test_data
        '''
        data = self.cursor.execute(a).fetchall()
        print(data)
        if data:
            self.table.setColumnCount(len(data[0]))
            self.table.setHorizontalHeaderLabels(self.get_column_names('test_data'))
            for row, line in enumerate(data):
                self.table.insertRow(row)
                for pos, info in enumerate(line):
                    self.table.setItem(row, pos, PyQt6.QtWidgets.QTableWidgetItem(str(info)))

    def add(self):
        print(self.category_combo_box.currentText())

    def delete(self, table='test_data'):
        selected = self.table.currentRow()
        print(selected)
        if selected == -1:
            PyQt6.QtWidgets.QMessageBox.warning(self, "No row chosen")
            return None

        selected_id = self.table.item(selected, 0).text()
        db_request = 'DELETE FROM {} WHERE id = ?'.format([table])
        self.cursor.execute(db_request, selected_id)
        self.conn.commit()
        self.get_all_items()


if __name__ == '__main__':
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = Table_work()
    window.show()
    sys.exit(app.exec())
