
import sys
import pandas as pd
import mysql.connector

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
import Lyc_PyQt.UI.csv_ui
import Lyc_PyQt.db_connection



class CsvLayout(Lyc_PyQt.UI.csv_ui.CsvViews):
    def __init__(self):
        super().__init__()
        self.connection = Lyc_PyQt.db_connection.connect_db()
        self.cur = self.connection.cursor()
        self.refresh_btn.clicked.connect(self.display_all_files)
        self.add_csv_btn.clicked.connect(self.add_csv)
        self.del_csv_btn.clicked.connect(self.delete)

    def display_all_files(self, *args, **kwargs):
        cursor = self.cur
        cursor.execute("SELECT * FROM LicPyqt.csv_files")
        data = cursor.fetchall()
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["id", "filename"])
        if data:
            for row, line in enumerate(data):
                self.table.insertRow(row)
                for pos, info in enumerate(line):
                    self.table.setItem(row, pos, QTableWidgetItem(str(info)))
        else:
            self.table.insertRow(0)
            for pos, info in enumerate(["no", "files"]):
                self.table.setItem(0, pos, QTableWidgetItem(str(info)))

    def delete(self, *args, **kwargs):
        cursor = self.cur

        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "No row chosen")
            return None

        selected_id = self.table.item(selected, 0).text()
        selected_name = self.table.item(selected, 1).text()
        if not selected_id.isdigit():
            QMessageBox.warning(self, "Warning", "You can`t delete this")
            return None
        cursor.execute("DELETE FROM LicPyqt.csv_files WHERE name=%s", (selected_name,))
        cursor.execute(f"DROP TABLE `{selected_name}`")
        self.connection.commit()
        self.display_all_files()

    def add_csv(self, *args, **kwargs):
        cursor = self.cur

        QMessageBox.warning(self, "Warning", "File should contain headers")
        path = QFileDialog.getOpenFileName(
            self, "Select file", "C:/", "Excel (*.xlsx, *xls, *csv);; Все файлы (*)"
        )[0]
        if not path:
            QMessageBox.critical(self, "File selection error", "No file was selected")
            return None
        print(path)
        if "/" in path:
            name = path.split("/")[-1]
        else:
            name = path.split("\\")[-1]
        name = "_".join(name.split()).split(".")[0]
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
        db_request = f"CREATE TABLE `{name}` ( id INT PRIMARY KEY AUTO_INCREMENT,"
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
        db_request = f"""INSERT INTO `{name}` ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in range(len(columns))])})"""
        cursor.executemany(db_request, sheet1.values.tolist())
        cursor.execute("INSERT INTO csv_files (name) VALUES (%s)", (name,))
        self.connection.commit()
        self.display_all_files()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CsvLayout()
    sys.excepthook = except_hook
    main_window.show()
    sys.exit(app.exec())
