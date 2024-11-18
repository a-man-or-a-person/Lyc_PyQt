import sys
import os

import PyQt6.QtWidgets


import Lyc_PyQt.DataBase.work_with_csv
from Lyc_PyQt.db_connection import db_conn_wrap
import Lyc_PyQt.UI.Tabel_work_ui

from dotenv import load_dotenv


class Table_work(Lyc_PyQt.UI.Tabel_work_ui.TableWork):
    def __init__(self):
        super().__init__()
        self.refresh_btn.clicked.connect(self.combo_box)
        self.select_btn.clicked.connect(self.get_all_items)
        self.delete_btn.clicked.connect(self.delete)
        # self.conn = Lyc_PyQt.db_connection.connect_db()
        # self.cur = self.conn.cursor()
        self.combo_box()

    @db_conn_wrap
    def combo_box(self, *args, **kwargs):
        print('hello')
        if not ("conn" in kwargs or "cursor" in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "DB_conn_error", "DB was not provided or couldn't connect"
            )
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]
        load_dotenv()
        # conn = self.conn
        # cursor = self.cur
        self.files_combo_box.clear()
        user_id = os.environ.get("USER")

        cursor.execute(f"SELECT table_name FROM tables WHERE userid='{user_id}'")
        tables = cursor.fetchall()
        print(tables)
        if tables:
            self.files_combo_box.addItems([x[0] for x in tables])
        conn.commit()

    @db_conn_wrap
    def get_column_names(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "DB_conn_error", "DB was not provided or couldn't connect"
            )
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]
        table = "tables"
        a = "SELECT * FROM {0} LIMIT 1".format(table)
        cursor.execute(a)
        res = [x[0] for x in cursor.description]
        cursor.fetchall()
        return res

    @db_conn_wrap
    def get_all_items(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "DB_conn_error", "DB was not provided or couldn't connect"
            )
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]
        table = self.files_combo_box.currentText()
        a = f"SELECT * FROM '{table}'"
        cursor.execute(a)
        data = cursor.fetchall()
        self.table.setRowCount(0)
        if data:
            self.table.setColumnCount(len(data[0]))
            self.table.setHorizontalHeaderLabels(self.get_column_names(table))
            for row, line in enumerate(data):
                self.table.insertRow(row)
                for pos, info in enumerate(line):
                    self.table.setItem(
                        row, pos, PyQt6.QtWidgets.QTableWidgetItem(str(info))
                    )

    @db_conn_wrap
    def delete(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "DB_conn_error", "DB was not provided or couldn't connect"
            )
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]

        table = self.files_combo_box.currentText()

        selected = self.table.currentRow()
        if selected == -1:
            PyQt6.QtWidgets.QMessageBox.warning(self, "Warning", "No row chosen")
            return None

        selected_id = self.table.item(selected, 0).text()
        request = f"DELETE FROM {table} WHERE id = '{selected_id}'"
        cursor.execute(request)
        conn.commit()
        self.get_all_items()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = Table_work()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
