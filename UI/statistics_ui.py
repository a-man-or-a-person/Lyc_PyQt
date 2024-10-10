import sys

import PyQt6.QtWidgets as QT
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout


class MainWindow(QT.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Statistics')

        self.main_layout = QVBoxLayout(self)
        self.combo_box_layout = QHBoxLayout(self)

        self.label = QT.QLabel('Select some options:')

        self.combo_box1 = QT.QComboBox(self)
        self.combo_box2 = QT.QComboBox(self)
        self.combo_box3 = QT.QComboBox(self)

        self.view_stats = QT.QTextBrowser(self)

        self.combo_box_layout.addWidget(self.combo_box1)
        self.combo_box_layout.addWidget(self.combo_box2)
        self.combo_box_layout.addWidget(self.combo_box3)

        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.combo_box_layout)
        self.main_layout.addWidget(self.view_stats)


if __name__ == '__main__':
    app = QT.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())