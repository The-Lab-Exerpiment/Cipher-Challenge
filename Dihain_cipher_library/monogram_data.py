from generic_functions import strip_text
from cipher_files import save_dict_to_file, get_log_dir_name
from plotting_functions import save_figure_as_svg, plot_bar_chart
from frequency_functions import per_letter_frequency, get_monograms
from os import mkdir


def create_monogram_logs(string: str):
    string = strip_text(string)
    monogram_data = get_monograms(string)

    fig, ax = plot_bar_chart(
        tuple(chr(a + 65) for a in range(26)),
        [
            monogram_data[chr(_ + 65)] if chr(_ + 65) in monogram_data else 0
            for _ in range(26)
        ],
        "Alphabet",
        "Frequency",
        "Monogram Frequency",
    )
    logging_directory = get_log_dir_name("logs/monogram_data/logs_")
    mkdir(logging_directory)
    save_figure_as_svg(fig, f"{logging_directory}/monogram_log.svg")
    save_dict_to_file(monogram_data, f"{logging_directory}/monogram_log")


create_monogram_logs(input())
