import time


def timeit(func: function) -> function:
    """ Calculate and print execution time of a function into the standard output. """
    def wrapper(*args):
        start = time.time()
        result = func(*args)
        end = time.time()
        print("Execution time for \"" + str(func.func_name) + "\" : " + str(end - start) + " seconds")
        return result
    return wrapper


def is_a_float(s: str) -> bool:
    """ Check if a parsed string is a float.

        Example :
        >>> is_a_float("0.0")
        True
        >>> is_a_float("0.1")
        True
        >>> is_a_float("1.0")
        True
        >>> is_a_float("1.1")
        True
        >>> is_a_float("75")
        False
        >>> is_a_float("abcd")
        False
    """
    try:
        float(s)
        return "." in s
    except ValueError:
        return False


def is_an_int(s: str) -> bool:
    """ Check if a parsed string is an int.

        Example :
        >>> is_an_int("0.0")
        False
        >>> is_an_int("0.1")
        False
        >>> is_an_int("1.0")
        False
        >>> is_an_int("75")
        True
        >>> is_an_int("abcd")
        False
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_a_percentage(s: str) -> bool:
    """ Check if a parsed string is a percentage.

        Example :
        >>> is_a_percentage("0.0")
        True
        >>> is_a_percentage("0.1")
        True
        >>> is_a_percentage("1.0")
        True
        >>> is_a_percentage("1.1")
        False
        >>> is_a_percentage("75")
        False
        >>> is_a_percentage("abcd")
        False
    """
    return is_a_float(s) and 0.0 <= float(s) <= 1.0
