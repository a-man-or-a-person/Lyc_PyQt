import sys

import PyQt6.QtWidgets as QT
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout


class MainWindow(QT.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Welcome Page')

        self.main_layout = QVBoxLayout(self)
        self.buttons_layout = QHBoxLayout(self)

        self.header_text = QT.QLabel(text='Welcome to our application!')

        self.statistics_btn = QT.QPushButton('Статистика')
        self.downloaded_btn = QT.QPushButton('Загруженные данные')

        self.buttons_layout.addWidget(self.statistics_btn)
        self.buttons_layout.addWidget(self.downloaded_btn)

        self.main_layout.addWidget(self.header_text)
        self.main_layout.addLayout(self.buttons_layout)


if __name__ == '__main__':
    app = QT.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())