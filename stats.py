import sys
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QLabel,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import Lyc_PyQt.db_connection
from Lyc_PyQt.UI.statisics_ui import StatisticsView

matplotlib.use("QtAgg")


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class StatisticsWindow(StatisticsView):
    def __init__(self):
        super().__init__()
        self.graphs_box.addItems(["pie", "hist"])

        self.refresh_btn.clicked.connect(self.combo_box)
        self.plot_btn.clicked.connect(self.update_graph)
        self.refresh_boxes_btn.clicked.connect(self.refresh_boxes)

        self.conn = Lyc_PyQt.db_connection.connect_db()
        self.cur = self.conn.cursor()

        # Add canvas for plotting
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout.addWidget(self.canvas)

    def refresh_boxes(self, *args, **kwargs):
        conn = self.conn
        cursor = self.cur

        self.value_box.clear()
        self.label_box.clear()

        selected_table = self.files_combo_box.currentText()
        df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
        cols = df.columns
        vals = df.iloc[0]
        for val, col in zip(vals, cols):
            self.label_box.addItem(col)
            self.value_box.addItem(col)
            # Values can also be integers ----------- !!!!!!!!!!!!!!!!!!!!
            # try:
            #     float(val)
            #     self.value_box.addItem(col)
            # except ValueError:
            #     self.label_box.addItem(col)
            # except TypeError:
            #     pass

    def update_graph(self, *args, **kwargs):
        conn = self.conn
        cursor = self.cur

        self.canvas.axes.cla()

        selected_table = self.files_combo_box.currentText()
        df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)

        value = self.value_box.currentText()
        label = self.label_box.currentText()

        selected_graph = self.graphs_box.currentText()
        if selected_graph == "hist":
            sns.histplot(
                data=df, x=value, hue=label, multiple="stack", ax=self.canvas.axes
            )
        elif selected_graph == "pie":
            self.canvas.axes.pie(
                df[value], labels=df[label], colors=sns.color_palette("dark")
            )
        else:
            return
        self.canvas.draw()

    def combo_box(self, *args, **kwargs):
        conn = self.conn
        cursor = self.cur
        self.files_combo_box.clear()
        cursor.execute("SELECT * FROM csv_files")
        tables = cursor.fetchall()
        if tables:
            self.files_combo_box.addItems([x[1] for x in tables])
        conn.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StatisticsWindow()
    window.show()
    sys.exit(app.exec())
