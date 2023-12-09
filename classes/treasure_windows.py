from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout)

import json
import os
import pandas as pd
import openpyxl

DATA_DIRECTORY = 'data/'
CONDITIONS = f'{DATA_DIRECTORY}/conditions.json'
DAMAGE_TYPES = f'{DATA_DIRECTORY}/damage_types.json'
HIGHLIGHTING = f'{DATA_DIRECTORY}/highlighting.json'
TABLES = f'{DATA_DIRECTORY}/tables.xlsx'
CONFIG_FILE = f'{DATA_DIRECTORY}/config.json'


class TreasureWindow(QMainWindow):
    pass
