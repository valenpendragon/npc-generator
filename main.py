from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout)

import sys
import os

DATA_DIRECTORY = 'data/'
CONDITIONS = f'{DATA_DIRECTORY}/conditions.json'
DAMAGE_TYPES = f'{DATA_DIRECTORY}/damage_types.json'
HIGHLIGHTING = f'{DATA_DIRECTORY}/highlighting.json'
