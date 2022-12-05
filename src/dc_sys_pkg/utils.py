#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl.utils as xl_ut  # for column_index_from_string and get_column_letter
import xlrd


def get_xlrd_column(col: str) -> int:
    return xl_ut.column_index_from_string(col) - 1


def get_xlrd_line(line: int) -> int:
    return line - 1


def compare_dict(dict1: dict, dict2: dict, dict1_name: str, dict2_name: str, lvl: int = 0) -> bool:
    if dict1 == dict2:
        return True
    if dict1.keys() != dict2.keys():
        print(f"{get_print_prefix(lvl)}Dictionaries keys are different: ")
        print(f"Missing keys in {dict2_name}: {[key for key in dict1 if key not in dict2]}")
        print(f"Missing keys in {dict1_name}: {[key for key in dict2 if key not in dict1]}")
        for key in [key for key in dict1 if key not in dict2]:
            dict1.pop(key)
        for key in [key for key in dict2 if key not in dict1]:
            dict2.pop(key)
        compare_dict(dict1, dict2, dict1_name, dict2_name, lvl)
        return False
    lvl += 1
    for key in dict1:
        if dict1[key] == dict2[key]:
            pass
        else:
            print(f"{get_print_prefix(lvl)}> {key}")
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                compare_dict(dict1[key], dict2[key], dict1_name, dict2_name, lvl)
            elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
                for elem1, elem2 in zip(dict1[key], dict2[key]):
                    compare_dict(elem1, elem2, dict1_name, dict2_name, lvl)
            else:
                print(f"{get_print_prefix(lvl-1)}Values are different:"
                      f"\n{get_print_prefix(lvl)}\t· {dict1_name}: {dict1[key]}"
                      f"\n{get_print_prefix(lvl)}\t· {dict2_name}: {dict2[key]}")
    return False


def get_print_prefix(lvl: int) -> str:
    return '\t'*lvl
