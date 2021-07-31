import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QFileDialog
from PySide6.QtWidgets import (QTableWidget, QHBoxLayout, QVBoxLayout,
                               QStackedLayout)
from PySide6.QtCore import Qt


welcome_text = """
Welcome to Survalyser!
...
"""

load_text = """
To load data into survalyser, click the 'Load Data' button
in the main menu, and select the file you'd like to load data
from. If you encounter issues, it may be due to one of the following
reasons:
...
"""

spreadsheet_text = """
The spreadsheet view ....
...
"""

analyse_text = """
When analysing data...
...
"""



class DocumentationTextArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QStackedLayout()

        self.welcome_text = QLabel(welcome_text)
        self.load_text = QLabel(load_text)
        self.spreadsheet_text = QLabel(spreadsheet_text)
        self.analyse_text = QLabel(analyse_text)

        self.layout.addWidget(self.welcome_text)
        self.layout.addWidget(self.load_text)
        self.layout.addWidget(self.spreadsheet_text)
        self.layout.addWidget(self.analyse_text)

        self.setLayout(self.layout)


class DocumentationButtonArrea(QWidget):
    def __init__(self, parent, text_area):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.welcome_button = QPushButton("Welcome")
        self.load_button = QPushButton("Loading Data")
        self.spreadsheet_button = QPushButton("Spreadsheet View")
        self.analyse_button = QPushButton("Analysing Data")

        self.welcome_button.clicked.connect(parent.welcome)
        self.load_button.clicked.connect(parent.load)
        self.spreadsheet_button.clicked.connect(parent.spreadsheet)
        self.analyse_button.clicked.connect(parent.analyse)

        self.layout.addWidget(self.welcome_button)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.spreadsheet_button)
        self.layout.addWidget(self.analyse_button)

        self.setLayout(self.layout)


class DocumentationWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.text_area = DocumentationTextArea(self)
        self.button_area = DocumentationButtonArrea(self, self.text_area)

        self.layout.addWidget(self.button_area)
        self.layout.addWidget(self.text_area)
        self.setLayout(self.layout)

    def welcome(self):
        self.text_area.layout.setCurrentIndex(0)

    def load(self):
        self.text_area.layout.setCurrentIndex(1)

    def spreadsheet(self):
        self.text_area.layout.setCurrentIndex(2)

    def analyse(self):
        self.text_area.layout.setCurrentIndex(3)
