from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout)

import sys
import os

DATA_DIRECTORY = 'data/'
CONDITIONS = f'{DATA_DIRECTORY}/conditions.json'
DAMAGE_TYPES = f'{DATA_DIRECTORY}/damage_types.json'
HIGHLIGHTING = f'{DATA_DIRECTORY}/highlighting.json'
TABLES = f'{DATA_DIRECTORY}/tables.xlsx'
CONFIG_FILE = f'{DATA_DIRECTORY}/config.json'


class StartWindow(QMainWindow):
    def __init__(self, conditions_fp=CONDITIONS, damage_types_fp=DAMAGE_TYPES,
                 highlighting_fp=HIGHLIGHTING, table_fp=TABLES, config_file=CONFIG_FILE):
        super().__init__()
        # Initialize to None any attributes handled by other methods,
        # such as init_ui, load_tables, load_config_files.
        self.conditions_fp = conditions_fp
        self.damage_types_fp = damage_types_fp
        self.highlighting_fp = highlighting_fp
        self.tables_fp = table_fp
        self.config_fp = config_file
        self.vbox = None
        self.statusbar = None
        self.required_tables = None
        self.treasure_window = None
        self.load_config_files()
        self.load_tables()
        self.init_ui()

    def load_tables(self):
        pass

    def load_config_files(self):
        pass

    def init_ui(self):
        pass


if __name__ == "__main__":
    sys.argv += ['-platform', 'windows:darkmode=2']
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
