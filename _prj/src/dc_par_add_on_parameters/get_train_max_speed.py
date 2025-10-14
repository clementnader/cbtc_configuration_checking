#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_train_max_speed"]


def get_train_max_speed(variables: dict = None):
    if "MaxSpeed" in get_class_attributes_dict(DCSYS.Train_Types):
        pv_sheet_class = DCSYS.Train_Types
        av_sheet_class = DCSYS.AV_Types
    else:
        pv_sheet_class = DCSYS.Train_Consist
        av_sheet_class = DCSYS.AV_Consist

    pv_dict = load_sheet(pv_sheet_class)
    av_dict = load_sheet(av_sheet_class)
    train_max_speed_dict = dict()
    for train_type, train_value in pv_dict.items():
        max_speed = get_dc_sys_value(train_value, pv_sheet_class.MaxSpeed)
        train_max_speed_dict[train_type] = max_speed
    for train_type, train_value in av_dict.items():
        max_speed = get_dc_sys_value(train_value, av_sheet_class.MaxSpeed)
        train_max_speed_dict[train_type] = max_speed

    max_max_speed = max(train_max_speed_dict.values()) / 3.6  # convert to m/s
    if variables is not None:
        variables.update({"train_max_speed": f"{max_max_speed} m/s"})
    return max_max_speed
