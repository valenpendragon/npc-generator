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
from entities import (Treasure, OtherWealth, MagicItem,
                      Coin, Gem, Valuable, Dice, return_die_roll)
from functions import return_range


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

        # Initialize encounter attributes.
        self.treasure = None

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

        # Create an empty Treasure object.
        self.treasure = Treasure()
        print(f"TreasureWindow.generate_treasure: cr: {cr}. "
              f"treasure: {self.treasure}.")

        # Find the correct workbook for CR-Based treasure generation.
        cr_wb_name = ''
        for wb_name in self.config['tables']['required tables']:
            if 'cr' in wb_name.lower():
                cr_wb_name = wb_name
        if cr_wb_name == '':
            error_msg = (f"TreasureWindow.generate_treasure: A CR-based "
                         f"treasure workbook could not be found in "
                         f"required tables.")
            QMessageBox.critical(self, "Fatal Error", error_msg)
            self.exit_app()

        # Get the correct worksheet for coin (cash) treasure.
        coin_ws = self._return_ws_name('coin', cr, cr_wb_name)
        print(f"TreasureWindow.generate_treasure: coin_ws: {coin_ws}.")

        # Generate the coin treasure from it.
        coin_table = self.tables[cr_wb_name][coin_ws]
        dice_info = coin_table.columns[0].lower()
        dice_size = int(dice_info.replace('d', ''))
        coin_die = Dice(dice_size)
        coin_result = coin_die.roll()

        print(f"TreasureWindow.generate_treasure: coin_table: {coin_table}")
        print(f"TreasureWindow.generate_treasure: coin_die: {coin_die}")
        print(f"TreasureWindow.generate_treasure: dice_info: {dice_info}. "
              f"dice_size: {dice_size}. coin_result: {coin_result}.")

        raw_coin_result = self._get_table_result(coin_table, coin_ws, coin_result)
        print(f"TreasureWindow.generate_treasure: raw_coin_result: {raw_coin_result}.")

        self._parse_coin_result(raw_coin_result)
        print(f"TreasureWindow.generate_treasure: Coin Treasure completed.")

    def _parse_coin_result(self, raw_coin_result):
        """
        This method takes a string in the format: {value} ({dice combo} x
        {number}) {currency type} . The format can appear multiple times with a comma separating each
        set. It will return the final value computed by rolling the correct dice and
        performing the calculations on each such string. It will then add the correct
        Coin objects to self.treasure.
        :param raw_coin_result: str
        :return: None
        """
        coin_results = raw_coin_result.split(', ')
        print(f"TreasureWindow._parse_coin_result: coin_results: {coin_results}.")

        # Clean up the results to make the numbers easier to find.
        for idx, result in enumerate(coin_results):
            coin_results[idx] = result.replace(",", "")

        # Build a new dataframe.
        dice = []
        numbers = []
        currency = []
        for result in coin_results:
            currency.append(result[-2:])
            result = result[:-4]
            l_paren = result.index('(')
            x_loc = result.index('x')
            dice.append(result[l_paren + 1:x_loc])
            numbers.append(int(result[x_loc + 2:]))

        print(f"TreasureWindow._parse_coin_result")

        for i in range(len(coin_results)):
            die_roll = return_die_roll(dice[i])
            total = die_roll * numbers[i]
            coin = Coin(number=total, type=currency[i])
            self.treasure.add_item(coin)
            print(f"TreasureWindow:_parse_coin_result: treasure; "
                  f"{self.treasure}.")
        print(f"TreasureWindow._parse_coin_result: Process completed.")

    @staticmethod
    def _get_table_result(table, ws, roll):
        """
        This static method takes the roll integer, finds the value in the dXX columns
        that contains that value (or is in the range of values) and returns the
        corresponding result text.
        This method needs the name of worksheet sent to it in case there is an error
        in the table content that prevents this method from returning a str from
        the table based on the roll.
        :param table: pandas Dataframe
        :param ws: str
        :param roll: int
        :return: str
        """
        roll_col_name, result_col_name = table.columns
        roll_col = table[roll_col_name]
        result_col = table[result_col_name]
        print(f"TreasureWindow._get_table_result: roll_col: {roll_col}.")
        print(f"TreasureWindow._get_table_result: result_col: {result_col}.")

        roll_idx = None
        for idx, item in roll_col.items():
            m,n = return_range(item)
            if m <= roll <= n:
                roll_idx = idx
                break
        if roll_idx is None:
            error_msg = (f"TreasureWindow._get_table_result: {ws} is invalid. "
                         f"Returning empty coin treasure.")
            QMessageBox.critical(error_msg)
            result = "no coins"
        else:
            result = result_col.loc[roll_idx]

        if result == "-":
            result = "no coins"
        return result

    @staticmethod
    def _get_cr_range(s):
        """
        This static method requires a string and return a tuple of
        integers that is a range of values. It looks for CR or CRs to
        find the range that follows this string.
        :param s: str, workbook title
        :return: 2-tuple of int
        """
        s_lc = s.lower()
        l = s_lc.split()
        r_txt = l[-2]
        if r_txt[-1] == '+':
            r_txt = r_txt[:-1]
        return return_range(r_txt)

    @staticmethod
    def _get_last_word(s):
        """
        This method returns the last word of a title. It is used to
        determine which type of treasure the workbook generates.
        :param s: str, workbook title
        :return: str, last word of title in lowercase
        """
        s_lc = s.lower()
        l = s_lc.split()
        treasure_type = l[-1]
        return treasure_type

    def _return_ws_name(self, treasure_type, cr, wb_name):
        """
        This method finds the worksheet title in
        self.config[tables][required tables][wb_name] that contains
        the cr in its cr range and matches the treasure_type.
        :param treasure_type: str, only 'coin', 'magic', and 'other
            are valid values
        :param cr: int
        :param wb_name: str, workbook name
        :return: str, worksheet title
        """
        if treasure_type not in ('coin', 'magic', 'other'):
            error_msg = (f"Treasure_window._return_ws_name: Invalid "
                         f"type of treasure, {treasure_type}. Only"
                         f"coin, magic, or other are supported.")
            QMessageBox.critical(self, "Fatal Error", error_msg)
            self.exit_app()

        ws_list = self.config['tables']['required tables'][wb_name]
        correct_ws = ''
        for ws_name in ws_list:
            low, high = self._get_cr_range(ws_name)
            type_in_title = self._get_last_word(ws_name)
            if low > high:
                low, high = high, low
            if low <= cr <= high:
                if treasure_type == type_in_title:
                    correct_ws = ws_name
                    break
                else:
                    continue
            else:
                continue
        if correct_ws == '':
            error_msg = (f"Treasure_window._return_ws_name: No "
                         f"worksheet in {wb_name} contains the "
                         f"CR {cr}.")
            QMessageBox.critical(self, "Fatal Error", error_msg)
            self.exit_app()
        else:
            return correct_ws


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
