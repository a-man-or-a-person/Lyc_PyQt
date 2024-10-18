import sqlite3
import sys

import PyQt6.QtWidgets

import project.UI.work_with_data_ui


class Table_work(project.UI.work_with_data_ui.TableWork):
    def __init__(self):
        super().__init__()
        self.add_btn.clicked.connect(self.add)
        self.category_combo_box.addItems(['first', 'second', 'third'])


    def connect_db(self):
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS data
        #                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                       category TEXT NOT NULL,
        #                       value TEXT NOT NULL)''')
    def add(self):
        print(self.category_combo_box.currentText())



if __name__ == '__main__':
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = Table_work()
    window.show()
    sys.exit(app.exec())
