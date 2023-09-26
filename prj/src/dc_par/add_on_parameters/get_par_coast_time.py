#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ...dc_sys import *


def par_coast_time(variables: dict = None):
    if "CoastTime" in get_sheet_attributes_columns_dict(DCSYS.Train_Types):
        sheet_class = DCSYS.Train_Types
    else:
        sheet_class = DCSYS.Train_Consist

    train_dict = load_sheet(sheet_class)
    coast_time_dict = dict()
    for train_type, train_value in train_dict.items():
        coast_time = get_dc_sys_value(train_value, sheet_class.CoastTime)
        coast_time_dict[train_type] = coast_time

    max_coast_time = max(coast_time_dict.values())
    if variables is not None:
        variables.update({"par_coast_time": f"{max_coast_time} s"})
    return max_coast_time
