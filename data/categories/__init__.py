import json
import os

categories_dict = {}


def get_subcategories_items(subcat) -> list[str]:
    # if user provided category contents
    # a subcategories with child nodes
    result_text_array = []
    if isinstance(subcat, dict):
        for key, value in subcat.items():
            result_text_array.append(key)
    # if user provided category contents
    # a subcategories without child nodes
    elif isinstance(subcat, list):
        result_text_array = subcat
    return result_text_array



def read_json(path: str) -> str:
    global categories_dict
    with open(path, 'r', encoding='utf-8') as file:
        categories = json.load(file)
        categories_dict = categories
        text = ''
        for category, content in categories.items():
            text = text + '/' + category + '\n'
    file.close()
    return text


start = os.getcwd()
categories_text = read_json(start+"/data/categories/categories.json")
