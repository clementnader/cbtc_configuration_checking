#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy.random as rd
from .colored_output import *
from ..time_utils import *

__ALL__ = ["print_bar", "print_title", "print_section_title", "print_error", "print_warning", "print_success",
           "print_log", "progress_bar", "print_sub_variables", "print_variables", "print_final_value",
           "test_moving_progress_bar"]


def print_bar(length: int = 100):
    print("-" * length + "\n")


def print_title(title: str):
    main_color = f"{Color.bold}{Color.underline}{Color.turquoise}"
    len_title = len(remove_colors(title))
    whole_len = max(100, len_title + 10)
    title = title.replace(Color.reset, f"{Color.reset}{main_color}")
    empty_len = whole_len - len_title

    print_bar(whole_len)
    print(" " * (empty_len//2) + main_color + title + Color.reset + " " * (empty_len - empty_len//2) + "\n")
    print_bar(whole_len)


def print_section_title(title: str):
    main_color = f"{Color.bold}{Color.underline}{Color.beige}"
    title = title.replace(Color.reset, f"{Color.reset}{main_color}")
    title = title.replace("\n", f"{Color.reset}\n{main_color}")
    print(main_color + title + Color.reset)


def print_error(*args, end="\n"):
    main_color = Color.light_red
    print(f"\n{bg_color(main_color)}{Color.black}Error{Color.reset}{main_color}: ", end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") for arg in args)
    print(*args, end="")
    print(f"{Color.reset}\n", end=end)


def print_warning(*args, end="\n"):
    main_color = Color.orange
    print(f"\n{bg_color(main_color)}{Color.black}Warning{Color.reset}{main_color}: ", end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") for arg in args)
    print(*args, end="")
    print(f"{Color.reset}\n", end=end)


def print_success(*args, end="\n"):
    main_color = Color.vivid_green
    print(f"\n{main_color}", end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") for arg in args)
    print(*args, end="")
    print(f"{Color.reset}\n", end=end)


def print_log(*args, end="\n"):
    main_color = Color.light_grey
    print(main_color, end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") for arg in args)
    print(*args, end="")
    print(Color.reset, end=end)


g_last_color_index = 0
g_start_time = 0
g_coin_flip = rd.random() < .05


def progress_bar(i: int, max_nb: int, end: bool = False, only_bar: bool = False,
                 sliding_rainbow: bool = True, static_rainbow: bool = False):
    global g_last_color_index, g_start_time, g_coin_flip
    colors = Color.rainbow if not g_coin_flip else Color.progress_pride
    full_cell_char = '█'
    full_len = len(colors)
    percent = i / max_nb
    nb_char = int(percent*full_len)

    if sliding_rainbow and not static_rainbow:
        s = '|'
        for num_color_index in range(nb_char):
            color = colors[(g_last_color_index + num_color_index) % full_len] if not end else Color.reset
            s += color + full_cell_char
        s += Color.reset + ' '*(full_len-nb_char) + '|'
        g_last_color_index = (g_last_color_index - 1) % full_len if not end else 0
    else:
        if static_rainbow:
            color = colors[int(percent*(full_len-1))]
        else:
            color = colors[g_last_color_index] if not end else Color.reset
        g_last_color_index = (g_last_color_index + 1) % full_len if not end else 0
        s = '|' + color + full_cell_char*nb_char + ' '*(full_len-nb_char) + Color.reset + '|'
    if not only_bar:
        s += f" {Color.default}{percent:>7.2%}{Color.reset} " + " "*(len(str(max_nb))-len(str(i))) + f"({i}/{max_nb})"

    # Timer
    current_time = time.perf_counter()
    elapsed_time = format_timespan(current_time - g_start_time)
    if end:
        s += f" (total elapsed time: {elapsed_time})"
        g_start_time = time.perf_counter()
        g_coin_flip = rd.random() < .05
    else:
        s += f" (elapsed time: {elapsed_time})"
    return s


def test_moving_progress_bar():
    progress_bar(1, 1, end=True)  # init progress bar
    len_colors = len(Color.rainbow) if not g_coin_flip else len(Color.progress_pride)
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
            if nb_ite > 20 and nb_ite % len_colors == 1:  # around 1.6 s and wait until a whole loop haas passed
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
