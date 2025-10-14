import json
from os.path import isfile, isdir
from os import listdir, getcwd
from generic_functions import strip_text


def save_dict_to_file(dictionary: dict, file_name: str):
    with open(file_name, "w") as file:
        json.dump(dictionary, file)


def open_file_as_dict(file_name: str) -> dict:
    with open(file_name, "r") as file:
        return json.load(file)


def cleanse_file(file_name: str) -> str:
    return strip_text("".join(open(file_name, "r").readlines()))


def save_list_to_file(l: set | list, file_name: str):
    with open(file_name, "w") as file:
        json.dump(list(l), file)


def open_file_as_set(file_name: str):
    with open(file_name, "r") as file:
        return set(json.load(file))


def open_file_as_list(file_name: str):
    with open(file_name, "r") as file:
        return list(json.load(file))


def get_log_file_name(
    target_file: str, file_extension: str = ""
) -> str:  # should not be used - create a subdirectory in a logging directory and place files in that
    directory, target_file_name = target_file.split("/")
    if not directory:
        raise Exception("Attempting to create log files in current working directory")
    if target_file.count("/") > 1:
        raise Exception(
            "Have not implemented logging in subdirectories with a depth of >1"
        )
    files_in_path = [
        file.split(".")[0]
        for file in listdir(getcwd() + "/" + directory)
        if isfile(getcwd() + "/" + directory + "/" + file)
    ]
    temp = [
        "".join(
            [letter if str.isalpha(letter) or letter == "_" else "" for letter in file]
        )
        for file in files_in_path
    ]
    n_max = -1
    if target_file_name in temp:
        for index in range(len(files_in_path)):
            if temp[index] == target_file_name:
                n_max = max(n_max, int(files_in_path[index][len(target_file_name) :]))
    if file_extension:
        return f"{target_file}{n_max + 1}.{file_extension}"
    return f"{target_file}{n_max + 1}"


def get_log_dir_name(target_directory: str) -> str:
    if target_directory.count("/") == 0:
        raise Exception(
            "Attempting to create a logging directory directly at a depth of 0"
        )
    logging_directory = "".join(target_directory.split("/")[-1])
    target_directory = getcwd() + "/" + "/".join(target_directory.split("/")[:-1])
    directories_in_path = [
        directory
        for directory in listdir(target_directory)
        if isdir(target_directory + "/" + directory)
    ]
    n_max = -1
    for directory in directories_in_path:
        parsed_directory = strip_text(directory, exceptions={"-", "_"})
        if logging_directory in parsed_directory:
            n_max = max(n_max, int(directory[len(logging_directory) :]))
    return f"{target_directory}/{logging_directory}{n_max + 1}"
