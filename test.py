import sys
import os

from dotenv import load_dotenv

import PyQt6.QtWidgets

import Lyc_PyQt.db_connection
import Lyc_PyQt.app_ui


# import Lyc_PyQt.DataBase.work_with_csv


import Lyc_PyQt.db_connection


class DB_cl:
    def __init__(self):
        print('hello')
        self.connect_to_db()
        print('bue')

    def connect_to_db(self):
        self.conn = Lyc_PyQt.db_connection.connect_to_db()
        self.conn = self.conn.cursor()


DB_cl()
# class DB_cl:
#     def __init__(self):
#         print('hello')
#         self.connect_to_db()
#         print('bue')
#
#     def connect_to_db(self):
#         self.conn = Lyc_PyQt.db_connection.connect_to_db()
#         self.conn = self.conn.cursor()

    # def combo_box(self):
    #     conn = self.conn
    #     cursor = self.cur
    #     cursor.execute(
    #         """CREATE TABLE IF NOT EXISTS csv_files (
    #                 id INTEGER PRIMARY KEY,
    #                 name TEXT UNIQUE
    #             )"""
    #     )
    #     self.files_combo_box.clear()
    #     tables = cursor.execute("SELECT * FROM csv_files").fetchall()
    #     if tables:
    #         self.files_combo_box.addItems([x[1] for x in tables])
    #     conn.commit()
    #
    # def add_exel_file(self):
    #     self.add_exel_window = Lyc_PyQt.DataBase.work_with_csv.CsvLayout()
    #     self.add_exel_window.show()

    # def get_column_names(self, table="test_data", **kwargs):
    #     conn = self.conn
    #     cursor = self.cur
    #
    #     a = "SELECT * FROM {0} LIMIT 1".format(table)
    #     res = [x[0] for x in cursor.execute(a).description]
    #     return res

    # def get_all_items(self, *args, **kwargs):
    #     conn = self.conn
    #     cursor = self.cur
    #
    #     table = self.files_combo_box.currentText()
    #     a = f"SELECT * FROM {table}"
    #     data = cursor.execute(a).fetchall()
    #     self.table.setRowCount(0)
    #     if data:
    #         self.table.setColumnCount(len(data[0]))
    #         self.table.setHorizontalHeaderLabels(self.get_column_names(table))
    #         for row, line in enumerate(data):
    #             self.table.insertRow(row)
    #             for pos, info in enumerate(line):
    #                 self.table.setItem(
    #                     row, pos, PyQt6.QtWidgets.QTableWidgetItem(str(info))
    #                 )

    # def delete(self, *args, **kwargs):
    #     conn = self.conn
    #     cursor = self.cur
    #
    #     table = self.files_combo_box.currentText()
    #     if "table" in kwargs:
    #         table = kwargs["table"]
    #
    #     selected = self.table.currentRow()
    #     if selected == -1:
    #         PyQt6.QtWidgets.QMessageBox.warning(self, "Warning", "No row chosen")
    #         return None
    #
    #     selected_id = self.table.item(selected, 0).text()
    #     request = f"DELETE FROM {table} WHERE id = ?"
    #     cursor.execute(request, [selected_id])
    #     conn.commit()
    #     self.get_all_items()

