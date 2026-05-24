import json


def read_json():

    with open("test_data/search_data.json") as file:
        return json.load(file)