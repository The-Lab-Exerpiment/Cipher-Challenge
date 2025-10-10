import cipher_files
from generic_functions import remove_spaces
from frequency_constants import per_letter_frequency
import math


def get_monograms(string: str, function=str.upper, increment=str.isalpha) -> dict:
    result_table = {}
    counter = 0

    for character in string:
        result_table[function(character)] = result_table.get(function(character), 0) + 1
        counter += increment(character)

    for character in result_table:
        result_table[character] = (result_table[character]) / counter
    return result_table


def get_tetragrams(
    string: str, function=str.upper, increment=str.isalpha, decimal=True
) -> dict:
    result_table = {}
    tetragram = string[:4]
    counter = 0

    for index in range(4, len(string)):
        tetragram = tetragram[1:] + string[index]
        result_table[function(tetragram)] = result_table.get(function(tetragram), 0) + 1
        counter += increment(tetragram)

    if decimal:
        for character in result_table:
            result_table[character] = (result_table[character]) / counter
    return result_table


def get_log_frequency_table_from_percentages(frequency_table: dict) -> dict:
    for character in frequency_table:
        frequency_table[character] = math.log(frequency_table[character]) + 1
    return frequency_table


def chi_squared(actual_set: dict, expected_set: dict, do_not_ignore=True) -> float:
    chi_squared_statistic = 0
    for key in actual_set:
        if key in expected_set:
            chi_squared_statistic += ((actual_set[key] - expected_set[key]) ** 2) / (
                expected_set[key]
            )
        elif do_not_ignore:
            raise Exception(
                "chi_squared function: the expected_set does not contain all the data values within the actual_set"
            )
    return chi_squared_statistic


def determine_monogram_fitness_using_chi_squared(
    string: str, expected_set=per_letter_frequency, function=remove_spaces
):
    return 1 / chi_squared(get_monograms(remove_spaces(string)), per_letter_frequency)


def dot_product(u_vector: dict, v_vector: dict):
    dot_product = 0
    for component in u_vector:
        dot_product += u_vector[component] * v_vector[component]
    return dot_product


def length_of_vector(vector: dict):
    return dot_product(vector, vector)


def angle_between_vectors(u_vector: dict, v_vector: dict):
    return dot_product(u_vector, v_vector) / (
        (length_of_vector(u_vector) * length_of_vector(v_vector)) ** 0.5
    )


def determine_monogram_fitness_using_angle_between_vectors(
    u_vector: dict, v_vector: dict, do_not_ignore=True
):
    return angle_between_vectors(u_vector, v_vector)


def get_log_frequencies_from_frequency(frequency, total_frequency):
    return math.log(frequency) - math.log(total_frequency)


def tetragram_fitness(actual_tetragrams: dict, expected_tetragrams: dict):
    total_frequency = sum(expected_tetragrams.values())
    fitness = 0
    for tetragram in actual_tetragrams:
        if tetragram in expected_tetragrams:
            fitness += actual_tetragrams[
                tetragram
            ] * get_log_frequencies_from_frequency(
                expected_tetragrams[tetragram], total_frequency
            )
        else:  # the tetragram does not occur in the English language
            fitness += 0
    fitness /= sum(actual_tetragrams.values())
    return fitness


expected_tetragrams = cipher_files.open_file_as_dict("tetragrams.json")
total_frequency = sum(expected_tetragrams.values())
