import json


def load_data_from_json_file(filename):
    with open(f"preload_data/{filename}", "r", encoding='utf8') as f:
        result = json.load(f)
    return result


def load_categories():
    return load_data_from_json_file('categories.json')


def load_meals():
    return load_data_from_json_file('meals.json')