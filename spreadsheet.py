from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QHBoxLayout, QPushButton,
                               QFileDialog, QDialog, QFormLayout, QComboBox,
                               QTextEdit, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import numpy as np

import analyser
from toolbar import ToolBarWidget
from icons import sv_icons

comparators = {
    "=": lambda x, y: x == y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y
}


class SpreadSheetWindow(ToolBarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.sidebar = QWidget()
        self.sidebar.layout = QVBoxLayout()
        self.sidebar.layout.setAlignment(Qt.AlignTop)

        kaplan_lbl = QLabel("<font color=darkblue size = 5>Kaplan Meier")
        self.select_time_btn = QPushButton("Select Time")
        self.select_event_btn = QPushButton("Select Event")
        self.select_discrim_btn = QPushButton("Select Discriminator")
        self.analyse_btn = QPushButton("Analyse!")

        self.select_time_btn.clicked.connect(self.set_time_col)
        self.select_event_btn.clicked.connect(self.set_event_col)
        self.select_discrim_btn.clicked.connect(self.set_discrim_col)
        self.analyse_btn.clicked.connect(self.analyse)

        self.sidebar.layout.addWidget(kaplan_lbl)
        self.sidebar.layout.addWidget(self.select_time_btn)
        self.sidebar.layout.addWidget(self.select_event_btn)
        self.sidebar.layout.addWidget(self.select_discrim_btn)
        self.sidebar.layout.addWidget(self.analyse_btn)

        cox_lbl = QLabel("<font color=darkblue size = 5>Cox Regression")
        self.sidebar.layout.addWidget(cox_lbl)

        self.sidebar.setLayout(self.sidebar.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.data = None
        self.time_col = None
        self.discrim_col = None
        self.event_col = None

        # add actions to the toolbar
        toolbar = self.getBar()
        self.action_filter = QAction(sv_icons.filt, "Filter", toolbar)
        self.action_filter.triggered.connect(self.do_filter)
        toolbar.addAction(self.action_filter)

    def set_data(self, dataframe):
        dims = dataframe.shape
        self.table.setRowCount(dims[0])
        self.table.setColumnCount(dims[1])
        self.table.setHorizontalHeaderLabels(dataframe.columns)

        for row in range(0, dims[0]):
            for col in range(0, dims[1]):
                item = QTableWidgetItem()
                item.setText(str(dataframe.loc[row, dataframe.columns[col]]))
                self.table.setItem(row, col, item)

        self.data = dataframe

    def set_col_color(self, old, color):
        if old is not None:
            for row in range(0, self.data.shape[0]):
                self.table.item(row, old).setBackground(Qt.white)
        col = self.table.currentColumn()
        for row in range(0, self.data.shape[0]):
            self.table.item(row, col).setBackground(color)

    def set_time_col(self, dataframe):
        self.set_col_color(self.time_col, Qt.red)
        self.time_col = self.table.currentColumn()

    def set_discrim_col(self, dataframe):
        self.set_col_color(self.discrim_col, Qt.blue)
        self.discrim_col = self.table.currentColumn()

    def set_event_col(self, dataframe):
        self.set_col_color(self.event_col, Qt.yellow)
        self.event_col = self.table.currentColumn()

    def analyse(self):
        if (self.data is None or self.time_col is None or
            self.discrim_col is None or self.event_col is None):
            print("must have data, time, event, discriminator")
        else:
            time = self.data.columns[self.time_col]
            event = self.data.columns[self.event_col]
            discriminator = self.data.columns[self.discrim_col]

            plot = analyser.get_kaplan(self.data, time, event, discriminator)

            file_name = QFileDialog.getSaveFileName(self,
                                                    "Open Dataset",
                                                    ".",
                                                    "Image files (*.png)")
            if file_name[0] != '':
                plot.savefig(file_name[0])

    def do_filter(self):
        dialog = FilterDialog(self)
        acc, value, col, comp = dialog.run()
        col_type = self.data.dtypes[col]
        if acc == 1:
            if col_type == np.float64:
                val = float(value)
            elif col_type == np.int64:
                val = int(value)
            else:
                val = value

            index = self.data[col].apply(comparators[comp], args=(val,))
            counter = 0
            for elt in index:
                if not elt:
                    self.table.removeRow(counter)
                else:
                    counter = counter + 1

            # now, update the model
            self.data = self.data[index]


class FilterDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Filter")

        form_layout = QFormLayout()
        form = QWidget()
        self.column_combo = QComboBox()
        self.comparator_combo = QComboBox()
        self.value_field = QTextEdit()

        for col in parent.data.columns:
            self.column_combo.addItem(col)
        for comparator in ["=", ">", "<", ">=", "<="]:
            self.comparator_combo.addItem(comparator)

        # set selected column
        self.column_combo.setCurrentIndex(parent.table.currentColumn())

        form_layout.addRow("Column:", self.column_combo)
        form_layout.addRow("Comparator:", self.comparator_combo)
        form_layout.addRow("Value:", self.value_field)

        form.setLayout(form_layout)

        accept_btn = QPushButton("Filter")
        accept_btn.clicked.connect(self.accept)

        reject_btn = QPushButton("Cancel")
        reject_btn.clicked.connect(self.reject)

        button_area = QWidget()
        button_area_layout = QHBoxLayout()
        button_area_layout.addWidget(accept_btn)
        button_area_layout.addWidget(reject_btn)
        button_area.setLayout(button_area_layout)

        layout = QVBoxLayout()
        layout.addWidget(form)

        layout.addWidget(button_area)

        self.setLayout(layout)

    def run(self):
        self.exec()
        return (self.result(),
                self.value_field.toPlainText(),
                self.column_combo.currentText(),
                self.comparator_combo.currentText())
