def return_range(s):
    """
    This function takes a string in one of two forms: n or m-n, where
    m and n are strings such that int(n) or int(m) is an integer.
    :param s:
    :return: tuple in the form (m, m) or (m, n)
    """
    # First, check the string for integers and dashes.
    s = str(s)
    ctr = 0
    for c in s:
        if c != '-':
            try:
                n = int(c)
            except ValueError:
                error_msg = (f"return_range: Fatal Error: All characters"
                             f" in the string must be integers with the"
                             f" exception of a single dash (-).")
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
    m = int(l[0])
    if len(l) == 1:
        return (m, m)
    else:
        n = int(l[1])
        return (m, n)
