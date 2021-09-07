from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QHBoxLayout, QPushButton,
                               QFileDialog, QDialog, QFormLayout, QComboBox,
                               QTextEdit, QLabel, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

import analyser
from toolbar import ToolBarWidget
from icons import sv_icons
from preview import KaplanPreview, CoxPreview, ChiPreview

comparators = {
    "=": lambda x, y: x == y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
    "!=": lambda x, y: x != y,
    "nan": lambda x: pd.isna(x)
}


class SpreadSheetWindow(ToolBarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.sidebar = QWidget()
        self.sidebar.layout = QVBoxLayout()
        self.sidebar.layout.setAlignment(Qt.AlignTop)

        self.data = None
        self.time_col = None
        self.discrim_col = None
        self.event_col = None

        # KAPLAN MEIER
        kaplan_lbl = QLabel("<font color=darkblue size = 5>Kaplan Meier")
        kaplan_time_lbl = QLabel("Select Time")
        self.kaplan_time_combo = QComboBox()
        kaplan_event_lbl = QLabel("Select Event")
        self.kaplan_event_combo = QComboBox()
        kaplan_discrim_lbl = QLabel("Select Discriminator")
        self.kaplan_discrim_combo = QComboBox()
        self.kaplan_analyse_btn = QPushButton("Analyse!")

        self.kaplan_analyse_btn.clicked.connect(self.analyse_kaplan)

        self.sidebar.layout.addWidget(kaplan_lbl)
        self.sidebar.layout.addWidget(kaplan_time_lbl)
        self.sidebar.layout.addWidget(self.kaplan_time_combo)
        self.sidebar.layout.addWidget(kaplan_event_lbl)
        self.sidebar.layout.addWidget(self.kaplan_event_combo)
        self.sidebar.layout.addWidget(kaplan_discrim_lbl)
        self.sidebar.layout.addWidget(self.kaplan_discrim_combo)
        self.sidebar.layout.addWidget(self.kaplan_analyse_btn)

        # COX REGRESSION
        cox_lbl = QLabel("<font color=darkblue size = 5>Cox Regression")
        cox_time_lbl = QLabel("Select Time Column")
        self.cox_time_combo = QComboBox()
        cox_event_lbl = QLabel("Select Event Column")
        self.cox_event_combo = QComboBox()
        cox_covar_lbl = QLabel("Select Covaraites")
        self.cox_covar_cols = MultiColumnSelect(self)
        self.cox_analyse_btn = QPushButton("Analyse!")

        self.cox_analyse_btn.clicked.connect(self.analyse_cox)

        self.sidebar.layout.addWidget(cox_lbl)
        self.sidebar.layout.addWidget(cox_time_lbl)
        self.sidebar.layout.addWidget(self.cox_time_combo)
        self.sidebar.layout.addWidget(cox_event_lbl)
        self.sidebar.layout.addWidget(self.cox_event_combo)
        self.sidebar.layout.addWidget(cox_covar_lbl)
        self.sidebar.layout.addWidget(self.cox_covar_cols)
        self.sidebar.layout.addWidget(self.cox_analyse_btn)

        # CHI Square Test
        chi_lbl = QLabel("<font color=darkblue size = 5>Chi Square")
        chi_discriminator_lbl = QLabel("Select Discriminator")
        self.chi_discriminator_col = QComboBox()
        chi_cat_lbl = QLabel("Select Category Columns")
        self.chi_cat_col = QComboBox()
        self.chi_analyse_btn = QPushButton("Test!")

        self.chi_analyse_btn.clicked.connect(self.analyse_chi)

        self.sidebar.layout.addWidget(chi_lbl)
        self.sidebar.layout.addWidget(chi_discriminator_lbl)
        self.sidebar.layout.addWidget(self.chi_discriminator_col)
        self.sidebar.layout.addWidget(chi_cat_lbl)
        self.sidebar.layout.addWidget(self.chi_cat_col)
        self.sidebar.layout.addWidget(self.chi_analyse_btn)

        # self.scroll_area = QScrollArea()
        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scroll_area.setBackgroundRole(QPalette.Dark)
        # self.scroll_area.setWidget(self.sidebar)

        self.sidebar.setLayout(self.sidebar.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

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

        self.kaplan_time_combo.addItems(dataframe.columns)
        self.kaplan_event_combo.addItems(dataframe.columns)
        self.kaplan_discrim_combo.addItems(dataframe.columns)

        self.cox_time_combo.addItems(dataframe.columns)
        self.cox_event_combo.addItems(dataframe.columns)

        self.chi_discriminator_col.addItems(dataframe.columns)
        self.chi_cat_col.addItems(dataframe.columns)

        self.data = dataframe
        self.cox_covar_cols.set_data(dataframe)

    def analyse_kaplan(self):
        time = self.kaplan_time_combo.currentText()
        event = self.kaplan_event_combo.currentText()
        discriminator = self.kaplan_discrim_combo.currentText()

        # do analysis
        model = analyser.get_kaplan(self.data, time, event, discriminator)

        # do preview
        preview = KaplanPreview(model)
        preview.exec()

    def analyse_cox(self):
        time_col = self.cox_time_combo.currentText()
        event_col = self.cox_event_combo.currentText()
        value_cols = self.cox_covar_cols.get_values()

        bad_cols = []
        for col in value_cols:
            if self.data[col].isnull().values.any():
                bad_cols.append(col)

        cox_data = self.data
        if len(bad_cols) != 0:
            msg_box = QMessageBox()
            msg_box.setText("The Following columns contain nan values: " +
                            ' '.join(bad_cols))
            msg_box.setInformativeText("Would you like to filter them out?")
            filter_btn = msg_box.addButton("Filter", QMessageBox.ActionRole)
            msg_box.addButton(QMessageBox.Cancel)

            msg_box.exec()
            if not msg_box.clickedButton() == filter_btn:
                return
            else:
                # filter out nan values
                index = np.full(self.data.shape[0], True, dtype=bool)
                for col in bad_cols:
                    index = index & self.data[col].notnull()

                cox_data = self.data[index]
                # connect

        try:
            fit_cox = analyser.get_cox(cox_data, time_col,
                                       event_col, value_cols)
            preview = CoxPreview(fit_cox)
            preview.exec()

        except ValueError:
            warn = QMessageBox()
            warn.setText("The cox fitter has returned a ValueError. "
                         "It is most likely that one of the columns "
                         "you provided has non-numeric data!")
            warn.exec()

    def analyse_chi(self):
        discriminator_col = self.chi_discriminator_col.currentText()
        category_cols = self.chi_cat_col.currentText()

        chisq_data = pd.crosstab(self.data[category_cols],
                                 self.data[discriminator_col])

        value = np.array([chisq_data.iloc[0][0:5].values,
                          chisq_data.iloc[1][0:5].values])
        prev = ChiPreview(chi2_contingency(value))
        prev.exec()

    def do_filter(self):
        dialog = FilterDialog(self)
        acc, value, col, comp = dialog.run()
        col_type = self.data.dtypes[col]
        # special case: isnan
        if comp == "nan":
            index = self.data[col].apply(comparators[comp])
            counter = 0
            for elt in index:
                if elt:
                    self.table.removeRow(counter)
                else:
                    counter = counter + 1

            # now, update the model
            self.data = self.data[~index]
            return

        if acc == 1:
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

            index = self.data[col].apply(comparators[comp], args=(val,))
            counter = 0
            for elt in index:
                if elt:
                    self.table.removeRow(counter)
                else:
                    counter = counter + 1

            # now, update the model
            self.data = self.data[~index]


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
        for comparator in comparators.keys():
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


class MultiColumnSelect(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()
        container = QWidget()
        self.combo_layout = QVBoxLayout()
        container.setLayout(self.combo_layout)

        btnContainer = QWidget()
        btnLayout = QHBoxLayout()

        addComboButton = QPushButton("+")
        rmComboButton = QPushButton("-")

        addComboButton.clicked.connect(self.add_combo)
        rmComboButton.clicked.connect(self.rm_combo)

        btnLayout.addWidget(addComboButton)
        btnLayout.addWidget(rmComboButton)
        btnContainer.setLayout(btnLayout)

        layout.addWidget(container)
        layout.addWidget(btnContainer)

        self.setLayout(layout)

        self.combo_widgets = []
        self.add_combo()

    def add_combo(self):
        combo = QComboBox()
        if self.parent.data is not None:
            combo.addItems(self.parent.data.columns)
        self.combo_widgets.append(combo)
        self.combo_layout.addWidget(combo)

    def rm_combo(self):
        widget = self.combo_widgets.pop()
        self.combo_layout.removeWidget(widget)
        self.update()

    def set_data(self, data):
        for combo in self.combo_widgets:
            combo.clear()
            combo.addItems(data.columns)

    def get_values(self):
        return list(map(lambda x: x.currentText(), self.combo_widgets))
