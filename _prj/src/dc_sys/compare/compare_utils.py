#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["compare_sheet", "compare_all_sheets"]


def compare_sheet(object_name):
    object_name = get_sheet_name(object_name)
    print_section_title(object_name)
    dict_old = load_sheet(object_name, old=True)
    dict_new = load_sheet(object_name, old=False)
    return compare_dict(dict_old, dict_new, "old", "new")


def compare_all_sheets(start: str = None):
    started = False
    for key in get_all_sheet_names():
        if start is not None and started is False:
            if key == start:
                started = True
            else:
                continue
        compare_sheet(key)
        print(f"{Color.white}Press any key to continue to next sheet...{Color.reset}", flush=True)
        input()
        print()


def compare_dict(dict1: dict, dict2: dict, dict1_name: str, dict2_name: str, lvl: int = 0, s: list = None) -> bool:
    if s is None:
        s = list()
    if dict1 == dict2:
        return True
    if dict1.keys() != dict2.keys():
        print(f"Dictionaries keys are different:\n"
              f"Missing keys in {dict2_name}: {[key for key in dict1 if key not in dict2]}\n"
              f"Missing keys in {dict1_name}: {[key for key in dict2 if key not in dict1]}\n")
        for key in [key for key in dict1.keys() if key not in dict2]:
            dict1.pop(key)
        for key in [key for key in dict2.keys() if key not in dict1]:
            dict2.pop(key)
    lvl += 1
    for key in dict1:
        if dict1[key] != dict2[key]:
            if len(s) == lvl - 1:
                s.append(None)
            s[lvl - 1] = f"{get_print_prefix(lvl)}> {Color.pale_green}{key}{Color.reset}"
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                if lvl == 1:
                    compare_dict(dict1[key], dict2[key], dict1_name, dict2_name, lvl, s)
                else:
                    compare_sub_dict(key, dict1[key], dict2[key], dict1_name, dict2_name, lvl, s)
            else:
                print("\n".join(s))
                print(f"{get_print_prefix(lvl - 1)}Values are different:\n"
                      f"{get_print_prefix(lvl)}\t· {dict1_name}: {Color.light_yellow}{dict1[key]}{Color.reset}\n"
                      f"{get_print_prefix(lvl)}\t· {dict2_name}: {Color.yellow}{dict2[key]}{Color.reset}\n")
    return False


def compare_sub_dict(key: str, dict1: dict, dict2: dict, dict1_name: str, dict2_name: str, lvl: int, s: list):
    s = s[:]
    lvl += 1
    merge_cols = False if key == get_dc_sys_attribute_name(DCSYS.Seg.SegmentsVoisins) else True
    if merge_cols:
        sub_key = tuple(x for x in dict1.keys())
        if len(s) == lvl - 1:
            s.append(None)
        s[lvl - 1] = f"{get_print_prefix(lvl)}> {Color.pale_green}{sub_key}{Color.reset}"
        list_of_object_1 = list(zip(*dict1.values()))
        list_of_object_2 = list(zip(*dict2.values()))
        list_of_object_1 = sorted([x for x in list_of_object_1 if x[0] is not None], key=lambda x: _sort_function(x, sub_key))
        list_of_object_2 = sorted([x for x in list_of_object_2 if x[0] is not None], key=lambda x: _sort_function(x, sub_key))
        for i, (elem1, elem2) in enumerate(zip(list_of_object_1, list_of_object_2)):
            if elem1 != elem2:
                print("\n".join(x for x in s if x is not None))
                print(f"{get_print_prefix(lvl + 1)}> {Color.pink}{i}{Color.reset}")
                print(f"{get_print_prefix(lvl)}Values are different:\n"
                      f"{get_print_prefix(lvl + 1)}\t· {dict1_name}: {Color.light_yellow}{elem1}{Color.reset}\n"
                      f"{get_print_prefix(lvl + 1)}\t· {dict2_name}: {Color.yellow}{elem2}{Color.reset}\n")
    else:
        for sub_key in dict1.keys():
            if len(s) == lvl - 1:
                s.append(None)
            s[lvl - 1] = f"{get_print_prefix(lvl)}> {Color.pale_green}{sub_key}{Color.reset}"
            list_of_object_1 = (sorted([x for x in dict1[sub_key] if x is not None])
                             + [x for x in dict1[sub_key] if x is None])
            list_of_object_2 = (sorted([x for x in dict2[sub_key] if x is not None])
                             + [x for x in dict2[sub_key] if x is None])
            for i, (elem1, elem2) in enumerate(zip(list_of_object_1, list_of_object_2)):
                if elem1 != elem2:
                    print("\n".join(x for x in s if x is not None))
                    print(f"{get_print_prefix(lvl + 1)}> {Color.pink}{i}{Color.reset}")
                    print(f"{get_print_prefix(lvl)}Values are different:\n"
                          f"{get_print_prefix(lvl + 1)}\t· {dict1_name}: {Color.light_yellow}{elem1}{Color.reset}\n"
                          f"{get_print_prefix(lvl + 1)}\t· {dict2_name}: {Color.yellow}{elem2}{Color.reset}\n")


def _sort_function(x, sub_key):
    if "Voie" in sub_key and "Pk" in sub_key:
        return x[sub_key.index("Voie")], x[sub_key.index("Pk")]
    elif "Track" in sub_key and "Kp" in sub_key:
        return x[sub_key.index("Track")], x[sub_key.index("Kp")]
    else:
        return x
