import json


def dict_to_file(dictionary: dict, file_name: str):
    with open(file_name, "w") as file:
        json.dump(dictionary, file)


def open_file_as_dict(file_name: str) -> dict:
    with open(file_name, "r") as file:
        return json.load(file)
