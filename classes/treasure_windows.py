from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout, QGridLayout)

import json
import os
import pandas as pd
import openpyxl


class TreasureWindow(QMainWindow):
    def __init__(self, config: dict, conditions: dict,
                 damage_types: dict, highlighting: dict,
                 tables: dict, parent=None):
        print(f"treasure_windows: Starting TreasureWindow.__init__().")
        super().__init__(parent)

        # Set attributes pushed from calling window.
        self.config = config
        self.conditions = conditions
        self.damage_types = damage_types
        self.highlighting = highlighting
        self.tables = tables

        # Set minimum values for new attributes.
        self.encounter_challenge_rating = 0
        self.elite_creature = False
        self.legendary_creature = False
        self.methodology = 'CR'

        # Setup statusbar.
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Initialize the grig.
        self.grid = None

        # Run init_ui.
        self.init_ui()
        print(f"treasure_windows: Completed TreasureWindow.__init__().")

    def init_ui(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Treasure Generation Window")

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        self.setCentralWidget(QWidget(self))
        self.grid = QGridLayout()
        self.centralWidget().setLayout(self.grid)
        self.grid.addWidget(close_button)

        print(f"TW.init_ui: Completed TreasureWindows.init_ui().")



