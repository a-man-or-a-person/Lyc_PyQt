import sys

import PyQt6.QtWidgets

import Lyc_PyQt.UI.work_with_data_ui
from Lyc_PyQt.DataBase.decorators import db_conn_wrap
import Lyc_PyQt.UI.main_menu_ui
import Lyc_PyQt.DataBase.work_with_csv


class Table_work(Lyc_PyQt.UI.work_with_data_ui.TableWork):
    def __init__(self):
        super().__init__()
        self.refresh_btn.clicked.connect(self.combo_box)
        self.select_btn.clicked.connect(self.get_all_items)
        self.delete_btn.clicked.connect(self.delete)
        self.add_exel_file_btn.clicked.connect(self.add_exel_file)
        self.combo_box()
        # self.files_combo_box.toggled.connect(self.combo_box)


    @db_conn_wrap
    def combo_box(self, *args, **kwargs):
        if not ('conn' in kwargs or 'cursor' in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(self, 'DB_conn_error', "DB was not provided or couldn't connect")
        conn = kwargs['conn']
        cursor = kwargs['cursor']
        self.files_combo_box.clear()
        self.files_combo_box.addItems([x[1] for x in cursor.execute("SELECT * FROM csv_files").fetchall()])

    def add_exel_file(self):
        self.add_exel_window = Lyc_PyQt.DataBase.work_with_csv.CsvLayout()
        self.add_exel_window.show()

    @db_conn_wrap
    def get_column_names(self, table='test_data', **kwargs):
        if not ('conn' in kwargs or 'cursor' in kwargs):
            raise ValueError('No connection to db had been provided')
        conn = kwargs['conn']
        cursor = kwargs['cursor']

        a = 'SELECT * FROM {0} LIMIT 1'.format(table)
        res = [x[0] for x in cursor.execute(a).description]
        return res

    @db_conn_wrap
    def get_all_items(self, *args, **kwargs):
        if not ('conn' in kwargs or 'cursor' in kwargs):
            raise ValueError('No connection to db had been provided')
        conn = kwargs['conn']
        cursor = kwargs['cursor']

        table = self.files_combo_box.currentText()
        a = f'SELECT * FROM {table}'
        data = cursor.execute(a).fetchall()
        self.table.setRowCount(0)
        if data:
            self.table.setColumnCount(len(data[0]))
            self.table.setHorizontalHeaderLabels(self.get_column_names(table))
            for row, line in enumerate(data):
                self.table.insertRow(row)
                for pos, info in enumerate(line):
                    self.table.setItem(row, pos, PyQt6.QtWidgets.QTableWidgetItem(str(info)))


    @db_conn_wrap
    def delete(self, *args, **kwargs):
        if not ('conn' in kwargs or 'cursor' in kwargs):
            raise ValueError('No connection to db had been provided')
        conn = kwargs['conn']
        cursor = kwargs['cursor']

        table = self.files_combo_box.currentText()
        if 'table' in kwargs:
            table = kwargs['table']

        selected = self.table.currentRow()
        if selected == -1:
            PyQt6.QtWidgets.QMessageBox.warning(self, 'Warning', "No row chosen")
            return None

        selected_id = self.table.item(selected, 0).text()
        request = f'DELETE FROM {table} WHERE id = ?'
        cursor.execute(request, [selected_id])
        conn.commit()
        self.get_all_items()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = Table_work()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
