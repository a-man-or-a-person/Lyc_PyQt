import sys

import PyQt6.QtWidgets


class TableWork(PyQt6.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Work With DB')

        self.main_layout = PyQt6.QtWidgets.QVBoxLayout(self)

        self.date_and_category_layout = PyQt6.QtWidgets.QHBoxLayout(self)
        self.amount_and_description_layout = PyQt6.QtWidgets.QHBoxLayout(self)
        self.btns_layout = PyQt6.QtWidgets.QHBoxLayout(self)

        self.date_edit = PyQt6.QtWidgets.QDateEdit(self)

        self.category_combo_box = PyQt6.QtWidgets.QComboBox(self)

        self.amount_edit = PyQt6.QtWidgets.QLineEdit(self)

        self.description_edit = PyQt6.QtWidgets.QLineEdit(self)

        self.add_btn = PyQt6.QtWidgets.QPushButton(parent=self, text='Add')
        self.delete_btn = PyQt6.QtWidgets.QPushButton(parent=self, text='Delete')

        self.table = PyQt6.QtWidgets.QTableWidget(self)
        # self.table.setColumnCount(5)
        # self.table.setHorizontalHeaderLabels(['id', 'date', 'category', 'amount', 'description'])

        self.date_and_category_layout.addWidget(PyQt6.QtWidgets.QLabel('Date:'))
        self.date_and_category_layout.addWidget(self.date_edit)
        self.date_and_category_layout.addWidget(PyQt6.QtWidgets.QLabel('Category:'))
        self.date_and_category_layout.addWidget(self.category_combo_box)

        self.amount_and_description_layout.addWidget(PyQt6.QtWidgets.QLabel('Amount:'))
        self.amount_and_description_layout.addWidget(self.amount_edit)
        self.amount_and_description_layout.addWidget(PyQt6.QtWidgets.QLabel('Description:'))
        self.amount_and_description_layout.addWidget(self.description_edit)

        self.btns_layout.addWidget(self.add_btn)
        self.btns_layout.addWidget(self.delete_btn)

        self.main_layout.addLayout(self.date_and_category_layout)
        self.main_layout.addLayout(self.amount_and_description_layout)
        self.main_layout.addLayout(self.btns_layout)
        self.main_layout.addWidget(self.table)


if __name__ == '__main__':
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = TableWork()
    window.show()
    sys.exit(app.exec())
