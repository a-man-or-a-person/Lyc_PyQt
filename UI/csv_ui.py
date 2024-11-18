import PyQt6.QtWidgets as QT


class CsvViews(QT.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Adding Exel_file")
        layout = QT.QVBoxLayout(self)
        btn_layout1 = QT.QHBoxLayout()
        btn_layout2 = QT.QHBoxLayout()
        self.refresh_btn = QT.QPushButton(parent=self, text="Refresh")
        self.add_csv_btn = QT.QPushButton(parent=self, text="Add Exel(XLS) File")
        self.del_csv_btn = QT.QPushButton(parent=self, text="Delete File")
        self.empty_btn = QT.QPushButton(parent=self, text="Empty")
        self.table = QT.QTableWidget(self)
        btn_layout1.addWidget(self.refresh_btn)
        btn_layout1.addWidget(self.empty_btn)
        btn_layout2.addWidget(self.add_csv_btn)
        btn_layout2.addWidget(self.del_csv_btn)
        layout.addLayout(btn_layout1)
        layout.addLayout(btn_layout2)
        layout.addWidget(self.table)
