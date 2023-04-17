#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def par_coast_time(variables: dict = None):
    test = True
    if test:
        train_types_dict = load_sheet("train_types")
        train_types_cols_name = get_cols_name("train_types")

        coast_time_dict = dict()
        for train_type, train_value in train_types_dict.items():
            coast_time = train_value[train_types_cols_name['L']]
            coast_time_dict[train_type] = coast_time
    else:
        train_consist_dict = load_sheet("train_consist")
        train_consist_cols_name = get_cols_name("train_consist")

        coast_time_dict = dict()
        for train_consist, train_value in train_consist_dict.items():
            coast_time = train_value[train_consist_cols_name['M']]
            coast_time_dict[train_consist] = coast_time

    max_coast_time = max(coast_time_dict.values())  # TODO: confirm we should take the max
    if variables is not None:
        variables.update({"par_coast_time": f"{max_coast_time} s"})
    return max_coast_time
