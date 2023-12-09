from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout)

from classes import TreasureWindow
import sys
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
        self.conditions = None
        self.damage_types = None
        self.highlighting = None
        self.tables = None
        self.config = None
        self.hbox = None
        self.required_tables = None

        # Create statusbar.
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Setting up the attributes for additional windows.
        self.treasure_window = None

        # Starting up the UI.
        self.load_config_files()
        self.load_tables()
        self.init_ui()

    def load_tables(self):
        self.tables = {}
        try:
            required_table_list = self.config["tables"]['required tables']
        except KeyError:
            error_msg = f"Config file, {self.config_fp} is missing required" \
                        f"tables list or is corrupt."
            QMessageBox.critical(self, "Fatal Error", error_msg)
            self.exit_app()
        else:
            for table_name in required_table_list:
                try:
                    table = pd.read_excel(self.tables_fp, sheet_name=table_name,
                                          index_col=None, na_values=False)
                except ValueError:
                    error_msg = f"Either {table_name} is not in tables files, " \
                                f"{self.tables_fp}, or tables files is corrupt."
                    QMessageBox.critical(self, "Fatal Error", error_msg)
                    self.exit_app()
                except FileNotFoundError:
                    error_msg = f"Tables files, {self.tables_fp} was not found."
                    QMessageBox.critical(self, "Fatal Error", error_msg)
                    self.exit_app()
                else:
                    self.tables[table_name] = table
        # This is simply a check for optional tables. If this is not present
        # in config.json, this program will ignore it.
        try:
            optional_table_list = self.config['tables']['optional tables']
        except KeyError:
            status_msg = "No optional tables defined in config file."
            self.statusbar.showMessage(status_msg)
        else:
            for table_name in optional_table_list:
                try:
                    table = pd.read_excel(self.tables_fp, sheet_name=table_name,
                                          index_col=None, na_values=False)
                except ValueError:
                    msg = f"Optional table, {table_name}, was not found in " \
                          f"{self.tables_fp}. Skipping it"
                    self.statusbar.showMessage(msg)
                else:
                    self.tables[table_name] = table

        print(f"load_tables: tables: {self.tables}")

    def check_config_file(self, filepath):
        content = ""
        try:
            with open(filepath, "r") as f:
                content = f.read()
        except (FileNotFoundError, IOError):
            error_msg = f"Configuration file, {filepath}, could not be" \
                        f" read or does not exist."
            QMessageBox.critical(self, "Fatal Error", error_msg)
            self.exit_app()

        if content != "":
            try:
                json_content = json.loads(content)
            except json.decoder.JSONDecodeError:
                error_msg = f"Configuration file, {filepath}, is not a " \
                            f"valid JSON file or may be corrupted."
                QMessageBox.critical(self, "Fatal Error", error_msg)
                self.exit_app()
            else:
                return json_content

    def load_config_files(self):
        self.config = self.check_config_file(self.config_fp)
        print(f"load_config_files: config: {self.config}")
        self.conditions = self.check_config_file(self.conditions_fp)
        print(f"load_config_files: conditions: {self.conditions}")
        self.damage_types = self.check_config_file(self.damage_types_fp)
        print(f"load_config_files: damage_types: {self.damage_types}")
        self.highlighting = self.check_config_file(self.highlighting_fp)
        print(f"load_config_files: highlighting: {self.highlighting}")

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

    def start_treasure_window(self):
        self.statusbar.showMessage("Opening Treasure Generation Window")
        self.treasure_window = TreasureWindow()
        self.treasure_window.show()

    def exit_app(self):
        sys.exit()


if __name__ == "__main__":
    sys.argv += ['-platform', 'windows:darkmode=2']
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
