import PyQt6.QtWidgets as QT


class TableWork(QT.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Work With Selected File")
        layout = QT.QVBoxLayout(self)
        select_file_layout = QT.QHBoxLayout()
        btns_layout = QT.QHBoxLayout(self)
        btns_layout2 = QT.QHBoxLayout(self)
        self.files_combo_box = QT.QComboBox(self)
        self.refresh_btn = QT.QPushButton(parent=self, text="Refresh")
        self.delete_btn = QT.QPushButton(parent=self, text="Delete")
        self.select_btn = QT.QPushButton(parent=self, text="Select")
        self.table = QT.QTableWidget(self)
        select_file_layout.addWidget(QT.QLabel("Select file:"))
        select_file_layout.addWidget(self.files_combo_box)
        select_file_layout.addWidget(self.refresh_btn)
        btns_layout2.addWidget(self.select_btn)
        btns_layout.addWidget(self.delete_btn)
        layout.addLayout(select_file_layout)
        layout.addLayout(btns_layout2)
        layout.addLayout(btns_layout)
        layout.addWidget(self.table)
