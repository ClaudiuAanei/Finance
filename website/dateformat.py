

def change_date_format(calendar_day, date_format):
    if calendar_day:
        calendar_keys = ['yyyy', 'mm', 'dd']
        calendar_values = calendar_day.split('-')
        print(calendar_values)
        dictionary = dict(zip(calendar_keys, calendar_values))
        print(dictionary)

        sep = detect_separator(date_format)
        print(date_format)
        date_format_list = date_format.split(sep)
        print(date_format_list)

        new_format = []
        for i in date_format_list:
            new_format.append(dictionary[i])

        return f"{sep}".join(new_format)

    else:

        return None


def detect_separator(date_str):
    for sep in ['-', '/', '.', ' ']:
        if sep in date_str:
            return sep
    return None



if __name__ == '__main__':
    print(change_date_format('2025-05-13', 'dd/mm/yyyy'))