#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy.random
import re
from .colored_output import *
from ..time_utils import *
from ..common_utils import *


__all__ = ["print_bar", "print_title", "print_section_title", "print_error", "print_warning", "print_success",
           "print_log", "progress_bar", "print_sub_variables", "print_variables", "print_final_value",
           "test_moving_progress_bar", "ask_question_yes_or_no", "pretty_print_dict", "get_print_prefix",
           "print_log_progress_bar"]


def print_bar(length: int = 100, start="", end="\n"):
    print(start + "-" * length + "\n", end=end)


def print_title(title: str, color: str = Color.blue):
    main_color = f"{Color.bold}{Color.underline}{color}"
    title = title.replace(Color.reset, f"{Color.reset}{main_color}")

    whole_len = 100
    for line in title.splitlines():
        len_line = len(remove_colors(line))
        whole_len = max(whole_len, len_line + 10)

    print()
    print_bar(whole_len)
    for line in title.splitlines():
        len_line = len(remove_colors(line))
        empty_len = whole_len - len_line
        print(" " * (empty_len//2) + main_color + line + Color.reset + " " * (empty_len - empty_len//2) + NBSP)
    print()
    print_bar(whole_len)


def print_section_title(title: str):
    main_color = f"{Color.bold}{Color.underline}{Color.beige}"
    title = title.replace(Color.reset, f"{Color.reset}{main_color}")
    title = title.replace("\n", f"{Color.reset}{NBSP}\n{main_color}")
    print("\n" + main_color + title + Color.reset + NBSP)


def print_error(*args, end: str = "\n", no_newline: bool = False, no_prefix: bool = False):
    main_color = Color.light_red
    if not no_newline and not no_prefix:
        print("\n", end="")
    if not no_prefix:
        print(f"{csi_bg_color(main_color)}{Color.black}Error{Color.reset}{main_color}: ", end="")
    print(f"{main_color}", end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") if isinstance(arg, str) else arg
            for arg in args)
    print(*args, end="")
    print(f"{Color.reset}", end=end)


def print_warning(*args, end: str = "\n", no_newline: bool = False, no_prefix: bool = False):
    main_color = Color.orange
    if not no_newline and not no_prefix:
        print("\n", end="")
    if not no_prefix:
        print(f"{csi_bg_color(main_color)}{Color.black}Warning{Color.reset}{main_color}: ", end="")
    print(f"{main_color}", end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") if isinstance(arg, str) else arg
            for arg in args)
    print(*args, end="")
    print(f"{Color.reset}", end=end)


def print_success(*args, end: str = "\n", no_newline: bool = False, no_prefix: bool = True):
    main_color = Color.vivid_green
    if not no_newline:
        print("\n", end="")
    if not no_prefix:
        print(f"{csi_bg_color(main_color)}{Color.black}Success{Color.reset}{main_color}: ", end="")
    print(f"{main_color}", end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") if isinstance(arg, str) else arg
            for arg in args)
    print(*args, end="")
    print(f"{Color.reset}\n", end=end)


def print_log(*args, end: str = "\n"):
    main_color = Color.grey_blue
    print(main_color, end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") if isinstance(arg, str) else arg
            for arg in args)
    print(*args, end="")
    print(Color.reset, end=end)


G_LAST_COLOR_INDEX = 0
G_START_TIME = 0
G_NEXT_EXEC_TIME = None
C_PROBA = .1
G_COIN_FLIP = numpy.random.random() < C_PROBA


def progress_bar(i: int, max_nb: int, end: bool = False, only_bar: bool = False,
                 sliding_rainbow: bool = True, static_rainbow: bool = False):
    global G_LAST_COLOR_INDEX, G_START_TIME, G_COIN_FLIP, G_NEXT_EXEC_TIME
    colors = Color.rainbow if not G_COIN_FLIP else Color.progress_pride
    full_cell_char = "█"
    full_len = len(colors)
    percent = i / max_nb
    nb_char = int(percent*full_len)

    if sliding_rainbow and not static_rainbow:
        s = "|"
        for num_color_index in range(nb_char):
            color = colors[(G_LAST_COLOR_INDEX + num_color_index) % full_len] if not end else Color.reset
            s += color + full_cell_char
        s += Color.reset + " "*(full_len-nb_char) + "|"
        current_time = time.perf_counter()
        if G_NEXT_EXEC_TIME is None or current_time > G_NEXT_EXEC_TIME:
            G_NEXT_EXEC_TIME = current_time + 0.08
            G_LAST_COLOR_INDEX = (G_LAST_COLOR_INDEX - 1) % full_len if not end else 0
    else:
        if static_rainbow:
            color = colors[int(percent*(full_len-1))]
        else:
            color = colors[G_LAST_COLOR_INDEX] if not end else Color.reset
        s = "|" + color + full_cell_char*nb_char + " "*(full_len-nb_char) + Color.reset + "|"
        current_time = time.perf_counter()
        if G_NEXT_EXEC_TIME is None or current_time > G_NEXT_EXEC_TIME:
            G_NEXT_EXEC_TIME = current_time + 0.08
            G_LAST_COLOR_INDEX = (G_LAST_COLOR_INDEX + 1) % full_len if not end else 0
    if not only_bar:
        s += f" {Color.default}{percent:>7.2%}{Color.reset} " + " "*(len(str(max_nb))-len(str(i))) + f"({i}/{max_nb})"

    # Timer
    current_time = time.perf_counter()
    # elapsed_time = format_timespan(current_time - G_START_TIME)
    elapsed_time = format_timespan_simple(current_time - G_START_TIME)
    if end:
        s += f" (total elapsed time: {elapsed_time})"
        G_START_TIME = time.perf_counter()
        G_COIN_FLIP = numpy.random.random() < C_PROBA
    else:
        s += f" (elapsed time: {elapsed_time})"
    return s


def print_log_progress_bar(i: int, max_nb: int, sentence: str, end: bool = False):
    line = f"\r{progress_bar(i, max_nb, end=end)} {sentence.strip()}"
    # Remove any period character at the end of the sentence, so that it is either "..." while processing
    # and a final period "." when finished (end=True).
    line = re.sub(r"\.*$", r"", line)
    if not end:
        line += "..."
    else:
        line += "."

    # While processing, print with no end character so the carriage return \r works and the progress bar
    # visually progresses and when finished (end=True), print with 2 line feed \n so that it passes a blank line.
    if not end:
        print_log(line, end="")
    else:
        print_log(line, end="\n\n")


def test_moving_progress_bar():
    progress_bar(1, 1, end=True)  # reset progress bar
    len_colors = len(Color.rainbow) if not G_COIN_FLIP else len(Color.progress_pride)
    initial_time = 1000 * time.perf_counter()
    delay = 80  # every 80 ms
    next_exec_time = initial_time
    nb_ite = 0
    while True:
        current_time = 1000 * time.perf_counter()
        if current_time > next_exec_time:
            nb_ite += 1
            next_exec_time += delay
            print_log(f"\r{progress_bar(1, 1, only_bar=True)}", end="")
            if nb_ite > 30 and nb_ite % len_colors == 1:  # around 2.4 s and wait until a whole loop haas passed
                break
    print("\n")


def print_sub_variables(all_sub_variables: dict[str, str]):
    for var_name, var_value in _modify_variables_to_print(all_sub_variables).items():
        print(f"\t\t\t{var_name} = {Color.white}{var_value}{Color.reset}")


def print_variables(variables: dict[str, str]):
    for var_name, var_value in _modify_variables_to_print(variables).items():
        print(f"\t\t{Color.pink}{var_name}{Color.reset} = {Color.pale_pink}{var_value}{Color.reset}")


def print_final_value(final_value: dict[str, str]):
    for var_name, var_value in _modify_variables_to_print(final_value).items():
        print(f" --> {Color.yellow}{var_name}{Color.reset} = {Color.light_yellow}{var_value}{Color.reset}\n")


def _modify_variables_to_print(variables: dict[str, str]):
    dict_to_print = dict()
    for var_name in sorted(variables):
        if not isinstance(variables[var_name], str):
            print(var_name)
        dict_to_print[var_name] = variables[var_name].replace("^2", "²").replace("^3", "³")
    return dict_to_print


def ask_question_yes_or_no(question: str) -> bool:
    while (answer := (input(f"{Color.yellow}{question}{Color.reset} "
                            f"{Color.light_yellow}(Y/N){Color.reset} ").upper().strip())
           ) not in ["Y", "YES", "N", "NO"]:
        pass

    return answer in ["Y", "YES"]


def pretty_print_dict(in_dict: Union[dict, list], lvl: int = 0, max_lvl: int = None) -> None:
    lvl += 1
    if isinstance(in_dict, list):
        for key in in_dict:
            print(key)
        return
    if not isinstance(in_dict, dict):
        print(in_dict)
        return
    for key, val in in_dict.items():
        print(f"{get_print_prefix(lvl)}> {key}")
        if isinstance(val, dict):
            if max_lvl is None or lvl <= max_lvl:
                pretty_print_dict(val, lvl, max_lvl)
        else:
            if isinstance(val, list):
                for a in val:
                    print(f"{get_print_prefix(lvl)}\t{a}")
            else:
                print(f"{get_print_prefix(lvl)}\t{val}")


def get_print_prefix(lvl: int) -> str:
    return "\t"*lvl
