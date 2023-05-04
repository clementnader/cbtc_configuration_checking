#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .colored_output import *

__ALL__ = ["print_bar", "print_title", "print_section_title", "print_error", "print_warning", "print_success",
           "print_log", "progress_bar", "print_sub_variables", "print_variables", "print_final_value"]


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


def progress_bar(i: int, max_nb: int, end: bool = False):
    global g_last_color_index
    percent = i / max_nb
    full_cell_char = '█'
    full_len = 20
    nb_char = int(percent*full_len)
    colors = Color.rainbow
    # color = colors[int(percent*(len(colors)-1))]
    color = colors[g_last_color_index] if not end else Color.reset
    g_last_color_index = (g_last_color_index + 1) % len(colors) if not end else 0
    s = '|' + color + full_cell_char*nb_char + ' '*(full_len-nb_char) + Color.reset + '|'
    s += f" {Color.default}{percent:>7.2%}{Color.reset} ({i}/{max_nb})"
    return s


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
