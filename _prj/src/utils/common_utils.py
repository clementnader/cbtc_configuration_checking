#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Optional, Union, Generator, Callable, Any
from string import ascii_uppercase


__all__ = ["DESKTOP_DIRECTORY",
           "SRC_DIRECTORY", "PRJ_DIRECTORY", "ROOT_DIRECTORY", "TEMPLATE_DIRECTORY", "LAUNCH_FUNCTION_DIRECTORY",
           "Optional", "Union", "Generator", "Callable", "Any",
           "ascii_uppercase", "columns_from_to", "sort_dict",
           "get_file_directory_path", "get_full_path", "get_class_attr_dict",
           "remove_common_min_max_kp"]


DESKTOP_DIRECTORY = os.path.join(os.getenv("UserProfile"), "Desktop")

SRC_DIRECTORY = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
PRJ_DIRECTORY = os.path.realpath(os.path.join(SRC_DIRECTORY, ".."))
ROOT_DIRECTORY = os.path.realpath(os.path.join(PRJ_DIRECTORY, ".."))

TEMPLATE_DIRECTORY = os.path.join(SRC_DIRECTORY, "templates")
LAUNCH_FUNCTION_DIRECTORY = os.path.join(ROOT_DIRECTORY, "launch_function")


def get_full_path(file: str, relative_path: str) -> str:
    file_directory_path = get_file_directory_path(file)
    return os.path.join(file_directory_path, relative_path)


def get_file_directory_path(file: str) -> str:
    return os.path.dirname(os.path.realpath(file))


def get_class_attr_dict(cl) -> dict[str, Any]:
    if isinstance(cl, type):
        return {key: val for key, val in cl.__dict__.items()
                if not (key.startswith("__") and key.endswith("__"))}
    else:
        return {key: val for key, val in cl.__class__.__dict__.items()
                if not (key.startswith("__") and key.endswith("__"))}


def columns_from_to(first: str, last: str) -> list[str]:
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


def sort_dict(in_dict: dict) -> dict:
    return {key: in_dict[key] for key in sorted(in_dict)}


def remove_common_min_max_kp(list_min_max_kp: list[tuple[float, float]]) -> list[tuple[float, float]]:
    list_min_max_kp = sorted(list_min_max_kp)
    old_mini = list_min_max_kp[0][0]
    old_maxi = list_min_max_kp[0][0]
    final_list_min_max_kp = list()
    for mini, maxi in list_min_max_kp:
        if old_maxi == mini:  # KP are continuing, the old mini is kept and the new maxi becomes the old maxi.
            old_maxi = maxi
        elif old_mini == maxi:  # KP are continuing in decreasing order.
            # It happens for tracks where KP decreases when segment increases.
            # The old maxi is kept and the new mini becomes the old mini.
            old_mini = mini
        else:
            final_list_min_max_kp.append((old_mini, old_maxi))
            old_mini = mini
            old_maxi = maxi
    final_list_min_max_kp.append((old_mini, old_maxi))
    return final_list_min_max_kp
