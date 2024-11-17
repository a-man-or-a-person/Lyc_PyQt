import sys
import traceback
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QPushButton,
    QLabel,
    QComboBox,
    QTableWidget,
    QLineEdit,
    QMessageBox
)

import Lyc_PyQt.DataBase


def except_hook(cls, exception, tb):
    error_msg = ''.join(traceback.format_exception(cls, exception, tb))
    print("Unhandled exception:", error_msg)
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText("An unhandled exception occurred:")
    msg_box.setInformativeText(error_msg)
    msg_box.exec()


sys.excepthook = except_hook


class HomeView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Money and Statistics")
        layout = QVBoxLayout(self)

        header_text = QLabel("<h1>Welcome to Money & Statistics</h1>")
        header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_text = QLabel("<h3>Your tool for financial insights and data analysis</h3>")
        sub_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(header_text)
        layout.addWidget(sub_text)
        layout.addStretch()


class CsvViews(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Adding Exel_file")
        layout = QVBoxLayout(self)
        btn_layout1 = QHBoxLayout()
        btn_layout2 = QHBoxLayout()
        refresh_btn = QPushButton(parent=self, text="Refresh")
        add_csv_btn = QPushButton(parent=self, text="Add Exel(XLS) File")
        del_csv_btn = QPushButton(parent=self, text="Delete File")
        empty_btn = QPushButton(parent=self, text="Empty")
        table = QTableWidget(self)
        btn_layout1.addWidget(refresh_btn)
        btn_layout1.addWidget(empty_btn)
        btn_layout2.addWidget(add_csv_btn)
        btn_layout2.addWidget(del_csv_btn)
        layout.addLayout(btn_layout1)
        layout.addLayout(btn_layout2)
        layout.addWidget(table)


class StatisticsView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        select_file_layout = QHBoxLayout()
        select_values_layout = QHBoxLayout()
        select_plot_layout = QHBoxLayout()
        files_combo_box = QComboBox(self)
        refresh_btn = QPushButton(parent=self, text="Refresh")
        graphs_box = QComboBox(self)
        plot_btn = QPushButton(parent=self, text="Plot")
        label_box = QComboBox(self)
        value_box = QComboBox(self)
        refresh_boxes_btn = QPushButton(parent=self, text="Refresh boxes")
        select_file_layout.addWidget(QLabel("Select file:"))
        select_file_layout.addWidget(files_combo_box)
        select_file_layout.addWidget(refresh_btn)
        select_plot_layout.addWidget(QLabel("Select graph:"))
        select_plot_layout.addWidget(graphs_box)
        select_plot_layout.addWidget(plot_btn)
        select_values_layout.addWidget(QLabel("Select value:"))
        select_values_layout.addWidget(value_box)
        select_values_layout.addWidget(QLabel("Select labels:"))
        select_values_layout.addWidget(label_box)
        select_values_layout.addWidget(refresh_boxes_btn)
        layout.addLayout(select_file_layout)
        layout.addLayout(select_plot_layout)
        layout.addLayout(select_values_layout)


class TableWork(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Work With Selected File")
        layout = QVBoxLayout(self)
        select_file_layout = QHBoxLayout()
        btns_layout = QHBoxLayout(self)
        btns_layout2 = QHBoxLayout(self)
        files_combo_box = QComboBox(self)
        refresh_btn = QPushButton(parent=self, text="Refresh")
        delete_btn = QPushButton(parent=self, text="Delete")
        add_exel_file_btn = QPushButton(parent=self, text="Add exel file")
        select_btn = QPushButton(parent=self, text="Select")
        table = QTableWidget(self)
        select_file_layout.addWidget(QLabel("Select file:"))
        select_file_layout.addWidget(files_combo_box)
        select_file_layout.addWidget(refresh_btn)
        btns_layout2.addWidget(select_btn)
        btns_layout2.addWidget(add_exel_file_btn)
        btns_layout.addWidget(delete_btn)
        layout.addLayout(select_file_layout)
        layout.addLayout(btns_layout2)
        layout.addLayout(btns_layout)
        layout.addWidget(table)


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Main Application")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.nav_buttons = QHBoxLayout()
        self.layout.addLayout(self.nav_buttons)

        self.home_btn = QPushButton("Home")
        self.csv_btn = QPushButton("CSV Views")
        self.stats_btn = QPushButton("Statistics")
        self.table_btn = QPushButton("Table Work")

        self.nav_buttons.addWidget(self.home_btn)
        self.nav_buttons.addWidget(self.csv_btn)
        self.nav_buttons.addWidget(self.table_btn)
        self.nav_buttons.addWidget(self.stats_btn)

        self.home_btn.clicked.connect(self.show_home)
        self.csv_btn.clicked.connect(self.show_csv)
        self.stats_btn.clicked.connect(self.show_stats)
        self.table_btn.clicked.connect(self.show_table)

        self.home_view = HomeView()
        self.csv_view = CsvViews()
        self.stats_view = StatisticsView()
        self.table_view = TableWork()

        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.addWidget(self.csv_view)
        self.stacked_widget.addWidget(self.table_view)
        self.stacked_widget.addWidget(self.stats_view)

    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.home_view)

    def show_csv(self):
        self.stacked_widget.setCurrentWidget(self.csv_view)

    def show_stats(self):
        self.stacked_widget.setCurrentWidget(self.stats_view)

    def show_table(self):
        self.stacked_widget.setCurrentWidget(self.table_view)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout(self)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.check_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "admin" and password == "password":
            self.accepted_login.emit()
        else:
            self.username_input.clear()
            self.password_input.clear()


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow()
        self.main_window = MainApplication()

        self.login_window.login_btn.clicked.connect(self.show_main_window)

        self.login_window.show()

        sys.exit(self.app.exec())

    def show_main_window(self):
        self.login_window.close()
        self.main_window.show()


if __name__ == "__main__":
    AppController()
