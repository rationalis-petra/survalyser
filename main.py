# import sys
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QFileDialog,
                               QVBoxLayout, QStackedLayout, QApplication)
from PySide6.QtCore import Qt
# from PySide6.QtGui import QIcon

import pandas as pd

# other parts of program
from spreadsheet import SpreadSheetWindow
from docs import DocumentationWindow


class MainWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("<font color=darkblue size = 20>Survalyser")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.resume_btn = QPushButton("Resume")
        self.save_btn = QPushButton("Saves")
        self.load_btn = QPushButton("Load Data")
        self.doc_btn = QPushButton("Documentation")

        self.resume_btn.clicked.connect(parent.on_resume)
        self.save_btn.clicked.connect(parent.on_save)
        self.load_btn.clicked.connect(parent.on_load)
        self.doc_btn.clicked.connect(parent.on_doc)

        self.layout.addWidget(self.resume_btn)
        self.layout.addWidget(self.save_btn)
        self.layout.addWidget(self.load_btn)
        self.layout.addWidget(self.doc_btn)

        self.setLayout(self.layout)


class SurvalyserMain(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = MainWindow(self)
        self.spreadsheet_window = SpreadSheetWindow(self)
        self.doc_window = DocumentationWindow(self)

        self.layout = QStackedLayout()
        self.layout.addWidget(self.main_window)
        self.layout.addWidget(self.spreadsheet_window)
        self.layout.addWidget(self.doc_window)

        self.setLayout(self.layout)

        self.resize(1080, 720)
        self.move(100, 100)

        self.setWindowTitle("Survalyser")

    def on_load(self):
        self.spreadsheet_window
        file_name = QFileDialog.getOpenFileName(self,
                                                "Open Dataset",
                                                ".",
                                                "CSV files (*.csv)")
        dataframe = pd.read_csv(file_name[0])
        self.spreadsheet_window.set_data(dataframe)
        self.layout.setCurrentIndex(1)

    def on_resume(self):
        dataframe = pd.read_csv('test-data/indigenous-clean.csv')
        self.spreadsheet_window.set_data(dataframe)
        self.layout.setCurrentIndex(1)

    def on_save(self):
        pass

    def on_doc(self):
        self.layout.setCurrentIndex(2)

    def go_home(self):
        self.layout.setCurrentIndex(0)


def main():
    win = SurvalyserMain()
    win.show()
    app.exec()


app = QApplication([])
# main()
