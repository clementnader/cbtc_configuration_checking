#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .load_params import *


__all__ = ["get_param_value", "get_param_with_unit", "get_param_info"]


def get_param_value(param_name: str, variables: dict = None):
    value, unit = get_param_with_unit(param_name)
    if variables is not None:
        variables.update({param_name: f"{value} {unit}"})
    return value


def get_param_with_unit(param_name: str, keep_km_per_h: bool = False):
    value, unit, _, _ = get_param_info(param_name)
    if not keep_km_per_h and unit == "km/h":
        value /= 3.6  # convert the value to m/s
        unit = "m/s"
    elif unit == "m/s2":
        unit = "m/s^2"
    elif unit == "m/s3":
        unit = "m/s^3"
    return value, unit


def get_param_info(param_name: str):
    params_dict = load_params()
    param = params_dict[param_name.lower()]
    value = _convert_bool(param["value"], param["unit"])
    unit = param["unit"]
    s_ns = param["s_ns"]
    fr_name = param["fr_name"]
    is_safety_related = (s_ns.upper() == 'S')

    if not is_safety_related:
        print_log(f"\tThe parameter {param_name} is not safety-related.")

    return value, unit, is_safety_related, fr_name


def _convert_bool(value: Union[int, float, str], unit: str) -> Union[int, float, str, bool]:
    if unit.upper() == "BOOLEEN":
        if value == 0 or (isinstance(value, str) and value.upper() in ["FALSE", "FAUX"]):
            return False
        elif value == 1 or (isinstance(value, str) and value.upper() in ["TRUE", "VRAI"]):
            return True
    return value
