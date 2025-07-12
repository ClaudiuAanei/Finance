

def change_date_format(calendar_day, date_format):
    """
    Converts a date string from one format to another.

    This function takes a date string and a target format string. It first
    infers the structure of the input date string and then rearranges its
    components (year, month, day) to match the desired output format.

    Args:
        calendar_day (str): The input date string (e.g., '2025-12-03').
        date_format (str): The desired output format (e.g., 'dd/mm/yyyy').

    Returns:
        str or None: The newly formatted date string, or None if the
                     input date is empty.
    """
    if calendar_day:
        calendar_keys = ['yyyy', 'mm', 'dd']
        calendar_values = calendar_day.split(detect_separator(calendar_day))

        dictionary = dict(zip(calendar_keys, calendar_values))

        sep = detect_separator(date_format)
        date_format_list = date_format.split(sep)

        new_format = [dictionary[i] for i in date_format_list]

        return f"{sep}".join(new_format)

    else:

        return None


def detect_separator(date_str):
    for sep in ['-', '/', '.', ' ']:
        if sep in date_str:
            return sep

    return None



if __name__ == '__main__':
    print(change_date_format('2025-12-03', 'dd/mm/yyyy'))