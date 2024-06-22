import os.path
import pandas as pd
import numpy as np
from entities import return_die_roll

def roll_test(s):
    """
    This function examines a string to see if it is a single
    integer, an integer range, or neither. This is useful
    for testing a table entry to get the integer range it
    covers. If the string is a single integer, it returns
    that value. For an integer range of 'm-n', m must be
    less than or equal to n, and it returns the tuple
    (m, n). If none of these conditions are true, it
    returns the tuple (False,).
    :param s:  str (can be int or float)
    :return:  n-tuple of int, where n is 1 or 2, or 1-tuple
              (False,)
    """
    # For the case that s is actually an integer, return it.
    # For a float, return int(s). For a bool, raise an error.
    if isinstance(s, int):
        return (s,)
    elif isinstance(s, float):
        return (int(s),)
    elif isinstance(s, str):
        l = s.split('-')
        try:
            low = int(l[0])
        except ValueError:
            error_msg = f"roll_test: {s} has invalid format. Must " \
                        f"m or m-n, where m,n are positive integers " \
                        f"such m <= n."
            print(error_msg)
            return (False,)
        else:
            if len(l) == 2:
                try:
                    high = int(l[1])
                except ValueError:
                    error_msg = f"roll_test: {s} has invalid format. Must " \
                                f"m or m-n, where m,n are positive integers " \
                                f"such m <= n."
                    print(error_msg)
                    return (False,)
                else:
                    if low > high:
                        error_msg = f"roll_test: {s} has invalid format. Must " \
                                    f"m or m-n, where m,n are positive integers " \
                                    f"such m <= n."
                        print(error_msg)
                        return (False,)
                    elif low == high:
                        return (low,)
                    else:
                        return low, high
            elif len(l) == 1:
                return (low,)
            else:
                error_msg = f"roll_test: {s} has invalid format. Must " \
                            f"m or m-n, where m,n are positive integers " \
                            f"such m <= n."
                print(error_msg)
                return (False,)
    else:
        raise ValueError(f"roll_test: argument is invalid type {type(s)}")


def check_workbook(input_fp, ws_list):
    """
    Pulls all worksheets in the input_fp and compares the names with the
    ws_list to see if any are missing or misnamed.
    :param input_fp: filepath to an Excel workbook
    :param ws_list: list of str, names of worksheets to look for
    :return: dict: maps missing_names (list) to 'missing' key, unused worksheets
        found in sheet_names to 'extras', and bad worksheets to 'corrupt'.
    """
    f = pd.ExcelFile(input_fp)
    actual_worksheets = f.sheet_names
    missing_names = []
    data = {}
    corrupt_worksheets = []
    for name in ws_list:
        try:
            idx = actual_worksheets.index(name)
        except ValueError:
            missing_names.append(name)
        else:
            actual_worksheets.pop(idx)
            try:
                df = pd.read_excel(input_fp, sheet_name=name,
                                   index_col=None, na_values=False)
            except ValueError:
                corrupt_worksheets.append(name)
            else:
                # This was simply a test. We can get rid of the DataFrame.
                df = None

    if len(actual_worksheets) == 0:
        data['extras'] = None
    else:
        data['extras'] = actual_worksheets
        for name in actual_worksheets:
            try:
                df = pd.read_excel(input_fp, sheet_name=name,
                                   index_col=None, na_values=False)
            except ValueError:
                corrupt_worksheets.append(name)
            else:
                df = None

    if len(missing_names) == 0:
        data['missing'] = None
    else:
        data['missing'] = missing_names

    if len(corrupt_worksheets) == 0:
        data['corrupt'] = None
    else:
        data['corrupt'] = corrupt_worksheets

    f.close()
    return data


def find_workbooks(wb_fp_list):
    """
    This function looks for Excel workbooks, wb_fp_list. Each entry must be a
    full filepath or this function will return it as a missing file.
    :param wb_fp_list: list of filepaths
    :return: dict: maps missing workbooks to 'missing' key and corrupt files
        to 'corrupt' key
    """
    missing_workbooks = []
    corrupt_files = []
    data = {}
    print(f"find_workbooks: missing_workbooks: {missing_workbooks}. "
          f"corrupt_file: {corrupt_files}. data: {data}")
    for fp in wb_fp_list:
        if os.path.exists(fp):
            try:
                f = pd.ExcelFile(fp)
            except ValueError:
                corrupt_files.append(fp)
            else:
                f.close()
        else:
            missing_workbooks.append(fp)
    if len(missing_workbooks) == 0:
        data['missing'] = None
    else:
        data['missing'] = missing_workbooks
    if len(corrupt_files) == 0:
        data['corrupt'] = None
    else:
        data['corrupt'] = corrupt_files
    print(f"find_workbooks: missing_workbooks: {missing_workbooks}. "
          f"corrupt_file: {corrupt_files}. data: {data}")
    return data


