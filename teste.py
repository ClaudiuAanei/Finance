import json

def load_categories():

    with open('categories.json', mode='r', encoding='utf-8') as f:
        data = f.read()
        categories = json.loads(data)

    return categories


my_list = [1, 2]

def check_item():
    try:
        n = my_list[2]
    except IndexError:
        n = None

    return n

check_item()