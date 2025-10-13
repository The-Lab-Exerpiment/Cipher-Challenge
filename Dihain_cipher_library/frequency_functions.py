import math
from frequency_constants import per_letter_frequency
from generic_functions import strip_text, remove_spaces


def get_monograms(
    string: str, function=str.upper, increment=str.isalpha, decimal=True
) -> dict:
    result_table = {}
    counter = 0

    for character in string:
        result_table[function(character)] = result_table.get(function(character), 0) + 1
        counter += increment(character)

    if decimal:
        for character in result_table:
            result_table[character] = (result_table[character]) / counter
    return result_table


def get_tetragrams(
    string: str, function=str.upper, increment=str.isalpha, decimal=True
) -> dict[str, float] | dict[str, int]:
    result_table: dict[str, float] | dict[str, int] = {string[:4]: 1}
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


def get_log_frequency_table(frequency_table: dict) -> dict:
    for character in frequency_table:
        frequency_table[character] = math.log(frequency_table[character]) + 1
    return frequency_table  # Implemented as asked by the unit - seems useless


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


def monograms_chi_squared(
    string: str,
    expected_set=per_letter_frequency,
    do_not_ignore=True,
) -> float:
    return 1 / chi_squared(
        get_monograms(strip_text(string)),
        expected_set,
        do_not_ignore=do_not_ignore,
    )


def dot_product(u_vector: dict, v_vector: dict) -> float:
    dot_product = 0
    for component in u_vector:
        dot_product += u_vector[component] * v_vector[component]
    return dot_product


def magnitude(vector: dict) -> float:
    return dot_product(vector, vector)


def angle_cosine(u_vector: dict, v_vector: dict) -> float:
    return dot_product(u_vector, v_vector) / (
        (magnitude(u_vector) * magnitude(v_vector)) ** 0.5
    )


def monograms_angle_cosine(string: str, v_vector: dict):
    return angle_cosine(get_monograms(strip_text(string)), v_vector)


def get_english_frequency(string: str, english_dictionary: set) -> float:
    words = string.split()
    counter = 0
    english_counter = 0
    for word in words:
        counter += 1
        english_counter += word in english_dictionary
    return english_counter / counter


def get_log_frequencies(frequency, total_frequency) -> float:
    return (
        math.log(frequency) - math.log(total_frequency)
    )  # equal to math.log(frequency/total_frequency) -> we can compute the frequency percentage without using division


def tetragram_fitness(actual_tetragrams: dict, expected_tetragrams: dict) -> float:
    total_frequency = sum(expected_tetragrams.values())
    fitness = 0
    contains_unlikely_tetragrams = 0
    for tetragram in actual_tetragrams:
        if tetragram in expected_tetragrams:
            fitness += actual_tetragrams[tetragram] * get_log_frequencies(
                expected_tetragrams[tetragram], total_frequency
            )
        else:  # the tetragram does not occur in the English language
            fitness += 0
            contains_unlikely_tetragrams += (
                1  # TODO: determine better action when unexpected tetragram is hit
            )
    fitness /= total_frequency
    return fitness


def get_n_grams(string: str, length: int) -> dict:  # no overlap
    n_gram_frequency = {}
    for index in range(0, len(string), length):
        if (index + length) > len(string):
            break  # if there aren't "length" remaining non overlapping character at the end of the string
        n_gram = string[index : index + length]
        n_gram_frequency[n_gram] = n_gram_frequency.get(n_gram, 0) + 1
    return n_gram_frequency


def index_of_coincidence(string: str, length_of_n_grams: int = 1) -> float:
    string = remove_spaces(string)
    n_gram_frequency = get_n_grams(string, length_of_n_grams)
    total_frequency = sum(n_gram_frequency.values())
    # print(n_gram_frequency, total_frequency)
    result = 0
    for n_gram in n_gram_frequency:
        count = n_gram_frequency[n_gram]
        result += (count * (count - 1)) / (total_frequency * (total_frequency - 1))
    return result * (26**length_of_n_grams)


def entropy(string: str = "", monograms: dict = {}) -> float:
    if not monograms:
        if string:
            monograms = get_monograms(string)
        else:
            raise Exception("Erroneous call to entropy function")
    return -sum(
        [monograms[letter] * math.log(monograms[letter], 26) for letter in monograms]
    )


# total_frequency = sum(expected_tetragrams.values())