def check_worksheet(table, stat_values=False) -> bool:
    """
    Most of the worksheets that will be used in tables should in the
    format roll column followed by a description column. The roll
    column must have a single die to head it. The rest should be
    ranges of integer values separated by a single dash or a single
    integer. Note: Although they appear to a integers, all of the
    values in the worksheet, including single roll values must, in
    fact be strings to parse correctly.

    stat_values is used to override the usual behavior of the function.
    Stat tables have a stat value from 1 to 30 and either a bonus/penalty
    value in the second column or a description.

    This function returns a bool, True if the worksheet is usable, False
    otherwise.
    :param table: pd.DataFrame
    :param stat_values: bool, defaults to False, used to override the
        usual behavior and treat the first column as a d30 stat, running
        from 1 to 30
    :return: bool
    """
    if stat_values:
        pass
    else:
        headers = table.columns
        if len(headers) != 2:
            print(f"check_worksheet: Invalid Format: Invalid number of columns: "
                  f"{len(headers)}.")
            return False
        # Find the roll column first. All unnamed columns will be ignored.
        # The order of the possible values ensures the largest match will
        # be the first one found.
        possible_roll_values = ('d1000', 'd100', 'd30', 'd20',
                                'd12', 'd10', 'd8', 'd6',
                                'd4', 'd2')
        roll_header, desc_header = tuple(headers)
        roll_header_clean = roll_header.lower().strip()
        print(f"check_worksheet: roll_header: {roll_header}. desc_header: "
              f"{desc_header}. roll_header_clean: {roll_header_clean}.")

        if roll_header_clean in possible_roll_values:
            roll_type = roll_header.lower().strip()
            roll_max = int(roll_type[1:])
            print(f"check_worksheet: roll_max: {roll_max}.")
        else:
            if roll_header_clean[0] != 'd':
                print(f"check_worksheet: Invalid Format: Roll column has an "
                      f"invalid header, {roll_header}.")
                return False
            else:
                try:
                    roll_max = int(roll_header_clean[1:])
                except ValueError:
                    print(f"check_worksheet: Invalid Format: Roll column has an "
                          f"invalid header, {roll_header}.")
                    return False
        roll_column = table[roll_header]
        desc_column = table[desc_header]

        print(f"check_worksheet: roll_max: {roll_max}.")
        print(f"check_worksheet: roll_column: {roll_column}.")
        print(f"check_worksheet: desc_column: {desc_column}.")
        last_val = 0
        for item in roll_column:
            print(f"check_worksheet: last_val: {last_val}. item: {item}.")
            if item is None or item == '-':
                # Skip blank entries.
                continue
            else:
                item_ck = roll_test(str(item))
                print(f"check_worksheet: item_ck: {item_ck}.")
                if item_ck[0] is False:
                    # If roll_test returned (False,), there is a bad entry in the
                    # roll column. 0 is also an invalid entry, since rolls start
                    # with 1.
                    print(f"check_worksheet: Invalid Format: Item, {item_ck} has an "
                          f"invalid format.")
                    return False
                else:
                    if last_val + 1 != item_ck[0]:
                        # There is a gap or an overlap.
                        print(f"check_worksheet: Invalid Format: Item, {item_ck}, "
                              f"creates a gap or an overlap. ")
                        return False
                    else:
                        if len(item_ck) == 2:
                            last_val = item_ck[1]
                        else:
                            last_val = item_ck[0]
        print(f"check_worksheet: last_val: {last_val}. roll_max: {roll_max}.")
        if last_val != roll_max:
            # Either the values goes over the maximum dice value or under it. Either
            # way, the roll column is invalid.
            gap = last_val - roll_max
            print(f"check_worksheet: Invalid Format: Roll column has a gap of {gap} "
                  f"between max die result of {roll_max} and the last value "
                  f"{last_val}.")
            return  False
        else:
            # Now, we need to determine if this is a treasure table. If so, we need
            # to know which type. Coin tables have a very specific format.
            if 'coin' in desc_header.lower().strip():
                return _validate_coin_table_format(desc_column)
            else:
                return True


def check_string(s):
    """This function takes a utf-8 string and returns a
    list of all of the characters that appear in it.
    :param s: str
    :return l: list of utf-8 characters
    """
    l = [ord(c) for c in list(s)]
    return l


