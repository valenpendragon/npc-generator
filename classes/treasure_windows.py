import sys

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout, QGridLayout, QDockWidget,
                               QComboBox)
from PySide6.QtCore import Qt
import json
import os
import pandas as pd
import numpy as np
import openpyxl


class TreasureWindow(QMainWindow):
    def __init__(self, config: dict, conditions: dict,
                 damage_types: dict, highlighting: dict,
                 tables: dict, parent=None):
        print(f"TreasureWindow: Starting TreasureWindow.__init__().")
        super().__init__(parent)

        # Set attributes pushed from calling window.
        self.config = config
        self.conditions = conditions
        self.damage_types = damage_types
        self.highlighting = highlighting
        self.tables = tables

        # Set minimum values for new attributes.
        self.encounter_challenge_rating = '0'
        self.elite_creature = False
        self.legendary_creature = False
        self.methodology = 'CR'

        # Setup statusbar.
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_msg = None

        # Set up internal variables.
        self._use_cr_mode = True

        # Initialize the grig.
        self.grid = None

        # Run init_ui.
        self.init_ui()
        print(f"TreasureWindow: Completed TreasureWindow.__init__().")

    def init_ui(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Treasure Generation Window")

        # Create the Close and Exit buttons. Create the status
        # message. Positioning will handled near the end of this
        # method.
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.exit_app)
        self.status_msg = QLabel()

        # Set up the CentralWidget that will display our output.
        self.setCentralWidget(QWidget(self))
        self.grid = QGridLayout()
        self.centralWidget().setLayout(self.grid)

        # Create the dock widget for CR-based treasure generation.
        self.dock_widget_cr = QDockWidget(self)
        self.dock_widget_cr.setWindowTitle("CR-Based Generation")
        self.dock_widget_cr.setFloating(False)
        self.dock_widget_cr.setAllowedAreas(Qt.TopDockWidgetArea)
        self.dock_widget_cr.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # Add the QWidget that contains the widgets residing the top DockWidget.
        self.cr_widget = QWidget(self)
        self.cr_widget_layout = QGridLayout(self)
        self.toggle_cr_button = QPushButton("Toggle CR Off", self)
        self.toggle_cr_button.clicked.connect(self.toggle_cr)
        self.cr_widget_layout.addWidget(self.toggle_cr_button, 0, 0)
        self.cr_label = QLabel("Chose Total CR for Encounter: ")
        self.cr_widget_layout.addWidget(self.cr_label, 0, 1)

        #  This is a large combo box for the total CR of the encounter.
        self.cr_dropdown = QComboBox(self)
        dropdown_choices = ['0', '1/8', '1/4', '1/2',
                            '1', '2', '3', '4', '5',
                            '6', '7', '8', '9', '10',
                            '11', '12', '13', '14', '15',
                            '16', '17', '18', '19', '20',
                            '21', '22', '23', '24', '25',
                            '26', '27', '28', '29', '30',
                            '31', '32', '33', '34', '35',
                            '36', '37', '38', '39', '40',
                            '41+']
        self.cr_dropdown.addItems(dropdown_choices)
        self.cr_dropdown.activated.connect(self._pass_cr_value)
        self.cr_widget_layout.addWidget(self.cr_dropdown, 0, 2)

        # Add widgets to top DockWidget.
        self.cr_widget.setLayout(self.cr_widget_layout)
        self.dock_widget_cr.setWidget(self.cr_widget)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_widget_cr)

        # Add run treasure generation button.
        self.generate_treasure_button = QPushButton('Generate')
        self.statusbar.addWidget(self.generate_treasure_button)
        self.generate_treasure_button.clicked.connect(self.generate_treasure)

        # Add Generate Treasure button, Close button, and Exit button to statusBar.
        self.statusbar.addWidget(self.generate_treasure_button)
        self.statusbar.addWidget(close_button)
        self.statusbar.addWidget(exit_button)
        self.statusbar.addWidget(self.status_msg)
        update_txt = f"Treasure Generator is ready to use."
        self.status_msg.setText(update_txt)

        print(f"TreasureWindow.init_ui: Completed TreasureWindow.init_ui().")

    @staticmethod
    def exit_app(self):
        sys.exit()

    def toggle_cr(self):
        if self._use_cr_mode:
            self._use_cr_mode = False
            self.toggle_cr_button.setText("Toggle CR On")
        else:
            self._use_cr_mode = True
            self.toggle_cr_button.setText("Toggle CR Off")

    def _pass_cr_value(self):
        self.encounter_challenge_rating = str(self.cr_dropdown.currentText())
        print(f"TreasureWindow.init_ui: encounter_challenge_rating: "
              f"{self.encounter_challenge_rating}")

    def generate_treasure(self):
        print(f"TreasureWindow.generate_treasure: _use_cr_mode: "
              f"{self._use_cr_mode}. encounter_challenge_rating: "
              f"{self.encounter_challenge_rating}.")

        # Pull the actual integer value for CR.
        match self.encounter_challenge_rating:
            case '0'|'1/8':
                cr = 0
            case '1/4'|'1/2':
                cr = 1
            case '41+':
                cr = 41
            case _:
                cr = int(self.encounter_challenge_rating)
        print(f"TreasureWindow.generate_treasure: cr: {cr}")


if __name__ == "__main__":
    data_dir = "../my_data"
    conditions_fp = f"{data_dir}/conditions.json"
    config_fp = f"{data_dir}/config.json"
    damage_types_fp = f"{data_dir}/damage_types.json"
    highlighting_fp = f"{data_dir}/highlighting.json"

    def load_json(filepath):
        with open(filepath, 'r') as f:
            content= f.read()
        json_content = json.loads(content)
        return json_content

    config = load_json(config_fp)
    conditions = load_json(conditions_fp)
    damage_types = load_json(damage_types_fp)
    highlighting = load_json(highlighting_fp)
    tables = {}
    workbook_names = config['tables']['required tables']
    workbook_fps = []
    for wb_name in workbook_names:
        fp = f"{data_dir}/{wb_name}"
        workbook_fps.append(fp)
    for idx, wb_name in enumerate(workbook_names):
        tables[wb_name] = {}
        wb_fp = workbook_fps[idx]
        ws_list = config['tables']['required tables'][wb_name]
        f = pd.ExcelFile(wb_fp)
        for ws_name in ws_list:
            df = pd.read_excel(wb_fp, sheet_name=ws_name,
                               index_col=0, na_values=True)
            tables[wb_name][ws_name] = df.replace(to_replace=np.nan,
                                                  value=None)

        f.close()

    sys.argv += ['-platform', 'windows:darkmode=2']
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = TreasureWindow(config, conditions, damage_types,
                            highlighting, tables)
    window.show()
    sys.exit(app.exec())
