import sqlite3
import sys
import pandas as pd
import re

import PyQt6.QtWidgets

import Lyc_PyQt.UI.csv_input_ui
from Lyc_PyQt.DataBase.decorators import db_conn_wrap


class CsvLayout(Lyc_PyQt.UI.csv_input_ui.CsvViews):
    def __init__(self):
        super().__init__()
        self.display_all_files()
        self.refresh_btn.clicked.connect(self.display_all_files)
        self.add_csv_btn.clicked.connect(self.add_csv)
        self.del_csv_btn.clicked.connect(self.delete)

    @db_conn_wrap
    def display_all_files(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            raise ValueError("No connection to db had been provided")
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS csv_files (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )"""
        )
        data = cursor.execute("SELECT * FROM csv_files").fetchall()
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["id", "filename"])
        if data:
            for row, line in enumerate(data):
                self.table.insertRow(row)
                for pos, info in enumerate(line):
                    self.table.setItem(
                        row, pos, PyQt6.QtWidgets.QTableWidgetItem(str(info))
                    )
        else:
            self.table.insertRow(0)
            for pos, info in enumerate(["no", "files"]):
                self.table.setItem(0, pos, PyQt6.QtWidgets.QTableWidgetItem(str(info)))

    @db_conn_wrap
    def delete(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            raise ValueError("No connection to db had been provided")
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]

        selected = self.table.currentRow()
        if selected == -1:
            PyQt6.QtWidgets.QMessageBox.warning(self, "Warning", "No row chosen")
            return None

        selected_id = self.table.item(selected, 0).text()
        selected_name = self.table.item(selected, 1).text()
        if not selected_id.isdigit():
            PyQt6.QtWidgets.QMessageBox.warning(
                self, "Warning", "You can`t delete this"
            )
            return None
        cursor.execute("DELETE FROM csv_files WHERE name=?", [selected_name])
        cursor.execute(f"DROP TABLE {selected_name}")
        conn.commit()
        self.display_all_files()

    @db_conn_wrap
    def add_csv(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "DB_conn_error", "DB was not provided or couldn't connect"
            )
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]

        PyQt6.QtWidgets.QMessageBox.warning(
            self, "Warning", "File should contain headers"
        )
        path = PyQt6.QtWidgets.QFileDialog.getOpenFileName(self, "Select file")[0]
        if not path:
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "File selection error", "No file was selected"
            )
            return None

        if "/" in path:
            name = path.split("/")[-1]
        else:
            name = path.split("\\")[-1]
        name = "_".join(name.split()).split(".")[0]
        exel_file = pd.ExcelFile(path)
        sheet1 = exel_file.parse(0)
        columns = list(sheet1.columns)
        db_request = f"CREATE TABLE {name} ( id INTEGER PRIMARY KEY,"
        for i in columns[:-1]:
            db_request += f"{i} TEXT, "
        db_request += f"{columns[-1]} TEXT)"
        try:
            cursor.execute(db_request)
        except sqlite3.OperationalError:
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "Table creation failed", "Table already exists"
            )
            return None
        db_request = f"""INSERT INTO {name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in range(len(columns))])})"""
        cursor.executemany(db_request, sheet1.values)
        cursor.execute(f"INSERT INTO csv_files (name) VALUES (?)", [name])
        conn.commit()
        self.display_all_files()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = CsvLayout()
    sys.excepthook = except_hook
    window.show()
    sys.exit(app.exec())
