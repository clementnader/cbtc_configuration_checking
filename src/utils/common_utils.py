#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import ascii_uppercase
from .colors_pkg import *


def columns_from_to(first: str, last:str):
    assert len(first) <= 2 and len(last) <= 2
    if len(first) == 1:
        first = " " + first
    if len(last) == 1:
        last = " " + last

    within_range = False
    list_cols = list()
    for i in " " + ascii_uppercase:
        for j in ascii_uppercase:
            current_col = i + j
            if current_col == first:
                within_range = True
            if not within_range:
                continue
            list_cols.append(current_col.lstrip())
            if current_col == last:
                within_range = False
    return list_cols


def sort_dict(in_dict):
    return {key: in_dict[key] for key in sorted(in_dict)}


def compare_dict(dict1: dict, dict2: dict, dict1_name: str, dict2_name: str, lvl: int = 0, s: str = "") -> bool:
    if dict1 == dict2:
        return True
    if dict1.keys() != dict2.keys():
        s += f"{get_print_prefix(lvl)}Dictionaries keys are different: \n"
        s += f"Missing keys in {dict2_name}: {[key for key in dict1 if key not in dict2]}\n"
        s += f"Missing keys in {dict1_name}: {[key for key in dict2 if key not in dict1]}\n"
        for key in (key for key in dict1 if key not in dict2):
            dict1.pop(key)
        for key in (key for key in dict2 if key not in dict1):
            dict2.pop(key)
        compare_dict(dict1, dict2, dict1_name, dict2_name, lvl, s)
        if lvl == 0:
            print(s)
        return False
    lvl += 1
    for key in dict1:
        if dict1[key] == dict2[key]:
            pass
        else:
            if lvl == 1:
                s = ""
            s += f"{get_print_prefix(lvl)}> {Color.pale_green}{key}{Color.reset}\n"
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                compare_dict(dict1[key], dict2[key], dict1_name, dict2_name, lvl, s)
            elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
                dict1[key].sort(key=lambda x: list(x.values()))
                dict2[key].sort(key=lambda x: list(x.values()))
                lvl += 1
                for i, (elem1, elem2) in enumerate(zip(dict1[key], dict2[key])):
                    s += f"{get_print_prefix(lvl)}> {Color.pink}{i}{Color.reset}\n"
                    compare_dict(elem1, elem2, dict1_name, dict2_name, lvl, s)
            else:
                print(s[:-1])
                print(f"{get_print_prefix(lvl-1)}Values are different: \n"
                      f"{get_print_prefix(lvl)}\t· {dict1_name}: {Color.light_yellow}{dict1[key]}{Color.reset}\n"
                      f"{get_print_prefix(lvl)}\t· {dict2_name}: {Color.yellow}{dict2[key]}{Color.reset}\n")
    return False


def get_print_prefix(lvl: int) -> str:
    return '\t'*lvl


def pretty_print_dict(in_dict: dict, lvl: int = 0, max_lvl: int = None) -> None:
    lvl += 1
    for key, val in in_dict.items():
        print(f"{get_print_prefix(lvl)}> {key}")
        if isinstance(val, dict):
            if max_lvl is None or lvl <= max_lvl:
                pretty_print_dict(val, lvl)
        else:
            print(f"{get_print_prefix(lvl)}\t{val}")
