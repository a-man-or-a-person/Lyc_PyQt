import sys
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import PyQt6.QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

import Lyc_PyQt.UI.statistics_ui
from Lyc_PyQt.DataBase.decorators import db_conn_wrap

matplotlib.use('QtAgg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class StatisticsWindow(Lyc_PyQt.UI.statistics_ui.MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_btn.clicked.connect(self.combo_box)
        self.plot_btn.clicked.connect(self.update_pie_graph)
        self.combo_box()

        # self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        #
        # toolbar = NavigationToolbar2QT(self.sc, self)
        #
        # layout = PyQt6.QtWidgets.QVBoxLayout()
        # layout.addWidget(toolbar)
        # layout.addWidget(self.sc)
        #
        # self.main_layout.addLayout(layout)
        #
        # widget = PyQt6.QtWidgets.QWidget()
        # widget.setLayout(self.main_layout)
        # self.setCentralWidget(widget)
        self.figure = plt.figure(figsize=(6, 15))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.main_layout.addWidget(self.canvas)


    @db_conn_wrap
    def update_pie_graph(self, *args, **kwargs):
        if not ('conn' in kwargs or 'cursor' in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(self, 'DB_conn_error', "DB was not provided or couldn't connect")
        conn = kwargs['conn']
        cursor = kwargs['cursor']

        self.figure.clear()
        self.ax = self.figure.subplots()

        selected_table = self.files_combo_box.currentText()
        df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)

        self.ax.pie(df['price'], labels=df['name'])
        self.canvas.draw()

    @db_conn_wrap
    def combo_box(self, *args, **kwargs):
        if not ('conn' in kwargs or 'cursor' in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(self, 'DB_conn_error', "DB was not provided or couldn't connect")
        conn = kwargs['conn']
        cursor = kwargs['cursor']
        cursor.execute('''CREATE TABLE IF NOT EXISTS csv_files (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE
                    )''')
        self.files_combo_box.clear()
        tables = cursor.execute("SELECT * FROM csv_files").fetchall()
        if tables:
            self.files_combo_box.addItems([x[1] for x in tables])
        conn.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = StatisticsWindow()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
