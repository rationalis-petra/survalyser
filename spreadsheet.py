from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QFileDialog
from PySide6.QtCore import Qt

import analyser


class SpreadSheetWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.sidebar = QWidget()
        self.sidebar.layout = QVBoxLayout()
        self.sidebar.layout.setAlignment(Qt.AlignTop)

        self.select_time_btn = QPushButton("Select Time")
        self.select_event_btn = QPushButton("Select Event")
        self.select_discrim_btn = QPushButton("Select Discriminator")
        self.analyse_btn = QPushButton("Analyse!")

        self.select_time_btn.clicked.connect(self.set_time_col)
        self.select_event_btn.clicked.connect(self.set_event_col)
        self.select_discrim_btn.clicked.connect(self.set_discrim_col)
        self.analyse_btn.clicked.connect(self.analyse)

        self.sidebar.layout.addWidget(self.select_time_btn)
        self.sidebar.layout.addWidget(self.select_event_btn)
        self.sidebar.layout.addWidget(self.select_discrim_btn)
        self.sidebar.layout.addWidget(self.analyse_btn)
        self.sidebar.setLayout(self.sidebar.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.data = None
        self.time_col = None
        self.discrim_col = None
        self.event_col = None

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
