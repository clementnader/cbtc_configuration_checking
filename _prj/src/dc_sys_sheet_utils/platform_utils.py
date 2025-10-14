#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_platform_start_and_end_limits", "get_atb_zone_related_to_plt",
           "is_accelerometer_calibration_authorized_at_platform"]


def get_platform_start_and_end_limits(plt_name: str) -> tuple[tuple[str, float, str], tuple[str, float, str]]:
    plt_limits = get_object_position(DCSYS.Quai, plt_name)
    start_limit = [(seg, x, direction) for (seg, x, direction) in plt_limits if direction == Direction.CROISSANT][0]
    end_limit = [(seg, x, direction) for (seg, x, direction) in plt_limits if direction == Direction.DECROISSANT][0]
    return start_limit, end_limit


def get_atb_zone_related_to_plt(plt_name: str):
    atb_zone_dict = load_sheet(DCSYS.ZCRA)
    related_atb_mvt = list()
    for atb_zone_name, atb_zone in atb_zone_dict.items():
        if get_dc_sys_value(atb_zone, DCSYS.ZCRA.MouvZcra.QuaiOrigine)[0] == plt_name:
            related_atb_mvt.append((atb_zone_name, atb_zone))
    return related_atb_mvt


def is_accelerometer_calibration_authorized_at_platform(plt_name: str) -> Optional[bool]:
    plt_dict = load_sheet(DCSYS.Quai)
    plt_value = plt_dict[plt_name]
    if "AllowAccelerometerCalibration" in get_class_attributes_dict(DCSYS.Quai):
        return get_dc_sys_value(plt_value, DCSYS.Quai.AllowAccelerometerCalibration) == YesOrNo.O

    if "AllowAccelerometersCalibration" in get_class_attributes_dict(DCSYS.Quai):
        return get_dc_sys_value(plt_value, DCSYS.Quai.AllowAccelerometersCalibration) == YesOrNo.O

    return None
