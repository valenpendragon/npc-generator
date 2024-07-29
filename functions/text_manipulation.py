def return_range(s, debug=False):
    """
    This function takes a string in one of two forms: n or m-n, where
    m and n are strings such that int(n) or int(m) is an integer. This
    can handle a situation where 'n-m' in actually integers with extra
    spaces surrounding the values.
    If debug is True, more complete debugging messages are shown in
    program output.
    :param s:
    :param debug: bool, defaults to False
    :return: tuple in the form (m, m) or (m, n)
    """
    print(f"return_range: s: {s}.")
    # First, make sure the string is not NoneType.
    if s is None:
        error_msg = (f"return_range: Fatal Error: The string cannot be "
                     f"NoneType.")
        raise TypeError(error_msg)

    # Second, check the string for integers and dashes.
    s = str(s)
    if debug:
        print(f"return_range: s: {s}.")
    # Remove blank spaces.
    s = s.replace(' ', '')
    if debug:
        print(f"return_range: s: {s}.")
    ctr = 0
    for c in s:
        if debug:
            print(f"return_range: c: {c}. ctr: {ctr}")
        if c != '-':
            try:
                n = int(c.strip())
            except ValueError:
                error_msg = (f"return_range: Fatal Error: All characters"
                             f" in the string must be integers with the"
                             f" exception of a single dash (-). Spaces are"
                             f" permitted, but no other characters.")
                raise ValueError(error_msg)
            else:
                continue
        else:
            ctr += 1
    if ctr > 1:
        error_msg = (f"return_range: Fatal Error: More than a pair of"
                     f" values was included in the string.")
        raise ValueError(error_msg)

    l = s.split('-')
    m = int(l[0].strip())
    if len(l) == 1:
        result = (m, m)
    else:
        n = int(l[1].strip())
        result = (m, n)

    print(f"return_range: result: {result}")
    return result