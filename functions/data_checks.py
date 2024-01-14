import os.path
import pandas as pd
import numpy as np


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


def check_worksheet(table: pd.read_table) -> bool:
    """
    This function analyzes the table supplied to it. There may be index
    columns which will be ignored. The focus is on roll columns and
    description columns. The former should have a header indicating the
    type of dice to be used. The latter is text describing a result. Either
    column may have entries listed as None. For the roll column, that
    indicates the result in the description is not possible. For the
    description column, that means that the roll value or range produces
    nothing. Note: A Dash in a column will be treated as a blank entry.

    The roll columns are the part that requires carefully validation.
    There can be blank values in a roll column, but numbers must be sequential
    otherwise. There can be no duplication of values from row to row, no
    overlaps, and no gaps. Otherwise, the table is not usable.

    This function returns a bool, True if the worksheet is usable, False
    otherwise.
    :param table: pd.DataFrame
    :return: bool
    """
    headers = table.columns
    # Find the roll column first. All unnamed columns will be ignored.
    # The order of the possible values ensures the largest match will
    # be the first one found.
    possible_roll_values = ('d1000', 'd100', 'd30', 'd20',
                            'd12', 'd10', 'd8', 'd6',
                            'd4', 'd2')
    roll_header = None
    roll_type = None
    for h in headers:
        for v in possible_roll_values:
            if v in h.lower().strip():
                roll_type = v
                roll_header = h
                break
    if roll_header is None:
        # There is no roll column that matches the criteria.
        print("check_worksheet: No roll column founds Table is an invalid format.")
        return False
    else:
        roll_column = table[roll_header]
    roll_max = int(roll_type[1:])
    print(f"check_worksheet: roll_header: {roll_header}. roll_type: {roll_type}. "
          f"roll_max: {roll_max}. roll_column: {roll_column}.")
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
                return False
            else:
                if last_val + 1 != item_ck[0]:
                    # There is a gap or an overlap.
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
        return  False
    else:
        return True


# TODO: Create check_worksheet to verify that the numbering in the table
#  is consistent with the column header of the table and has no gaps or
#  overlaps in the numbering.
if __name__ == "__main__":
    # Set test strings.
    l = ['blank', '10', '11-13', '12-10', '', 12, 12.4, '1-2-3' ]
    for item in l:
        print(f"Test results for {item} is {roll_test(item)}")
    # TODO: Add tests for check_workbook and find_workbooks using
    #  sample files included in data directory.
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
