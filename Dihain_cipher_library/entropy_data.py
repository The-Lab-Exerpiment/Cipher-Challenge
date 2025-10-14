from generic_functions import strip_text
from cipher_files import save_list_to_file, get_log_dir_name
from plotting_functions import save_figure_as_svg, plot_bar_chart
from frequency_functions import per_letter_frequency, entropy
from os import mkdir


def create_entropy_logs(string: str):
    string = strip_text(string)
    res = [entropy(string)]
    logging_directory = get_log_dir_name("logs/entropy_data/logs_")
    mkdir(logging_directory)
    save_list_to_file(res, f"{logging_directory}/entropy_log")


create_entropy_logs(input())
