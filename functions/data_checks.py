import os.path

import pandas as pd


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
    elif isinstance(s, bool):
        raise ValueError(f"roll_test: argument cannot be bool type.")
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
