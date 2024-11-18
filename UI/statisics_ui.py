import PyQt6.QtWidgets as QT


class StatisticsView(QT.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QT.QVBoxLayout(self)
        select_file_layout = QT.QHBoxLayout()
        select_values_layout = QT.QHBoxLayout()
        select_plot_layout = QT.QHBoxLayout()
        self.files_combo_box = QT.QComboBox(self)
        self.refresh_btn = QT.QPushButton(parent=self, text="Refresh")
        self.graphs_box = QT.QComboBox(self)
        self.plot_btn = QT.QPushButton(parent=self, text="Plot")
        self.label_box = QT.QComboBox(self)
        self.value_box = QT.QComboBox(self)
        self.refresh_boxes_btn = QT.QPushButton(parent=self, text="Refresh boxes")
        select_file_layout.addWidget(QT.QLabel("Select file:"))
        select_file_layout.addWidget(self.files_combo_box)
        select_file_layout.addWidget(self.refresh_btn)
        select_plot_layout.addWidget(QT.QLabel("Select graph:"))
        select_plot_layout.addWidget(self.graphs_box)
        select_plot_layout.addWidget(self.plot_btn)
        select_values_layout.addWidget(QT.QLabel("Select value:"))
        select_values_layout.addWidget(self.value_box)
        select_values_layout.addWidget(QT.QLabel("Select labels:"))
        select_values_layout.addWidget(self.label_box)
        select_values_layout.addWidget(self.refresh_boxes_btn)
        self.layout.addLayout(select_file_layout)
        self.layout.addLayout(select_plot_layout)
        self.layout.addLayout(select_values_layout)
