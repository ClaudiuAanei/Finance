# import json
#
# def load_categories():
#
#     with open('categories.json', mode='r', encoding='utf-8') as f:
#         data = f.read()
#         categories = json.loads(data)
#
#     return categories
#
#
# my_list = [1, 2]
#
# def check_item():
#     try:
#         n = my_list[2]
#     except IndexError:
#         n = None
#
#     return n
#
# my_list.insert(3, 0)
# print(my_list)


def format_time(calendar_day, date_format):
    if calendar_day:
        calendar_keys = ['year', 'month', 'day']
        calendar_values = calendar_day.split('-')
        dictionary = dict(zip(calendar_keys, calendar_values))

        sep = detect_separator(date_format)
        date_form = date_format.split(sep)
        new_format = []
        for i in date_form:
            new_format.append(dictionary[i])

        return f"{sep}".join(new_format)

    else:

        return None


def detect_separator(date_str):
    for sep in ['-', '/', '.', ' ']:
        if sep in date_str:
            return sep
    return None


print(format_time('2025-05-16', "day/month/year"))

