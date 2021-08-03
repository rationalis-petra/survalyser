# import sys
from PySide6.QtWidgets import QWidget, QPushButton, QLabel
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QStackedLayout)
from PySide6.QtCore import Qt

from toolbar import ToolBarWidget


welcome_text = """
Welcome to Survalyser!
"""

load_text = """
To load data into Survalyser, you need to export it as a '.csv' file. In order to be analysed, the data needs to be formatted correctly:

Time data: The time data must be completely numeric, in your units of choice (e.g if a patient lived for 3 years 6 monts, the time value could be 3.5 (years), 42 (months), etc.

Event data: The 'event' column must consist of values reading True or False. The 'event' will be True if something of interest occurred (e.g. patient death), and False if the patient should be censored.
"""

spreadsheet_text = """
The spreadsheet view allow you to see the data you have loaded in to the application for analysis.
"""

analyse_text = """
When analysing data...
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


class DocumentationWindow(ToolBarWidget):
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
