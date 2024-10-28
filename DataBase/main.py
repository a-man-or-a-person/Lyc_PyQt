import sys

import PyQt6.QtWidgets

import Lyc_PyQt.UI.main_menu_ui
import Lyc_PyQt.DataBase.DB_implement


class MainMenu(Lyc_PyQt.UI.main_menu_ui.MainWindow):
    def __init__(self):
        super().__init__()
        self.downloaded_btn.clicked.connect(self.show_downloads)

    def show_downloads(self):
        self.downloads_window = Lyc_PyQt.DataBase.DB_implement.Table_work()
        self.downloads_window.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
