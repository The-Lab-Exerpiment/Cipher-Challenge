from generic_functions import modular_inverse
from frequency_constants import per_letter_frequency
from frequency_functions import (
    get_tetragrams,
    tetragram_fitness,
    monograms_angle_cosine,
    monograms_chi_squared,
)
from cipher_files import (
    open_file_as_dict,
    get_log_dir_name,
    save_list_to_file,
)
from os import mkdir
from plotting_functions import heatmap, annotate_heatmap, save_figure_as_svg
from typing import TypeAlias


def is_valid_key(a: int, b: int) -> bool:
    return modular_inverse(a, 26) is not None


def affine_cipher(string: str, a: int, b: int) -> str:
    if not is_valid_key(a, b):
        raise Exception(f"Invalid key for affine cipher: {a, b}")

    s: list[str] = list(string.upper())
    for index, character in enumerate(s):
        character = ord(character) - 65
        if 0 <= character <= 26:
            s[index] = chr(((a * ord(s[index])) % 26 + b) % 26 + 65)
    return "".join(s)


def decipher_affine_cipher(encoded_string: str, a: int, b: int) -> str:
    if not is_valid_key(a, b):
        raise Exception(f"Invalid for decoding an affine cipher: {a, b}")
    a_inv = modular_inverse(a, 26)
    string = list(encoded_string.upper())
    for index, character in enumerate(string):
        character = ord(character) - 65
        if 0 <= character <= 26:
            string[index] = chr((a_inv * ((character % 26) - b)) % 26 + 65)  # type: ignore
    return "".join(string)


def affine_to_mono_sub_key(a: int, b: int) -> str:
    key = ["" for _ in range(26)]
    for index in range(0, 26 * a, a):
        character_code = ((index % 26) + b) % 26
        key[int(index / 3)] = chr(character_code + 65)
    return "".join(key)


def generate_valid_keys() -> list[int]:
    coprime_a = [
        a for a in range(26) if is_valid_key(a, 0)
    ]  # gets all a coprime to 26 && a < 26
    return coprime_a


TetragramFitnesses: TypeAlias = list[list[float]]
TetragramLogs: TypeAlias = list[list[float, list[int, int]]]  # type: ignore


def tetragram_attack(
    string: str, valid_keys: list[int]
) -> tuple[TetragramFitnesses, TetragramLogs]:
    log_data: TetragramLogs = []
    tetragrams_fitnesses: list[list[float]] = [
        [0.0 for __ in range(26)] for _ in range(len(valid_keys))
    ]
    expected_tetragrams = open_file_as_dict("frequency_data/tetragrams.json")
    min_tetragram_fitness = float("inf")
    max_tetragram_fitness = -float("inf")
    for index in range(len(valid_keys)):
        for b in range(26):
            deciphered_text = decipher_affine_cipher(string, valid_keys[index], b)
            tetragrams_fitnesses[index][b] = tetragram_fitness(  # type: ignore
                get_tetragrams(deciphered_text, decimal=True), expected_tetragrams
            )
            # log_data.append([tetragrams_fitnesses[index][b], [valid_keys[index], b]])  # type: ignore
            min_tetragram_fitness = min(
                min_tetragram_fitness, tetragrams_fitnesses[index][b]
            )
            max_tetragram_fitness = max(
                max_tetragram_fitness, tetragrams_fitnesses[index][b]
            )
    # log_data = sorted(log_data, reverse=True)

    for index in range(
        len(valid_keys)
    ):  # normalising tetragrams fitnesses to 0-1 range
        for shift in range(26):
            tetragrams_fitnesses[index][shift] = (
                tetragrams_fitnesses[index][shift] - min_tetragram_fitness
            ) / (max_tetragram_fitness - min_tetragram_fitness)

    return (tetragrams_fitnesses, log_data)  # type: ignore


def monogram_attack(text: str, valid_keys: list[int]):
    chi_squared, angles = (
        [[0.0 for __ in range(26)] for _ in range(len(valid_keys))],
        [[0.0 for __ in range(26)] for _ in range(len(valid_keys))],
    )
    chi_squared_log_data = []
    angles_log_data = []
    for index in range(len(valid_keys)):
        for shift in range(0, 26):
            shifted_text = decipher_affine_cipher(text, valid_keys[index], shift)
            chi_squared[index][shift] = monograms_chi_squared(
                shifted_text, per_letter_frequency
            )
            angles[index][shift] = monograms_angle_cosine(
                shifted_text, per_letter_frequency
            )
            chi_squared_log_data.append(
                [chi_squared[index][shift], [valid_keys[index], shift]]
            )
            angles_log_data.append([angles[index][shift], [valid_keys[index], shift]])

    chi_squared_log_data = sorted(
        [
            (chi_squared_log_data[shift], shift)
            for shift in range(len(chi_squared_log_data))
        ],  # type: ignore
        reverse=True,
    )
    angles_log_data = sorted(
        [(angles_log_data[shift], shift) for shift in range(len(angles_log_data))],
        reverse=True,
    )  # type: ignore

    return (chi_squared, angles, chi_squared_log_data, angles_log_data)


def attack(string: str):
    valid_keys = generate_valid_keys()
    tetragram_fitnesses, tetragram_log_data = tetragram_attack(string, valid_keys)
    chi_squared, angles, chi_squared_log_data, angles_log_data = monogram_attack(
        string, valid_keys
    )
    log_directory = get_log_dir_name("logs/affine_cipher_logs/log_")
    mkdir(log_directory)
    save_list_to_file(tetragram_log_data, f"{log_directory}/tetragram_fitness_log")
    save_list_to_file(chi_squared_log_data, f"{log_directory}/chi_squared_log")
    save_list_to_file(angles_log_data, f"{log_directory}/angles_log")

    fig, im, _ = heatmap(
        tetragram_fitnesses[::-1],
        [str(k) for k in valid_keys][::-1],
        [str(_) for _ in range(26)],
        title="Normalised Average Tetragram Fitness (Affine Cipher)",
        name_x="Shift ($b$)",
        name_y="Multiplier ($a$)",
    )
    annotate_heatmap(im)
    save_figure_as_svg(fig, f"{log_directory}/tetragram_fitness.svg")

    fig, im, _ = heatmap(
        chi_squared[::-1],
        [str(k) for k in valid_keys][::-1],
        [str(_) for _ in range(26)],
        title="Monogram fitness determined using Chi Squared Test (Affine Cipher)",
        name_x="Shift ($b$)",
        name_y="Multiplier ($a$)",
    )
    annotate_heatmap(im)
    save_figure_as_svg(fig, f"{log_directory}/chi_squared.svg")

    fig, im, _ = heatmap(
        angles[::-1],
        [str(k) for k in valid_keys][::-1],
        [str(_) for _ in range(26)],
        title="Monogram fitness determined using Angle between Vectors (Affine Cipher)",
        name_x="Shift ($b$)",
        name_y="Multiplier ($a$)",
    )
    annotate_heatmap(im)
    save_figure_as_svg(fig, f"{log_directory}/angles.svg")


attack(input())
