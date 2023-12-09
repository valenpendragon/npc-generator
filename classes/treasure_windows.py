from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout, QGridLayout)

import json
import os
import pandas as pd
import openpyxl


class TreasureWindow(QWidget):
    def __init__(self, config: dict, conditions: dict,
                 damage_types: dict, highlighting: dict,
                 parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Treasure Generation Window")
        main_layout = QGridLayout()

        # Set attributes pushed from calling window.
        self.config = config
        self.conditions = conditions
        self.damage_types = damage_types
        self.highlighting = highlighting

        # Set minimum values for new attributes.
        self.encounter_challenge_rating = 0
        self.elite_creature = False
        self.legendary_creature = False


