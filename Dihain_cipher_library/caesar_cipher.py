from os import mkdir
import matplotlib.pyplot as plt
from frequency_functions import (
    get_english_frequency,
    monograms_angle_cosine,
    monograms_chi_squared,
)
from generic_functions import normalise_value
from cipher_files import save_list_to_file, get_log_dir_name
from frequency_constants import per_letter_frequency
from plotting_functions import plot_bar_chart, save_figure_as_svg


def caesar_cipher(s: str, key: int = 1) -> str:
    string = list(s)
    for index, character in enumerate(string):
        character = ord(character)
        is_character = ((character >= 65) and (character <= 90)) or 2 * (
            (character >= 97) and (character <= 122)
        )
        if is_character:
            string[index] = chr(
                ((ord(string[index]) + key - 65 - 32 * (is_character - 1)) % 26)
                + 65
                + 32 * (is_character - 1)
            )
    return "".join(string)


def determine_text_with_most_english(texts: dict, dictionary: set) -> tuple[str, int]:
    text_with_most_english = ""
    english_frequency = -1
    for text in texts:
        if (f := get_english_frequency(text, dictionary)) > english_frequency:
            text_with_most_english = text
            english_frequency = f
    return (text_with_most_english, texts[text_with_most_english])  # (text, shift)


def attack(text: str):
    chi_squared, angles, max_chi, min_angle = (
        [0.0 for _ in range(26)],
        [0.0 for _ in range(26)],
        0,
        0,
    )

    for shift in range(0, 26):
        shifted_text = caesar_cipher(text, shift)
        chi_squared[shift] = monograms_chi_squared(shifted_text, per_letter_frequency)
        angles[shift] = monograms_angle_cosine(shifted_text, per_letter_frequency)
        max_chi = max(max_chi, chi_squared[shift])
        min_angle = max(min_angle, angles[shift])

    sorted_chi_squared = sorted(
        [(chi_squared[shift], shift) for shift in range(len(chi_squared))],  # type: ignore
        reverse=True,
    )
    sorted_angles = sorted(
        [(angles[shift], shift) for shift in range(len(angles))], reverse=True
    )  # type: ignore

    log_directory = get_log_dir_name("logs/caesar_cipher_logs/logs_")
    mkdir(log_directory)
    save_list_to_file(sorted_chi_squared, f"{log_directory}/chi_squared.txt")
    save_list_to_file(sorted_angles, f"{log_directory}/angles.txt")

    fig, ax = plot_bar_chart(
        [shift for shift in range(0, 26)],
        chi_squared,
        name_x="Shift Key",
        name_y="Chi Squared $(1/χ^2)$",
        title="Chi Squared Test for monogram fitness (Caesar Cipher)",
        color=plt.get_cmap("Reds")(
            [
                normalise_value(k, min(chi_squared), max(chi_squared))
                for k in chi_squared
            ]
        ),
    )
    save_figure_as_svg(fig, f"{log_directory}/chi_squared.svg")

    fig, ax = plot_bar_chart(
        [shift for shift in range(0, 26)],
        angles,
        name_x="Shift Key",
        name_y="Angle $(\\cos{θ})$",
        title="Angle between vectors for determining monogram fitness (Caesar Cipher)",
        color=plt.get_cmap("PuBu")(angles),
    )
    save_figure_as_svg(fig, f"{log_directory}/angles.svg")


attack(input())
