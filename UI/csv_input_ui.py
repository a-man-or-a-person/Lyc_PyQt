import sys

import PyQt6.QtWidgets


class CsvViews(PyQt6.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Adding Exel_file")

        self.main_layout = PyQt6.QtWidgets.QVBoxLayout(self)
        self.btn_layout1 = PyQt6.QtWidgets.QHBoxLayout(self)
        self.btn_layout2 = PyQt6.QtWidgets.QHBoxLayout(self)

        self.refresh_btn = PyQt6.QtWidgets.QPushButton(parent=self, text="Refresh")
        self.add_csv_btn = PyQt6.QtWidgets.QPushButton(
            parent=self, text="Add Exel(XLS) File"
        )
        self.del_csv_btn = PyQt6.QtWidgets.QPushButton(parent=self, text="Delete File")
        self.empty_btn = PyQt6.QtWidgets.QPushButton(parent=self, text="Empty")

        self.table = PyQt6.QtWidgets.QTableWidget(self)

        self.btn_layout1.addWidget(self.refresh_btn)
        self.btn_layout1.addWidget(self.empty_btn)
        self.btn_layout2.addWidget(self.add_csv_btn)
        self.btn_layout2.addWidget(self.del_csv_btn)
        self.main_layout.addLayout(self.btn_layout1)
        self.main_layout.addLayout(self.btn_layout2)
        self.main_layout.addWidget(self.table)


if __name__ == "__main__":
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = CsvViews()
    window.show()
    sys.exit(app.exec())
