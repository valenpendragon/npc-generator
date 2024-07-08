import os.path
import pandas as pd
import numpy as np
from entities import return_die_roll


def fix_worksheet(table: pd.DataFrame):
    """
    An error in Pandas conversion of some worksheets can result in first
    item in the roll_column being interpreted as a np.NaN and converted
    to None value. This only seems to happen when a '1' appears in the
    0 element of the series. But, it has to be identified and corrected
    before checking the worksheet for valid format. This was only seen in
    magic items tables which have 2 columns, rolls and descriptions/items.
    This function returns the corrected table (or the original if nothing
    needs to be corrected.
    :param table:
    :return: pd.DataFrame
    """
    cols = table.columns
    roll_col_name = ''
    col_no = None
    print(f"fix_worksheet: table: {table}.")
    print(f"fix_worksheet: cols: {cols}.")
    for idx, col_name in enumerate(cols):
        possible_dice = ['d'+str(num) for num in range(100, 1001, 100)]
        print(f"fix_worksheet: possible_dice: {possible_dice}.")
        print(f"fix_worksheet: idx: {idx}. col_name: {col_name}.")
        for die in possible_dice:
            print(f"fix_worksheet: die: {die}.")
            if die == col_name.lower():
                roll_col_name = col_name
                col_no = idx
                print(f"fix_worksheet: roll_col_name: {roll_col_name}. "
                      f"col_no: {col_no}.")
                break
            else:
                continue
    print(f"fix_worksheet: roll_col_name: {roll_col_name}. col_no: {col_no}.")
    if roll_col_name == '' or col_no is None or len(cols) != 2:
        # This table is not in the format for this function to do anything.
        print(f"fix_worksheet: This table does not have format that needs data "
              f"repair. Returning original table.")
        return table
    else:
        if table.iloc[col_no, 0] is None:
            table.iloc[col_no, 0] = 1
            print(f"fix_worksheet: updated table: {table}.")
        return table


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
            error_msg = (f"roll_test: Attempt to convert low part of {s} "
                         f"failed because it has an invalid format. Format is "
                         f"m or m-n, where m,n are positive integers "
                         f"such m <= n. 0, 00, or 000 will fail the test.")
            print(error_msg)
            return (False,)
        else:
            if len(l) == 2:
                try:
                    high = int(l[1])
                except ValueError:
                    error_msg = (f"roll_test: Attempt to convert high part of {s} "
                                 f"failed because it has an invalid format. Format is "
                                 f"m or m-n, where m,n are positive integers "
                                 f"such m <= n. 0, 00, or 000 will fail the test.")
                    print(error_msg)
                    return (False,)
                else:
                    if low > high:
                        error_msg = (f"roll_test: Sequence test of {s} failed "
                                     f"because it has invalid format. Format is "
                                     f"m or m-n, where m,n are positive integers "
                                     f"such m <= n. Do not use 0, 00, or 000 for "
                                     f"end values.")
                        print(error_msg)
                        return (False,)
                    elif low == high:
                        return (low,)
                    else:
                        return low, high
            elif len(l) == 1:
                return (low,)
            else:
                error_msg = (f"roll_test: Integer test failes because {s} has "
                             f"invalid format. Must be"
                             f"m or m-n, where m,n are positive integers "
                             f"such m <= n. Do not use 0, 00, or 000 for "
                             f"end values.")
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


