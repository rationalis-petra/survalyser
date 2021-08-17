from PySide6.QtWidgets import (QHBoxLayout, QLabel, QDialog, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QPushButton,
                               QAbstractScrollArea)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class FigurePreview(QDialog):
    def __init__(self, figure):
        super().__init__()

        canvas = FigureCanvas(figure)
        canvas.draw()
        width, height = canvas.get_width_height()
        # we need to rearrange the rgb values slightly so that Qt interprets
        # the image correctly
        buf = (np.asarray(canvas.buffer_rgba())
               .take([2, 1, 0, 3], axis=2)
               .tobytes())
        img = QImage(buf,
                     width,
                     height,
                     QImage.Format_ARGB32)

        self.layout = QHBoxLayout()
        self.lbl = QLabel()
        self.lbl.setPixmap(QPixmap.fromImage(img))
        self.layout.addWidget(self.lbl)
        self.setLayout(self.layout)


class CoxPreview(QDialog):
    def __init__(self, model):
        super().__init__()

        # figure = model.plot().get_figure()

        # canvas = FigureCanvas(figure)
        # canvas.draw()
        # width, height = canvas.get_width_height()

        # buf = (np.asarray(canvas.buffer_rgba())
        #        .take([2, 1, 0, 3], axis=2)
        #        .tobytes())
        # img = QImage(buf,
        #              width,
        #              height,
        #              QImage.Format_ARGB32)

        self.layout = QVBoxLayout()

        self.title_label = QLabel("<font color=darkblue size = 20>Cox Summary")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        dataframe = model.summary

        dataframe = dataframe[['exp(coef)', 'coef lower 95%',
                               'coef upper 95%', 'p']]
        dataframe.columns = ['hazard ratio', 'hazard lower 95%',
                             'hazard upper 95%', 'p']

        dims = dataframe.shape
        self.table.setRowCount(dims[0])
        self.table.setColumnCount(dims[1])
        self.table.setHorizontalHeaderLabels(dataframe.columns)
        self.table.setVerticalHeaderLabels(dataframe.index.values)

        for row in range(0, dims[0]):
            for col in range(0, dims[1]):
                item = QTableWidgetItem()
                item.setText(str(dataframe.loc[dataframe.index[row],
                                               dataframe.columns[col]]))
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        question_lbl = QLabel("What would you like to do?")
        self.layout.addWidget(question_lbl)

        save_summary = QPushButton("Save Summary")
        save_summary.clicked.connect(self.save_summary)
        self.layout.addWidget(save_summary)

        plot_factor = QPushButton("Plot a factor")
        plot_factor.clicked.connect(self.plot_factor)
        self.layout.addWidget(plot_factor)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.reject)
        self.layout.addWidget(exit_btn)

        self.setLayout(self.layout)

    def save_summary():
        print("saving summary...")

    def plot_factor():
        print("plotting factor...")
