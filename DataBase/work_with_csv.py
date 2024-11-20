import sys
import pandas as pd
import mysql.connector

from dotenv import load_dotenv
import os
import PyQt6.QtWidgets

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QStackedWidget,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
)
import UI.csv_ui
from db_connection import db_conn_wrap


class CsvLayout(UI.csv_ui.CsvViews):
    def __init__(self):
        super().__init__()
        # self.connection = db_connection.connect_db()
        # self.cur = self.connection.cursor()
        self.refresh_btn.clicked.connect(self.display_all_files)
        self.add_csv_btn.clicked.connect(self.add_csv)
        self.del_csv_btn.clicked.connect(self.delete)

    @db_conn_wrap
    def display_all_files(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "DB_conn_error", "DB was not provided or couldn't connect"
            )
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]
        load_dotenv()
        user_id = os.getenv("USER")
        cursor.execute(
            f"SELECT tableid, table_name FROM tables WHERE userid='{user_id}'"
        )
        data = cursor.fetchall()
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["table_id", "filename"])
        if data:
            for row, line in enumerate(data):
                self.table.insertRow(row)
                for pos, info in enumerate(line):
                    self.table.setItem(row, pos, QTableWidgetItem(str(info)))
        else:
            self.table.insertRow(0)
            for pos, info in enumerate(["no", "files"]):
                self.table.setItem(0, pos, QTableWidgetItem(str(info)))

    @db_conn_wrap
    def delete(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "DB_conn_error", "DB was not provided or couldn't connect"
            )
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]

        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "No row chosen")
            return None

        selected_id = self.table.item(selected, 0).text()
        selected_name = self.table.item(selected, 1).text()
        if not selected_id.isdigit():
            QMessageBox.warning(self, "Warning", "You can`t delete this")
            return None
        load_dotenv()
        user_id = os.getenv("USER")
        cursor.execute("DELETE FROM tables WHERE tableid=%s", (selected_id,))
        cursor.execute(f"DROP TABLE `{selected_name}`")
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
        QMessageBox.warning(self, "Warning", "File should contain headers")
        path = QFileDialog.getOpenFileName(
            self, "Select file", "C:/"
        )[0]
        if not path:
            QMessageBox.critical(self, "File selection error", "No file was selected")
            return None
        if "/" in path:
            name = path.split("/")[-1]
        else:
            name = path.split("\\")[-1]
        load_dotenv()
        user_id = os.getenv("USER")
        name = f'{user_id}_{"_".join(name.split()).split(".")[0]}'

        try:
            excel_file = pd.ExcelFile(path)
            sheet1 = excel_file.parse(0)
        except ValueError:
            if path.split(".")[-1] == "csv":
                sheet1 = pd.read_csv(path)
            else:
                QMessageBox.critical(self, "File decoding error", "Wrong file type")
                return

        columns = list(sheet1.columns)
        db_request = f"CREATE TABLE `{name}` ( id INTEGER PRIMARY KEY AUTOINCREMENT,"
        for i in columns[:-1]:
            db_request += f"{i} TEXT, "
        db_request += f"{columns[-1]} TEXT)"
        try:
            cursor.execute(db_request)
        except mysql.connector.Error as err:
            QMessageBox.critical(
                self, "Table creation failed", f"Table already exists or error: {err}"
            )
            return None
        db_request = f"""INSERT INTO `{name}` ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in range(len(columns))])})"""
        cursor.executemany(db_request, sheet1.values.tolist())
        cursor.execute(
            "INSERT INTO tables (userid, table_name) VALUES (?, ?)", (user_id, name)
        )
        conn.commit()
        self.display_all_files()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CsvLayout()
    sys.excepthook = except_hook
    main_window.show()
    sys.exit(app.exec())
