from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QHBoxLayout, QPushButton,
                               QDialog, QFormLayout, QComboBox,
                               QTextEdit, QLabel, QMessageBox)
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QAction

import pandas as pd
import numpy as np

comparators = {
    "=": lambda x, y: x == y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
    "!=": lambda x, y: x != y,
    "nan": lambda x: pd.isna(x)
}


class Filter:
    def __init__(self, col, comp, val=None):
        self.col = col
        self.comp = comp
        self.val = val


class FilterDialog(QDialog):
    def __init__(self, columns, currentColumn):
        super().__init__()
        self.setWindowTitle("Filter")

        form_layout = QFormLayout()
        form = QWidget()
        self.column_combo = QComboBox()
        self.comparator_combo = QComboBox()
        self.value_field = QTextEdit()

        for col in columns:
            self.column_combo.addItem(col)
        for comparator in comparators.keys():
            self.comparator_combo.addItem(comparator)

        # set selected column
        self.column_combo.setCurrentIndex(currentColumn)

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


class FilterWidget(QWidget):
    def __init__(self, filt, parent):
        super().__init__(parent)
        self.parent = parent
        self.filt = filt

        txt = filt.col + " "
        if filt.val is None:
            txt = txt + str(filt.comp)
        else:
            txt = txt + str(filt.comp) + str(filt.val)
        lbl = QLabel(txt)
        xbtn = QPushButton("remove")
        xbtn.clicked.connect(self.do_delete)

        layout = QHBoxLayout(self)
        layout.addWidget(lbl)
        layout.addWidget(xbtn)

    def do_delete(self):
        self.parent.removeFilter(self)
        self.parent.update()
        self.hide()


class FilterWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.layout = QVBoxLayout(self)
        filterTitle = QLabel("<font color=darkblue size = 20>Kaplan Meier</font>")
        self.layout.addWidget(filterTitle)

        for filt in parent.filters:
            filterWidget = FilterWidget(filt, self)
            self.layout.addWidget(filterWidget)

        bottomBar = QWidget()
        bottomLayout = QHBoxLayout(bottomBar)
        newFilterBtn = QPushButton("new")
        newFilterBtn.clicked.connect(self.new_filter)

        doneBtn = QPushButton("done")
        doneBtn.clicked.connect(self.accept)
        bottomLayout.addWidget(doneBtn)
        bottomLayout.addWidget(newFilterBtn)
        self.layout.addWidget(bottomBar)

    def new_filter(self):
        dialog = FilterDialog(self.parent.data.columns,
                              self.parent.table.currentColumn())
        acc, value, col, comp = dialog.run()
        if acc == 0:
            return

        col_type = self.parent.data.dtypes[col]
        if col_type == np.float64:
            try:
                val = float(value)
            except ValueError:
                msg = QMessageBox()
                msg.setText("The value " + value + " is nota number, "
                            "but this columns contains numeric data. "
                            "Please provide a numeric value.")
                msg.setWindowTitle("Error Report")
                msg.exec()
                return
        elif col_type == np.int64:
            try:
                val = int(value)
            except ValueError:
                msg = QMessageBox()
                msg.setText("The value " + value + " is nota number, "
                            "but this columns contains numeric data. "
                            "Please provide a numeric value.")
                msg.setWindowTitle("Error Report")
                msg.exec()
                return
        else:
            val = value

        fil = Filter(col, comp, val)
        filWidget = FilterWidget(fil, self.parent)
        self.parent.filters.append(fil)
        self.layout.insertWidget(self.layout.count() - 1, filWidget)

    def run(self):
        self.exec()

    def removeFilter(self, filterWidget):
        self.layout.removeWidget(filterWidget)
        filterWidget.hide()
        self.parent.filters.remove(filterWidget.filt)