def check_worksheet(table, stat_values=False, other_valuables=False) -> bool:
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

    other_valuables is a bool used to override the usual behavior of this
    function. Gem and Other Valuables Tables have a 3 column format, with
    a roll column (dice type header with single values or a range of two
    integers in the Series), a 'gemstone' or 'valuable' column (header
    transformed to lowercase matches 'gemstone' or 'valuable' with strings
    for the Series values), and 'description' or 'example' column (header
    transformed to lowercase matches 'description' or 'example' with strings
    for the Series values).

    This function returns a bool, True if the worksheet is usable, False
    otherwise.
    :param table: pd.DataFrame
    :param stat_values: bool, defaults to False, used to override the
        usual behavior and treat the first column as a d30 stat, running
        from 1 to 30
    :param other_valuables: bool, defaults to False, used to override the
        behaviour and treat the format as 3-columns for gems or other
        valuables
    :return: bool
    """
    headers = table.columns
    if stat_values:
        # This is a stopgap until this feature is programmed.
        return True
    elif other_valuables:
        # These tables have one of two legit formats. Both share a column
        # that handles a dice roll. The gems tables use a 'gemstone' column
        # followed by a 'description' column. The second format uses a
        # 'valuable' column, followed by an 'example' column. The text
        # columns simply need to be non-empty so that something can be
        # displayed in the GUI.
        if len(headers) != 3:
            print(f"check_worksheet: Invalid Format: Invalid number of columns "
                  f"for gem or other valuables tables: {len(headers)}. It should "
                  f"be 3.")
            return False
        roll_max = _check_roll_column(headers)
        if roll_max is None:
            print(f"check_worksheet: Invalid Format: First column is not a roll "
                  f"column or has an invalid header: {headers[0]}.")
            return False

        # Next, we check the remaining headers for the correct format.
        col2_header = headers[1].lower()
        col3_header = headers[2].lower()
        if 'gemstone' not in col2_header and 'valuable' not in col2_header:
            print(f"check_worksheet: Invalid Format: Second column must contain "
                  f"either 'gemstone' or 'valuable' to be valid. Instead, it "
                  f"is {headers[1]}.")
            return False
        if 'description' not in col3_header and 'example' not in col3_header:
            print(f"check_worksheet: Invalid Format: Second column must contain "
                  f"either 'description' or 'example' to be valid. Instead, it "
                  f"is {headers[2]}.")
            return False

        # We need to make sure that the 2nd and 3rd column headers agree.
        if 'gemstone' in col2_header and 'description' not in col3_header:
            print(f"check_worksheet: Invalid Format: Column 2 and 3 headers "
                  f"do not agree on type of item. Column 2 is {headers[1]}, "
                  f"but Column 3 header does not contain 'description. It "
                  f"contains {headers[2]}.")
            return False
        if 'valuable' in col2_header and 'example' not in col3_header:
            print(f"check_worksheet: Invalid Format: Column 2 and 3 headers "
                  f"do not agree on type of item. Column 2 is {headers[1]}, "
                  f"but Column 3 header does not contain 'example'. It "
                  f"contains {headers[2]}.")
            return False

        # The headers are correct. There cannot be any NoneType or blank ('')
        # contents in the Series for the second and third header.
        col2_series = table[headers[1]]
        col3_series = table[headers[2]]
        col2_nulls = col2_series.dropna()
        col3_nulls = col3_series.dropna()
        if len(col2_nulls) != len(col2_series):
            print(f"check_worksheet: Invalid Format: Column 2 cannot have "
                  f"NaN, null, or NoneType entries. A blank string is "
                  f"acceptable, but not recommended.")
            return False
        if len(col3_nulls) != len(col3_series):
            print(f"check_worksheet: Invalid Format: Column 3 cannot have "
                  f"NaN, null, or NoneType entries. A blank string is "
                  f"acceptable, but not recommended.")
            return False
        return True
    else:
        if len(headers) != 2:
            print(f"check_worksheet: Invalid Format: Invalid number of columns "
                  f"for normal tables: {len(headers)}. It should be 2.")
            return False

        roll_max = _check_roll_column(headers)
        if roll_max is None:
            print(f"check_worksheet: Invalid Format: First column is not a roll "
                  f"column or has an invalid header: {headers[0]}.")
            return False

        roll_header = headers[0]
        desc_header = headers[1]
        roll_column = table[roll_header]
        desc_column = table[desc_header]
        print(f"check_worksheet: roll_max: {roll_max}.")
        print(f"check_worksheet: roll_header: {roll_header}. roll_column: {roll_column}.")
        print(f"check_worksheet: desc_header: {desc_header}. desc_column: {desc_column}.")
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


def _check_roll_column(cols: list):
    """
    This function receive a list of column headers and returns one that is a
    roll column and returns either None if a valid roll header is not found
    or the actual dice value as an integer.
    :param cols:
    :return:
    """
    # Roll column needs to be first column. If not, the format is invalid.
    possible_roll_values = ('d1000', 'd100', 'd30', 'd20',
                            'd12', 'd10', 'd8', 'd6',
                            'd4', 'd2')
    roll_header = cols[0]
    roll_header_clean = roll_header.lower().strip()
    print(f"_check_roll_column: roll_header: {roll_header}. "
          f"roll_header_clean: {roll_header_clean}.")

    if roll_header_clean in possible_roll_values:
        roll_type = roll_header.lower().strip()
        roll_max = int(roll_type[1:])
        print(f"_check_roll_column: roll_max: {roll_max}.")
    else:
        if roll_header_clean[0] != 'd':
            print(f"_check_roll_column: Invalid Format: Roll column has an "
                  f"invalid header, {roll_header}.")
            return None
        else:
            try:
                roll_max = int(roll_header_clean[1:])
            except ValueError:
                print(f"_find_roll_column: Invalid Format: Roll column has an "
                      f"invalid header, {roll_header}.")
                return None
    return roll_max


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
               'Treasure For CR 0 Coin', 'Treasure For CR 5 Coin']
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
