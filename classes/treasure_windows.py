import random
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
from functions import return_range, check_string


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
        coin_result = self._extract_dice_from_table_header_return_result(coin_table)
        print(f"TreasureWindow.generate_treasure: coin_table: {coin_table}.")
        print(f"TreasureWindow.generate_treasure: coin_result: {coin_result}.")

        raw_coin_result = self._get_table_result(coin_table, coin_ws, coin_result)
        print(f"TreasureWindow.generate_treasure: raw_coin_result: {raw_coin_result}.")

        if raw_coin_result is not None:
            self._parse_coin_result(raw_coin_result)
        print(f"TreasureWindow.generate_treasure: Coin Treasure completed.")

        # Get the correct worksheet for magic items to include in treasures.
        magic_ws = self._return_ws_name('magic', cr, cr_wb_name)

        # Generate the magic treasure from the table.
        magic_table = self.tables[cr_wb_name][magic_ws]
        magic_result = self._extract_dice_from_table_header_return_result(magic_table)
        print(f"TreasureWindow.generate_treasure: magic_ws: {magic_ws}.")
        print(f"TreasureWindow.generate_treasure: magic_table: {magic_table}.")
        print(f"TreasureWindow.generate_treasure: magic_result: {magic_result}.")

        raw_magic_result = self._get_table_result(magic_table, magic_ws, magic_result)
        print(f"TreasureWindow.generate_treasure: raw_magic_result: {raw_magic_result}.")

        if raw_magic_result is not None:
            self._parse_magic_items(raw_magic_result)

        # Get the correct worksheet for other treasure items (gems and other valuables).
        other_val_ws = self._return_ws_name('other', cr, cr_wb_name)

        # Get gems and other valuables treasure from this table.
        other_val_table = self.tables[cr_wb_name][other_val_ws]
        other_val_result = self._extract_dice_from_table_header_return_result(
            other_val_table)
        print(f"TreasureWindow.generate_treasure: other_val_ws: {other_val_ws}.")
        print(f"TreasureWindow.generate_treasure: other_val_table: {other_val_table}.")
        print(f"TreasureWindow.generate_treasure: other_val_result: {other_val_result}.")

        raw_other_val_result = self._get_table_result(other_val_table,
                                                      other_val_ws,
                                                      other_val_result)
        print(f"TreasureWindow.generate_treasure: raw_other_val_result:"
              f" {raw_other_val_result}.")

        if raw_other_val_result is not None:
            self._parse_other_val_items(raw_other_val_result)

    def _parse_other_val_items(self, raw_result: str):
        """
        This internal function parses text looking for type of items, its rough value,
        and possible dice rolls for number of the item. Next, it determines which
        table in the other valuables workbook that handles those items.

        All of its actions take place internally, changing only the treasure attribute.
        :return:
        """
        print(f"TreasureWindow._parse_other_val_items: Starting to parse result.")
        other_list = raw_result.split(', ')
        print(f"TreasureWindow._parse_other_val_items: raw_list: {other_list}.")

        rolls = []
        tables = []
        values = []
        for item in other_list:
            print(f"TreasureWindow._parse_other_val_items: item: {item}.")
            item = item.rstrip()
            # The entry format is m (ndo) p 'den' 'type', where m, n, o, and p are
            # integers, d denotes dice, 'den' is a 2-letter string for the primary
            # currency (e.g. 'gp' or 'sp'), and 'type' is one of two strings: 'gems'
            # or 'valuables'. If this is only one item, the format is p 'den' 'type'.
            contents = item.split(' ')
            print(f"TreasureWindow._parse_other_val_items: contents: {contents}.")

            item_type = contents[-1]
            item_val = f"{contents[-3]} {contents[-2]}"
            print(f"TreasureWindow._parse_other_val_items: item_type: {item_type}, "
                  f"item_val: {item_val}.")

            if 'valuable' in item_type:
                tables.append('valuables')
            else:
                tables.append('gems')

            print(f"TreasureWindow._parse_other_val_items: tables: {tables}.")

            if len(contents) == 3:
                # There is only one item.
                rolls.append(1)
            else:
                # There are multiple items.
                no_rolls = int(contents[0])
                roll_type = contents[1][1:-1]
                print(f"TreasureWindow._parse_other_val_items: no_rolls: {no_rolls}, "
                      f"roll_type: {roll_type}.")

    def _parse_magic_items(self, magic_result):
        """
        This method takes the string describing how to roll for the magic items, parses it
        down into number of rolls and tables to roll against. It, then, makes the desires
        rolls on the new tables and adds the results to self.treasure. There is no output.
        :param magic_result: str
        :return: None, all activity changes self.treasure attribute
        """
        magic_list = magic_result.split(', ')
        print(f"TreasureWindow._parse_magic_items: magic_list; {magic_list}.")

        rolls = []
        tables = []

        for item in magic_list:
            item = item.rstrip()
            print(f"TreasureWindow._parse_magic_items: item: {item}.")

            item = item.lower().replace('.', '').replace(':', '')
            roll_idx = item.index("r") - 1
            rolls.append(item[:roll_idx])
            num_idx = item.index('#') + 1
            tables.append(int(item[num_idx:]))
        print(f"TreasureWindow._parse_magic_items: rolls: {rolls}. tables: {tables}.")

        # Parse rolls looking for non-integers, since these require dice rolls.
        for idx, item in enumerate(rolls):
            if isinstance(item, int):
                continue
            elif isinstance(item, str):
                try:
                    print(f"TreasureWindow._parse_magic_items: testing string {item}.")
                    n = int(item)
                except ValueError:
                    print(f"TreasureWindow._parse_magic_items: rolling the dice "
                          f"specified in {item}.")
                    rolls[idx] = self._extract_dice_roll_from_text_return_result(item)
                else:
                    print(f"TreasureWindow._parse_magic_items: {item} is integer {n}.")
                    rolls[idx] = n
            else:
                error_msg = (f"TreasureWindow._parse_magic_items: magic item table "
                             f"has an invalid format. There are variable types, "
                             f"included that are not supported by this software, "
                             f"{type(item)}. Only string and integers are supported."
                             f"Returning zero for this input.")
                QMessageBox.critical(self, 'Trappable Error', error_msg)
                rolls[idx] = 0
        print(f"TreasureWindow._parse_magic_items: rolls {rolls}. tables: {tables}.")

        # Convert table numbers to names of Magic Item tables.
        magic_item_wb_names = []
        for wb_name in self.tables:
            if 'magic item' in wb_name.lower():
                magic_item_wb_names.append(wb_name)
            else:
                continue
        if magic_item_wb_names == []:
            error_msg = (f"TreasureWindow._parse_magic_items: There are no magic item "
                         f"tables in the data tables. This is a not a fatal error, but "
                         f"it means that no specific magic items can be determined.")
            QMessageBox.critical(self, 'Serious Error', error_msg)
            return
        else:
            print(f"TreasureWindow._parse_magic_items: magic_item_wb_names: "
                  f"{magic_item_wb_names}.")
        no_magic_item_wbs = len(magic_item_wb_names)
        for idx, num in enumerate(rolls):
            for i in range(num):
                print(f"TreasureWindow._parse_magic_items: idx: {idx}, num: {num}. "
                      f"i: {i}.")
                # Determine the workbook to use.
                wb_choice = random.randint(0, no_magic_item_wbs - 1)
                magic_item_wb_name = magic_item_wb_names[wb_choice]
                magic_item_wb = self.tables[magic_item_wb_name]
                print(f"TreasureWindow._parse_magic_items: wb_choice: {wb_choice}. "
                      f"magic_item_wb_name: {magic_item_wb_name}.")
                # print(f"TreasureWindow._parse_magic_items: magic_item_wb: {magic_item_wb}.")

                # The format for Magic Item tables is '{wb_name} N', where N is an integer
                # from 1 to 26. We have remove the file extension first.
                n = int(tables[idx])
                if magic_item_wb_name[-4] == '.':
                    wb_name_sans_ext = magic_item_wb_name[:-4]
                elif magic_item_wb_name[-5] == '.':
                    wb_name_sans_ext = magic_item_wb_name[:-5]
                else:
                    error_msg = (f"TreasureWindow._parse_magic_items: The magic item "
                                 f"workbook has an invalid name format. Only 3 or 4 "
                                 f"letter extensions are supported.")
                    QMessageBox.critical(self, 'Serious Error', error_msg)
                    return

                magic_item_ws_name = f"{wb_name_sans_ext} {n}"

                try:
                    magic_item_ws = magic_item_wb[magic_item_ws_name]
                except KeyError:
                    error_msg = (f"TreasureWindow._parse_magic_items: A magic item "
                                 f"worksheet in workbook, {magic_item_wb} is not "
                                 f"formatted correctly. Worksheet names must be formated as "
                                 f"'{wb_name_sans_ext} N', where N is an integer between "
                                 f"1 and 26. This is a not a fatal error, but it means "
                                 f"that no specific magic items can be determined "
                                 f"using this workbook.")
                    QMessageBox.critical(self, 'Serious Error', error_msg)
                    return

                # magic_item_ws should be set at this point.
                print(f"TreasureWindow._parse_magic_items: magic_item_ws_name: "
                      f"{magic_item_ws_name}. magic_item_ws: "
                      f"{magic_item_ws}.")
                roll_result = self._extract_dice_from_table_header_return_result(
                    magic_item_ws)
                result = self._get_table_result(magic_item_ws, magic_item_ws_name,
                                                roll_result)
                print(f"TreasureWindow._parse_magic_items: roll_result: "
                      f"{roll_result}. result: {result}.")
                self.treasure.add_item(MagicItem(result))
        print(f"TreasureWindow._parse_magic_items: self.treasure: {self.treasure}.")
        print(f"TreasureWindow._parse_magic_items: Magic Item determination completed.")
        return

    def _extract_dice_roll_from_text_return_result(self, s):
        """
        This static method accepts a string in the format ndm or nDm, where n and m are
        integers separated by the letter d or D. It converts this into Dice(m, dice_number=n)
        and returns Dice.roll(). Any deviation from this format results will be trapped,
        popup a critical message, and a zero returned as a result.
        :param s: str
        :return: int
        """
        s = s.lower()
        l = s.split('d')
        print(f"TreasureWindow._extract_dice_roll_from_text_return_result: s: {s}. l: {l}.")
        # There should be exactly 2 items, both strings that can be converted into integers.
        if len(l) != 2:
            error_msg = (f"TreasureWindow._extract_dice_roll_from_text_return_result: A "
                         f"string with an invalid format, {s}, was sent to this method. "
                         f"Format must be 'ndm' or 'nDm', when n and m are integers.")
            QMessageBox.critical(self, 'Trappable Error', error_msg)
            return 0
        try:
            n = int(l[0])
            m = int(l[1])
        except ValueError:
            error_msg = (f"TreasureWindow._extract_dice_roll_from_text_return_result: A "
                         f"string with an invalid format, {s}, was sent to this method. "
                         f"Format must be 'ndm' or 'nDm', when n and m are integers.")
            QMessageBox.critical(self, 'Trappable Error', error_msg)
            return 0

        die = Dice(m, dice_number=n)
        result = die.roll()
        print(f"TreasureWindow._extract_dice_roll_from_text_return_result: "
              f"n: {n}. m: {m}. result: {result}.")
        print(f"TreasureWindow._extract_dice_roll_from_text_return_result: die: {die}.")
        return result

    @staticmethod
    def _extract_dice_from_table_header_return_result(table):
        """
        This static method requires a treasure table that has the format in which the
        first column is the dice to use and rolled ranges. It will return the dice roll,
        an integer.
        :param table: pd.DataFrame
        :return: int
        """
        dice_info = table.columns[0].lower()
        dice_size = int(dice_info.replace('d', ''))
        die = Dice(dice_size)
        roll = die.roll()
        print(f"TreasureWindow._extract_dice_roll_dice: dice_info: {dice_info}. "
              f"dice_size: {dice_size}. roll: {roll}.")
        print(f"TreasureWindow._extract_dice_roll_dice: \ndie: {die}.")
        return roll

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

        # Convert that results into actual coin numbers.
        dice = []
        numbers = []
        currency = []
        for result in coin_results:
            result = result.rstrip()
            print(f"TreasureWindow._parse_coin_result: result: {result}. ")
            currency.append(result[-2:])
            l_paren = result.index('(')
            r_paren = result.index(')')
            coin_amt = result[l_paren+1:r_paren]
            print(f"TreasureWindow._parse_coin_result: l_paren: {l_paren}. r_paren: "
                  f"{r_paren}. coin_amt: {coin_amt}.")
            try:
                print(f"TreasureWindow._parse_coin_result: testing for x in result, "
                      f"{result}.")
                x_loc = result.index('x')
            except ValueError:
                print(f"TreasureWindow._parse_coin_result: x is not present. Setting "
                      f"numbers to 1 and adding coin_amt to dice.")
                dice.append(coin_amt)
                numbers.append(1)
            else:
                print(f"TreasureWindow._parse_coin_result: x is present. Slicing out "
                      f"dice and number from result.")
                dice.append(result[l_paren+1:x_loc])
                numbers.append(int(result[x_loc+2:r_paren]))

        print(f"TreasureWindow._parse_coin_result: dice: {dice}. numbers: {numbers}. "
              f"currency: {currency}.")

        for i in range(len(coin_results)):
            die_roll = return_die_roll(dice[i])
            total = die_roll * numbers[i]
            coin = Coin(number=total, type=currency[i])
            self.treasure.add_item(coin)
            print(f"TreasureWindow:_parse_coin_result: treasure: {self.treasure}.")
        print(f"TreasureWindow._parse_coin_result: Process completed.")

    def _get_table_result(self, table, ws, roll):
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
            QMessageBox.critical(self, 'Trappable Error', error_msg)
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
