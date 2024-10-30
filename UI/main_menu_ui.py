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
        self.buttons_layout = QGridLayout(self)

        self.header_text = QT.QLabel('Welcome to our application!')

        self.statistics_btn = QT.QPushButton('Статистика')
        self.downloaded_btn = QT.QPushButton('Загруженные данные')
        self.button3 = QT.QPushButton('Аналитика')
        self.button4 = QT.QPushButton('Экспорт данных')

        self.buttons_layout.addWidget(self.statistics_btn, 0, 0)
        self.buttons_layout.addWidget(self.downloaded_btn, 0, 1)
        self.buttons_layout.addWidget(self.button3, 1, 0)
        self.buttons_layout.addWidget(self.button4, 1, 1)

        self.main_layout.addWidget(self.header_text)
        self.main_layout.addLayout(self.buttons_layout)


if __name__ == '__main__':
    app = QT.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())