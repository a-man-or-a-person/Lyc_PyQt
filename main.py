import sys

import PyQt6.QtWidgets

import Lyc_PyQt.UI.main_menu_ui
import Lyc_PyQt.DataBase.DB_implement
import Lyc_PyQt.Statistics.statistics


class MainMenu(Lyc_PyQt.UI.main_menu_ui.MainWindow):
    def __init__(self):
        super().__init__()
        self.downloaded_btn.clicked.connect(self.show_downloads)
        self.statistics_btn.clicked.connect(self.show_statistics)

    def show_downloads(self):
        self.downloads_window = Lyc_PyQt.DataBase.DB_implement.Table_work()
        self.downloads_window.show()

    def show_statistics(self):
        self.stats_window = Lyc_PyQt.Statistics.statistics.StatisticsWindow()
        self.stats_window.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
