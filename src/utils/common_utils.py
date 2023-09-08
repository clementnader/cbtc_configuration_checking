#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, Union
from string import ascii_uppercase


__all__ = ["Optional", "Union", "ascii_uppercase", "columns_from_to", "sort_dict", "pretty_print_dict"]


def columns_from_to(first: str, last: str):
    assert len(first) <= 2 and len(last) <= 2
    if len(first) == 1:
        first = " " + first
    if len(last) == 1:
        last = " " + last

    if first > last:
        return []

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
                pretty_print_dict(val, lvl)
        else:
            print(f"{get_print_prefix(lvl)}\t{val}")


def get_print_prefix(lvl: int) -> str:
    return '\t'*lvl
