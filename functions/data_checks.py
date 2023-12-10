
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


if __name__ == "__main__":
    # Set test strings.
    l = ['blank', '10', '11-13', '12-10', '', 12, 12.4, '1-2-3' ]
    for item in l:
        print(f"Test results for {item} is {roll_test(item)}")
