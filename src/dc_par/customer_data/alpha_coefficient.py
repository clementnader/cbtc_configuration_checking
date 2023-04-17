#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def cd_alpha(variables: dict = None):
    train_types_dict = load_sheet("train_types")
    train_types_cols_name = get_cols_name("train_types")

    alpha_dict = dict()
    for train_type, train_value in train_types_dict.items():
        full_load_mass = train_value[train_types_cols_name['G']]
        rotating_mass = train_value[train_types_cols_name['H']]
        alpha = rotating_mass/full_load_mass
        alpha_dict[train_type] = alpha

    max_alpha = max(alpha_dict.values())

    if variables is not None:
        variables.update({"cd_alpha": f"{max_alpha}"})

    return max_alpha
