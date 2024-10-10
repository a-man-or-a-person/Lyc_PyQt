import sys

import PyQt6.QtWidgets as QT
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout


class MainWindow(QT.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Upload Data')

        self.main_layout = QVBoxLayout(self)
        self.load_layout = QHBoxLayout(self)

        self.label = QT.QLabel('Select path to file:')

        self.path_txt = QT.QLineEdit(self)
        self.upload_button = QT.QPushButton('Upload')

        self.lable2 = QT.QLabel('Uploaded files:')
        self.view_stats = QT.QTextBrowser(self)

        self.load_layout.addWidget(self.path_txt)
        self.load_layout.addWidget(self.upload_button)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.load_layout)
        self.main_layout.addWidget(self.lable2)
        self.main_layout.addWidget(self.view_stats)


if __name__ == '__main__':
    app = QT.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())