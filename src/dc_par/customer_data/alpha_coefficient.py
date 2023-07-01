#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import DCSYS
from ...dc_sys import *


def cd_alpha(variables: dict = None):
    train_types_dict = load_sheet(DCSYS.Train_Types)

    alpha_dict = dict()
    for train_type, train_value in train_types_dict.items():
        full_load_mass = get_dc_sys_value(train_value, DCSYS.Train_Types.FullLoadMass)
        rotating_mass = get_dc_sys_value(train_value, DCSYS.Train_Types.RotatingMass)
        alpha = rotating_mass / full_load_mass
        alpha_dict[train_type] = alpha

    max_alpha = max(alpha_dict.values())

    if variables is not None:
        variables.update({"cd_alpha": f"{max_alpha}"})

    return max_alpha
