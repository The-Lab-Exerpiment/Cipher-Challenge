from generic_functions import strip_text
from frequency_functions import FastTetragramFitness as ftt, tetragram_fitness
from cipher_files import open_file_as_dict
from random import randint, shuffle
from frequency_constants import per_letter_frequency
from time import sleep


def monoalphabetic_substitution(string: str, key: list[int]) -> str:
    result = ""
    for letter in string:
        result += chr(key[ord(letter) - 65] + 65)
    return result


def chr_codes_transform(string: str) -> list[int]:
    res = []
    for letter in string:
        res.append(ord(letter) - 65)
    return res


def hill_climbing_attack(
    string: str, key: list[int], character_indices: list[list[int]]
):
    text = chr_codes_transform(monoalphabetic_substitution(string, key))
    fitness = ftt.fast_tetragram_fitness(text)
    counter = 0
    x = 0
    y = 0
    while counter < 10_000:
        x, y = randint(0, 25), randint(0, 25)
        first_character = key[x]
        second_character = key[y]
        for index in character_indices[first_character]:
            text[index] = second_character
        for index in character_indices[second_character]:
            text[index] = first_character
        new_fitness = ftt.fast_tetragram_fitness(text)

        if new_fitness > fitness:
            fitness = new_fitness
            counter = 0
            key[x] = second_character
            key[y] = first_character
            character_indices[first_character], character_indices[second_character] = (
                character_indices[second_character],
                character_indices[first_character],
            )
        else:
            for index in character_indices[first_character]:
                text[index] = first_character
            for index in character_indices[second_character]:
                text[index] = second_character
        counter += 1
    return text, key, fitness


alpha = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
alpha = [ord(x) - 65 for x in alpha]

text_input = strip_text(str.upper(input()))
character_indices = [[] for _ in range(26)]


expected_tetragram = open_file_as_dict("frequency_data/tetragrams.json")
total_frequency = sum(expected_tetragram.values())


for index, val in enumerate(text_input):
    character_indices[ord(val) - 65].append(index)
ftt.compute_log_frequencies("frequency_data/tetragrams.json")
print(ftt.fast_tetragram_fitness([ord(x) - 65 for x in text_input]))
print(tetragram_fitness(text_input, expected_tetragram, total_frequency))

max_fitness = -float("inf")
best_text = ""
max_key = ""
for _ in range(200):
    shuffle(alpha)
    text, key, fitness = hill_climbing_attack(text_input, alpha[:], character_indices)
    if fitness > max_fitness:
        best_text = text
        max_fitness = fitness
        max_key = key
        print("Better fit found:")
        print("".join([chr(65 + x) for x in best_text]))
        print("Using key " + "".join([chr(x + 65) for x in key]))
        print("")
