import sys

import PyQt6.QtWidgets
from PyQt6.QtWidgets import QVBoxLayout


class MainWindow(PyQt6.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Statistics")

        self.main_layout = QVBoxLayout(self)
        self.select_file_layout = PyQt6.QtWidgets.QHBoxLayout(self)
        self.select_values_layout = PyQt6.QtWidgets.QHBoxLayout(self)

        self.files_combo_box = PyQt6.QtWidgets.QComboBox(self)
        self.refresh_btn = PyQt6.QtWidgets.QPushButton(parent=self, text="Refresh")

        self.plot_btn = PyQt6.QtWidgets.QPushButton(parent=self, text="Plot")

        self.label_box = PyQt6.QtWidgets.QComboBox(self)
        self.value_box = PyQt6.QtWidgets.QComboBox(self)
        self.refresh_boxes_btn = PyQt6.QtWidgets.QPushButton(
            parent=self, text="Refresh boxes"
        )

        self.select_file_layout.addWidget(PyQt6.QtWidgets.QLabel("Select file:"))
        self.select_file_layout.addWidget(self.files_combo_box)
        self.select_file_layout.addWidget(self.refresh_btn)

        self.select_values_layout.addWidget(PyQt6.QtWidgets.QLabel("Select value:"))
        self.select_values_layout.addWidget(self.value_box)
        self.select_values_layout.addWidget(PyQt6.QtWidgets.QLabel("Select labels:"))
        self.select_values_layout.addWidget(self.label_box)
        self.select_values_layout.addWidget(self.refresh_boxes_btn)

        self.main_layout.addLayout(self.select_file_layout)
        self.main_layout.addWidget(self.plot_btn)
        self.main_layout.addLayout(self.select_values_layout)


if __name__ == "__main__":
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
