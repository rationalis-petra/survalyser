from PySide6.QtWidgets import (QHBoxLayout, QLabel, QDialog, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QPushButton,
                               QAbstractScrollArea, QWidget, QFormLayout,
                               QLineEdit, QCheckBox, QSizePolicy, QFileDialog,
                               QTabWidget, QFileDialog)
from PySide6.QtGui import QImage, QPixmap, QRegularExpressionValidator
from PySide6.QtCore import Qt

from lifelines.statistics import logrank_test
import numpy as np
import pandas as pd
# import pandas as pd

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class KaplanPreview(QDialog):
    def __init__(self, model):
        super().__init__()
        self.accepted.connect(self.close)
        self.rejected.connect(self.close)

        self.model = model
        self.title = ""
        self.xlim = 0
        self.show_conf = False
        self.figure = None

        self.layout = QHBoxLayout()
        self.lbl = QLabel()
        self.pval_lbl = QLabel()

        self.form = QWidget()
        self.form_layout = QFormLayout(self.form)

        self.title_box = QLineEdit()
        self.title_box.setMinimumWidth(200)

        self.xlim_box = QLineEdit()
        self.xlim_box.setValidator(QRegularExpressionValidator("[0-9]*"))

        self.conf_box = QCheckBox()
        self.pval_box = QCheckBox()
        self.pval_box.clicked.connect(self.update_pval)

        self.plot_btn = QPushButton("Plot")
        self.plot_btn.clicked.connect(self.draw_model)

        self.form_layout.addRow("Title", self.title_box)
        self.form_layout.addRow("X-Limit", self.xlim_box)
        self.form_layout.addRow("Show CI", self.conf_box)
        self.form_layout.addRow("P-value", self.pval_box)
        self.form_layout.addRow(self.plot_btn)

        # spacing
        spacer = QWidget()
        policy = spacer.sizePolicy()
        policy.setVerticalPolicy(QSizePolicy.Expanding)
        spacer.setSizePolicy(policy)
        self.form_layout.addRow(spacer)

        # Exit: save/cancel
        self.save_btn = QPushButton("Save Plot")
        self.save_btn.clicked.connect(self.save_plot)
        self.cancel_btn = QPushButton("Done")
        self.cancel_btn.clicked.connect(self.close)

        self.form_layout.addRow(self.save_btn)
        self.form_layout.addRow(self.cancel_btn)

        self.layout.addWidget(self.form)

        display = QWidget()
        display.layout = QVBoxLayout(display)
        display.layout.addWidget(self.lbl)
        display.layout.addWidget(self.pval_lbl)

        self.layout.addWidget(display)

        self.draw_model()

        self.setLayout(self.layout)

    def draw_model(self):
        # prepare data
        self.title = self.title_box.text()
        self.xlim = (None if self.xlim_box.text() == ""
                     else int(self.xlim_box.text()))
        self.show_conf = self.conf_box.isChecked()
        # prepare inputs
        title = None if self.title == "" else self.title
        xlim = None if self.xlim == 0 else (0, self.xlim)
        show_conf = self.show_conf

        if self.figure is not None:
            self.figure.clear()

        # plot the data
        ax = None
        for (val, fitter) in self.model.fitters.items():
            ax = fitter.plot(ci_show=show_conf,
                             title=title,
                             xlim=xlim,
                             ax=ax)
        self.figure = ax.get_figure()
        canvas = FigureCanvas(self.figure)
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

        self.lbl.setPixmap(QPixmap.fromImage(img))

        if len(self.model.fitters.items()) == 2:
            (time_series, event_series, discrim_series, cat) = self.model.data
            time1 = time_series[discrim_series == cat[0]]
            time2 = time_series[discrim_series == cat[1]]
            event1 = event_series[discrim_series == cat[0]]
            event2 = event_series[discrim_series == cat[1]]
            results = logrank_test(time1, time2, event1, event2)

            self.pval_lbl.setText(str(results.p_value))
            self.pval_box.setCheckState(Qt.CheckState.Checked)
        else:
            self.pval_lbl.setText("Can only have p-values when there "
                                  "are exactly 2 curves")
            self.pval_lbl.hide()

    def save_plot(self):
        # save file
        file_name = QFileDialog.getSaveFileName(self,
                                                "Save Kaplan Diagram",
                                                ".",
                                                "Image files (*.png)")
        if file_name[0] != '':
            self.figure.savefig(file_name[0])

    def update_pval(self, event):
        state = self.pval_box.checkState()
        if state == Qt.CheckState.Checked:
            self.pval_lbl.show()
        else:
            self.pval_lbl.hide()

    def closeEvent(self, event):
        self.figure.clear()


