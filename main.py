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
        self.hbox = None
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
        self.setWindowTitle("NPC Generator with Treasures")
        self.setMinimumSize(400, 300)

        treasure_generator_button = QPushButton("Open Treasure Window")
        treasure_generator_button.clicked.connect(self.start_treasure_window)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.exit_app)
        self.setCentralWidget(QWidget(self))
        self.hbox = QHBoxLayout()
        self.centralWidget().setLayout(self.hbox)
        self.hbox.addWidget(treasure_generator_button)
        self.hbox.addWidget(exit_button)

        # Create statusbar.
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def start_treasure_window(self):
        status_msg = "Treasure Window Open"
        self.statusbar.showMessage("Opening Treasure Generation Window")


    def exit_app(self):
        sys.exit()


if __name__ == "__main__":
    sys.argv += ['-platform', 'windows:darkmode=2']
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
