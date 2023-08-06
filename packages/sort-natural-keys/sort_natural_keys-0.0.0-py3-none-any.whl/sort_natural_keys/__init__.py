import re

# Inspired from: https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def sort_natural_keys_number(arr):
    """
    Sorts with natural keys an array of string containing numbers.
    The array is sorted in place and is returned

    Parameters:
        arr:    array of strings
    
    Returns:
        arr:    array of strings sorted
    """
    arr.sort(key=natural_keys)
    return arr

