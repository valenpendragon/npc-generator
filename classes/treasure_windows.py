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
        self.encounter_challenge_rating = 0
        self.elite_creature = False
        self.legendary_creature = False
        self.methodology = 'CR'

        # Setup statusbar.
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_msg = None

        # Initialize the grig.
        self.grid = None

        # Run init_ui.
        self.init_ui()
        print(f"treasure_window: Completed TreasureWindow.__init__().")

    def init_ui(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Treasure Generation Window")

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.exit_app)
        self.status_msg = QLabel()

        self.setCentralWidget(QWidget(self))
        self.grid = QGridLayout()
        self.centralWidget().setLayout(self.grid)

        # Create the dock widget for CR-based treasure generation.
        dock_widget_cr = QDockWidget(self)
        dock_widget_cr.setWindowTitle("CR-Based Generation")
        dock_widget_cr.setFloating(False)
        dock_widget_cr.setAllowedAreas(Qt.TopDockWidgetArea)
        dock_widget_cr.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # Add the QWidget that contains the widgets residing the top DockWidget.
        cr_widget = QWidget(self)
        cr_widget_layout = QGridLayout(self)
        toggle_cr_button = QPushButton("Toggle CR", self)
        toggle_cr_button.clicked.connect(self.cr_based_generation)
        cr_widget_layout.addWidget(toggle_cr_button, 0, 0)
        cr_label = QLabel("Chose Total CR for Encounter: ")
        cr_widget_layout.addWidget(cr_label, 0, 1)

        #  This is a large combo box for the total CR of the encounter.
        cr_dropdown = QComboBox(self)
        dropdown_choices = ['1/8', '1/4', '1/2',
                            '1', '2', '3', '4', '5',
                            '6', '7', '8', '9', '10',
                            '11', '12', '13', '14', '15',
                            '16', '17', '18', '19', '20',
                            '21', '22', '23', '24', '25',
                            '26', '27', '28', '29', '30',
                            '31', '32', '33', '34', '35',
                            '36', '37', '38', '39', '40',
                            '41+']
        cr_dropdown.addItems(dropdown_choices)
        cr_widget_layout.addWidget(cr_dropdown, 0, 2)

        # Add widgets to top DockWidget.
        cr_widget.setLayout(cr_widget_layout)
        dock_widget_cr.setWidget(cr_widget)
        self.addDockWidget(Qt.TopDockWidgetArea, dock_widget_cr)

        # Add Close button and Exit button to statusBar
        self.statusbar.addWidget(close_button)
        self.statusbar.addWidget(exit_button)
        self.statusbar.addWidget(self.status_msg)
        update_txt = f"Treasure Generator is ready to use."
        self.status_msg.setText(update_txt)

        print(f"TW.init_ui: Completed TreasureWindow.init_ui().")

    def exit_app(self):
        sys.exit()

    def cr_based_generation(self):
        update_txt = f"CR-Based Generation enabled."
        self.status_msg.setText(update_txt)


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
