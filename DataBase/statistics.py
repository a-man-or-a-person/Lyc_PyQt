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


class StatisticsWindow(Lyc_PyQt.UI.statistics_ui.MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.refresh_btn.clicked.connect(self.combo_box)
        self.plot_btn.clicked.connect(self.update_pie_graph)
        self.combo_box()
        self.figure = plt.figure(figsize=(6, 15))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.main_layout.addWidget(self.canvas)
        self.refresh_boxes_btn.clicked.connect(self.refresh_boxes)
        self.refresh_boxes()

    @db_conn_wrap
    def refresh_boxes(self, *args, **kwargs):
        if not ('conn' in kwargs or 'cursor' in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(self, 'DB_conn_error', "DB was not provided or couldn't connect")
        conn = kwargs['conn']
        cursor = kwargs['cursor']

        self.value_box.clear()
        self.label_box.clear()

        selected_table = self.files_combo_box.currentText()
        df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
        cols = df.columns
        vals = df.iloc[0]
        for val, col in zip(vals, cols):
            try:
                int(val)
                self.value_box.addItem(col)
            except ValueError:
                self.label_box.addItem(col)

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

        value = self.value_box.currentText()
        label = self.label_box.currentText()
        self.ax.pie(df[value], labels=df[label])
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
