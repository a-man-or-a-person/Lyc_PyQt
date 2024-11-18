import os

import Lyc_PyQt.DataBase.work_with_csv
import Lyc_PyQt.DataBase.DB_implement
import Lyc_PyQt.UI.home_ui
import Lyc_PyQt.stats
import Lyc_PyQt.login

import PyQt6.QtWidgets as QT
import sys
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
    QMessageBox,
)


class HomeView(Lyc_PyQt.UI.home_ui.HomeView):
    def __init__(self):
        super().__init__()


class CsvViews(Lyc_PyQt.DataBase.work_with_csv.CsvLayout):
    def __init__(self):
        super().__init__()


class TableWork(Lyc_PyQt.DataBase.DB_implement.Table_work):
    def __init__(self):
        super().__init__()


class StatisticsView(Lyc_PyQt.stats.StatisticsWindow):
    def __init__(self):
        super().__init__()


class MainApplication(QT.QMainWindow):
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


class LoginWindow(Lyc_PyQt.login.Login):
    def __init__(self):
        super().__init__()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


sys.excepthook = except_hook


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = Lyc_PyQt.login.Login(self)
        self.main_window = MainApplication()

        self.login_window.show()

        sys.exit(self.app.exec())

    def show_main_window(self):
        self.login_window.close()
        self.main_window.show()
        print(os.getenv("USER"))


if __name__ == "__main__":
    AppController()
