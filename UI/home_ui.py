import PyQt6.QtWidgets as QT
from PyQt6.QtCore import Qt


class HomeView(QT.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Money and Statistics")
        layout = QT.QVBoxLayout(self)

        header_text = QT.QLabel("<h1>Welcome to Money & Statistics</h1>")
        header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_text = QT.QLabel(
            "<h3>Your tool for financial insights and data analysis</h3>"
        )
        sub_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(header_text)
        layout.addWidget(sub_text)
        layout.addStretch()
