import sys

import PyQt6.QtWidgets


import Lyc_PyQt.DataBase.work_with_csv
import Lyc_PyQt.db_connection
import Lyc_PyQt.UI.Tabel_work_ui


class Table_work(Lyc_PyQt.UI.Tabel_work_ui.TableWork):
    def __init__(self):
        super().__init__()
        self.refresh_btn.clicked.connect(self.combo_box)
        self.select_btn.clicked.connect(self.get_all_items)
        self.delete_btn.clicked.connect(self.delete)
        self.add_exel_file_btn.clicked.connect(self.add_exel_file)
        self.conn = Lyc_PyQt.db_connection.connect_db()
        self.cur = self.conn.cursor()
        self.combo_box()

    def combo_box(self, *args, **kwargs):
        conn = self.conn
        cursor = self.cur
        print('start')
        self.files_combo_box.clear()
        cursor.execute("SELECT * FROM csv_files")
        tables = cursor.fetchall()
        if tables:
            self.files_combo_box.addItems([x[1] for x in tables])
        conn.commit()

    def add_exel_file(self):
        self.add_exel_window = Lyc_PyQt.DataBase.work_with_csv.CsvLayout()
        self.add_exel_window.show()

    def get_column_names(self, table="test_data", **kwargs):
        conn = self.conn
        cursor = self.cur
        a = "SELECT * FROM {0} LIMIT 1".format(table)
        cursor.execute(a)
        res = [x[0] for x in cursor.description]
        cursor.fetchall()
        return res

    def get_all_items(self, *args, **kwargs):
        conn = self.conn
        cursor = self.cur
        table = self.files_combo_box.currentText()
        a = f"SELECT * FROM {table}"
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

    def delete(self, *args, **kwargs):
        conn = self.conn
        cursor = self.cur

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