def _validate_coin_table_format(coin_col: pd.Series):
    """
    This function checks the format of the descriptive column. The header format
    is not important, but the entries in the columns must be strings comprised
    of a single 'content' or multiple 'contents' separated by a comma followed by
    a space. An 'entry' is a string having one of two formats:
        i (jdk x l) 'currency type'
        i (jdk) 'currency type'
    where i, j, k, and l are integers, d an x are the actual letters 'd' and
    'x', and 'currency' is a two letter abbreviation. While any two letters
    for currency should parse correctly, sticking to 'pp', 'gp, 'ep', and
    'cp' is recommended. Commas are permitted for large integers. The 'x' must
    be bracketed by at least one space. The spaces around the 'x' are not
    required. None of the letters are case-dependent, but all of them will
    be rendered into lowercase when computing the coin results.

    No coin result can be NoneType.

    Example (multiple contents): 900 (2d8 x 100) gp, 500 (2d4 x 100) pp
    Example (multiple contents): 700 (2d6 x 100) ep, 15 (6d6) gp
    Example (single content): 4,500 (10d8 x 1,000) gp
    Example (single content): 350(1d6 x 10) cp
    Example (single content): 33 (6d10) sp

    There can any number of contents per item in the series. but currency
    types cannot appear more than once.

    This function returns True if the format of the Series is correct,
    False otherwise.
    :param df: pd.Series
    :return: bool
    """

    for raw_coin_result in coin_col:
        if raw_coin_result is None:
            print(f"_validate_coin_table_format: Invalid Format. Raw coin result "
                  f"is NoneType which is invalid for any encounter. Even a peon "
                  f"carries a few coppers.")
            return False
        raw_coin_result = raw_coin_result.rstrip()
        coin_results = raw_coin_result.split(", ")

        # Get rid of commas in large integers.
        for idx, result in enumerate(coin_results):
            coin_results[idx] = result.replace(",", "")

        print(f"_validate_coin_table_format: item: {raw_coin_result}. "
              f"item_list: {coin_results}.")

        dice = []
        numbers = []
        currency = []
        fudge_amts = []

        for idx, result in enumerate(coin_results):
            result = result.lower()
            currency.append(result[-2:])
            try:
                l_paren = result.index('(')
                r_paren = result.index(')')
            except ValueError:
                print(f"_validate_coin_table_format: Invalid Format: Item, "
                      f"{raw_coin_result}, content, {coin_results[idx]}, is "
                      f"missing at least one parentheses.")
                return False
            # roll_section needs to look like nd
            roll_section = result[l_paren+1:r_paren]
            fudge_amt = result[:l_paren]
            try:
                fudge_amts.append(int(fudge_amt))
            except ValueError:
                print(f"_validate_coin_table_format: Invalid Format: For item, "
                      f"{raw_coin_result}, content, {coin_results[idx]}, first "
                      f"{l_paren} characters must be integers.")
                return False

            try:
                x_loc = result.index('x')
            except ValueError:
                print(f"_validate_coin_table_format: x is not present. Add 1 to "
                      f"numbers and roll_section, {roll_section}, to dice.")
                dice.append(roll_section)
                numbers.append(1)
            else:
                dice.append(result[l_paren+1:x_loc])
                no_test = result[x_loc+2:r_paren]
                try:
                    numbers.append(int(result[x_loc+2:r_paren]))
                except ValueError:
                    print(f"_validate_coin_table_format: Invalid Format: For item, "
                          f"{raw_coin_result}, content, {coin_results[idx]}, number "
                          f"{no_test} must be an integer.")
                    return False
                else:
                    try:
                        die_roll = return_die_roll(dice[idx])
                    except ValueError:
                        print(f"_validate_coin_table_format: Invalid Format: For item, "
                              f"{raw_coin_result}, content, {coin_results[idx]} with "
                              f"dice roll {dice[idx]} must be 'ndm' or 'nDm', where"
                              f"n and m are integers and d/D is the utf-8 letter.")
                        return False

        # Final check: None of the currencies can be duplicates in a single result.
        # This program will not add them all up.
        currency_set = set(currency)
        if len(currency_set) != len(currency):
            print(f"_validate_coin_table_format: Invalid Format: Item, "
                  f"{raw_coin_result} contains duplicate currency types "
                  f"which is not supported by this software.")
            return False
    return True


if __name__ == "__main__":
    # Set test strings.
    l = ['blank', '10', '11-13', '12-10', '', 12, 12.4, '1-2-3' ]
    for item in l:
        print(f"Test results for {item} is {roll_test(item)}")

    wb_fp = '../data/test_workbook.xlsx'
    ws_list = ['Treasure For CR 0 Magic', 'Treasure For CRs 1-2 Coin',
               'Treasure For CRs 1-2 Magic', 'Treasure For CRs 3-4 Coin',
               'Treasure For CRs 3-4 Magic', 'Treasure for CR 0 Coin'
               'Treasure For CR 0 Coin']
    f = pd.ExcelFile(wb_fp)
    tables = {}
    for ws in ws_list:
        try:
            df = pd.read_excel(wb_fp, sheet_name=ws, index_col=0, na_values=True)
        except ValueError:
            print(f"Worksheet, {ws}, is not in workbook, {wb_fp}.")
        else:
            tables[ws] = df.replace(to_replace=np.nan, value=None)
    f.close()
    print(f"Collected tables: {tables}.")
    for ws in tables.keys():
        print(f"Testing table, {ws}.")
        if check_worksheet(tables[ws]):
            print(f"Table, {ws}, has a valid format and is usable.")
        else:
            print(f"Table, {ws}, has an invalid format and cannot be used.")
