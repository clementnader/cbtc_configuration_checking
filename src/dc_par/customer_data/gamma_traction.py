#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def par_gamma_traction_max(variables: dict = None):
    traction_dict = load_sheet("traction")
    traction_cols_name = get_cols_name("traction")

    traction_list = list()
    for traction_value in traction_dict.values():
        traction = traction_value[traction_cols_name['E']]
        traction_list.append(traction)

    max_traction = max(traction_list)
    if variables is not None:
        variables.update({"par_gamma_traction_max": f"{max_traction} m/s^2"})
    return max_traction