class CoxPreview(QDialog):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.accepted.connect(self.close)
        self.rejected.connect(self.close)

        self.forrest_plot = None
        self.cov_plot = None

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

        # Layout
        self.layout = QVBoxLayout()

        # Title & Body
        self.title_label = QLabel("<font color=darkblue size = 20>Cox Summary")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        self.layout.addWidget(body)

        # Form
        self.form = QWidget()
        self.form.setMinimumWidth(150)
        self.form.layout = QFormLayout(self.form)
        body_layout.addWidget(self.form)

        plot_btn = QPushButton("Plot")
        self.form.layout.addRow(plot_btn)

        spacer = QWidget()
        policy = spacer.sizePolicy()
        policy.setVerticalPolicy(QSizePolicy.Expanding)
        spacer.setSizePolicy(policy)
        self.form.layout.addWidget(spacer)

        self.save_btn = QPushButton("Save Summary")
        self.save_btn.clicked.connect(self.do_save)
        done_btn = QPushButton("Done")
        done_btn.clicked.connect(self.accept)

        self.form.layout.addRow(self.save_btn)
        self.form.layout.addRow(done_btn)

        # TAB WIDGET
        # ----------
        self.tabs = QTabWidget()

        # Table
        self.table = QTableWidget()

        dataframe = model.summary

        dataframe = dataframe[['exp(coef)', 'exp(coef) lower 95%',
                               'exp(coef) upper 95%', 'p']]
        dataframe.columns = ['hazard ratio', 'hazard lower 95%',
                             'hazard upper 95%', 'p']

        self.custom_summary = dataframe
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

        self.tabs.addTab(self.table, "Summary")

        self.cov_plot = QLabel("Covariate Plot")
        self.tabs.addTab(self.cov_plot, "Covariate Plot")

        self.forrest_plot = QLabel("Forrest Plot")
        self.tabs.addTab(self.forrest_plot, "Forrest Plot")

        body_layout.addWidget(self.tabs)

        self.tabs.currentChanged.connect(self.on_tab_change)
        self.setLayout(self.layout)

    def do_save(self):
        n = self.tabs.currentIndex()
        print(n)
        if n == 0:
            self.save_summary()
        if n == 1:
            pass
        if n == 2:
            pass

    def save_summary(self):
        file_name = QFileDialog.getSaveFileName(self,
                                                "Save Cox Summary",
                                                ".",
                                                "CSV Files (*.csv)")

        # fig = fit_cox.plot().get_figure()
        if file_name[0] != '':
            name = file_name[0]
            if name[-4:] != ".csv":
                name += ".csv"
            self.custom_summary.to_csv(name)

    def plot_factor(self):
        print("plotting factor...")

    def on_tab_change(self, n):
        if n == 0:
            self.save_btn.setText("Save Summary")
        else:
            self.save_btn.setText("Save Plot")

    def closeEvent(self, event):
        if self.forrest_plot is not None:
            self.forrest_plot.clear()
        if self.cov_plot is not None:
            self.cov_plot.clear()


class ChiPreview(QDialog):
    def __init__(self, model):
        super().__init__()

        values = model[0:3]
        self.stat = values[0]
        self.pval = values[1]
        self.freedom = values[2]

        layout = QFormLayout(self)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect.save_chi_vals

        layout.addRow("Statistic:", QLabel(str(self.stat)))
        layout.addRow("P-Value:", QLabel(str(self.pval)))
        layout.addRow("Degrees of Freedom", QLabel(str(self.freedom)))
        layout.addRow(save_btn)

    def save_chi_vals(self):
        data = {"P-Value:": self.pval,
                "Statistic": self.stat,
                "Degrees of Freedom": self.freedom}
        frame = pd.DataFrame(data=data)

        file_name = QFileDialog.getSaveFileName(self,
                                                "Save Chi Summary",
                                                ".",
                                                "CSV Files (*.csv)")

        frame.to_csv(file_name)
