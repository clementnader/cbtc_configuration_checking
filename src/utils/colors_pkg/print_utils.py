#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .colored_output import *


def print_log(*args):
    main_color = Color.light_grey
    print(main_color, end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") for arg in args)
    print(*args, end="")
    print(Color.reset)


def print_warning(*args):
    main_color = Color.orange
    print(f"{bg_color(main_color)}{Color.black}Warning{Color.reset}{main_color}: ", end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") for arg in args)
    print(*args, end="")
    print(f"{Color.reset}\n")


def print_success(*args):
    main_color = Color.light_green
    print(f"{main_color}", end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") for arg in args)
    print(*args, end="")
    print(f"{Color.reset}\n")


def print_error(*args):
    main_color = Color.light_red
    print(f"{bg_color(main_color)}{Color.black}Error{Color.reset}{main_color}: ", end="")
    args = (arg.replace(Color.reset, f"{Color.reset}{main_color}") for arg in args)
    print(*args, end="")
    print(f"{Color.reset}\n")


def print_sub_variables(all_sub_variables: dict[str, str]):
    for var_name, var_value in modify_variables_to_print(all_sub_variables).items():
        print(f"\t\t\t{var_name} = {Color.white}{var_value}{Color.reset}")


def print_variables(variables: dict[str, str]):
    for var_name, var_value in modify_variables_to_print(variables).items():
        print(f"\t\t{Color.pink}{var_name}{Color.reset} = {Color.pale_pink}{var_value}{Color.reset}")


def print_final_value(final_value: dict[str, str]):
    for var_name, var_value in modify_variables_to_print(final_value).items():
        print(f" --> {Color.yellow}{var_name}{Color.reset} = {Color.light_yellow}{var_value}{Color.reset}\n")


def modify_variables_to_print(variables: dict[str, str]):
    dict_to_print = dict()
    for var_name in sorted(variables):
        if not isinstance(variables[var_name], str):
            print(var_name)
        dict_to_print[var_name] = variables[var_name].replace("^2", "²").replace("^3", "³")
    return dict_to_print
