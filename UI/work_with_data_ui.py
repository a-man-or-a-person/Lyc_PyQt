import sys

import PyQt6.QtWidgets


class TableWork(PyQt6.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Work With Selected File')

        self.main_layout = PyQt6.QtWidgets.QVBoxLayout(self)

        self.select_file_layout = PyQt6.QtWidgets.QHBoxLayout(self)

        self.btns_layout = PyQt6.QtWidgets.QHBoxLayout(self)
        self.btns_layout2 = PyQt6.QtWidgets.QHBoxLayout(self)

        self.files_combo_box = PyQt6.QtWidgets.QComboBox(self)

        self.refresh_btn = PyQt6.QtWidgets.QPushButton(parent=self, text='Refresh')
        self.delete_btn = PyQt6.QtWidgets.QPushButton(parent=self, text='Delete')

        self.add_exel_file_btn = PyQt6.QtWidgets.QPushButton(parent=self, text='Add exel file')
        self.select_btn = PyQt6.QtWidgets.QPushButton(parent=self, text='Select')

        self.table = PyQt6.QtWidgets.QTableWidget(self)

        self.select_file_layout.addWidget(PyQt6.QtWidgets.QLabel('Select file:'))
        self.select_file_layout.addWidget(self.files_combo_box)
        self.select_file_layout.addWidget(self.refresh_btn)



        self.btns_layout2.addWidget(self.select_btn)
        self.btns_layout2.addWidget(self.add_exel_file_btn)

        self.btns_layout.addWidget(self.delete_btn)

        self.main_layout.addLayout(self.select_file_layout)
        self.main_layout.addLayout(self.btns_layout2)
        self.main_layout.addLayout(self.btns_layout)
        self.main_layout.addWidget(self.table)


if __name__ == '__main__':
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = TableWork()
    window.show()
    sys.exit(app.exec())
