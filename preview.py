from PySide6.QtWidgets import (QHBoxLayout, QLabel, QDialog)
from PySide6.QtGui import QImage, QPixmap

import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class FigurePreview(QDialog):
    def __init__(self, figure):
        super().__init__()

        canvas = FigureCanvas(figure)
        canvas.draw()
        width, height = figure.canvas.get_width_height()
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
