import sys

import PyQt6.QtWidgets

import Lyc_PyQt.UI.work_with_data_ui
from Lyc_PyQt.DataBase.decorators import db_conn_wrap
import Lyc_PyQt.UI.main_menu_ui


class Table_work(Lyc_PyQt.UI.work_with_data_ui.TableWork):
    def __init__(self):
        super().__init__()
        self.add_btn.clicked.connect(self.get_all_items)
        self.delete_btn.clicked.connect(self.open_new_window)

    def open_new_window(self):
        self.main_window = Lyc_PyQt.UI.main_menu_ui.MainWindow()
        self.main_window.show()

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

        table = 'test_data'
        a = f'SELECT * FROM {table}'
        data = cursor.execute(a).fetchall()
        self.table.setRowCount(0)
        if data:
            self.table.setColumnCount(len(data[0]))
            self.table.setHorizontalHeaderLabels(self.get_column_names('test_data'))
            for row, line in enumerate(data):
                self.table.insertRow(row)
                for pos, info in enumerate(line):
                    self.table.setItem(row, pos, PyQt6.QtWidgets.QTableWidgetItem(str(info)))

    def add(self):
        print(self.category_combo_box.currentText())

    @db_conn_wrap
    def delete(self, *args, **kwargs):
        if not ('conn' in kwargs or 'cursor' in kwargs):
            raise ValueError('No connection to db had been provided')
        conn = kwargs['conn']
        cursor = kwargs['cursor']

        table = 'test_data'
        if 'table' in kwargs:
            table = kwargs['table']

        selected = self.table.currentRow()
        if selected == -1:
            PyQt6.QtWidgets.QMessageBox.warning(self, 'Warning', "No row chosen")
            return None

        selected_id = self.table.item(selected, 0).text()
        request = f'DELETE FROM {table} WHERE id = ?'
        # print(selected_id, 'selected_id')
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
