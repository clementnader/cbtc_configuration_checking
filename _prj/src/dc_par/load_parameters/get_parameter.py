#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .load_params import *


__all__ = ["get_parameter_value", "get_parameter_value_with_unit", "get_parameter_info"]


def get_parameter_value(parameter_name: str, variables: dict = None):
    value, unit = get_parameter_value_with_unit(parameter_name)
    if variables is not None:
        variables.update({parameter_name: f"{value} {unit}"})
    return value


def get_parameter_value_with_unit(parameter_name: str, keep_km_per_h: bool = False):
    value, unit, _, _ = get_parameter_info(parameter_name)
    if not keep_km_per_h and unit == "km/h":
        value /= 3.6  # convert the value to m/s
        unit = "m/s"
    elif unit == "m/s2":
        unit = "m/s^2"
    elif unit == "m/s3":
        unit = "m/s^3"
    return value, unit


def get_parameter_info(parameter_name: str) -> tuple[Optional[Union[float, bool, str]], Optional[str],
                                                 Optional[bool], Optional[str]]:
    params_dict = load_params()
    param = params_dict.get(parameter_name.lower())
    if param is None:
        print_error(f"Parameter {parameter_name} does not exist in DC_PAR.")
        return None, None, None, None
    if parameter_name.lower() == "tsr_interfaced_with_vhmi":
        param["unit"] = "Booleen"  # Correct unit for this parameter from "sans" to "Booléen"
    value = _convert_bool(param["value"], param["unit"])
    unit = param["unit"]
    s_ns = param["s_ns"]
    fr_name = param["fr_name"]
    is_safety_related = (s_ns.upper() == "S")

    if not is_safety_related:
        print_log(f"\tThe parameter {parameter_name} is not safety-related.")

    return value, unit, is_safety_related, fr_name


def _convert_bool(value: Union[int, float, str], unit: str) -> Union[int, float, str, bool]:
    if unit.upper() == "BOOLEEN":
        if value == 0 or (isinstance(value, str) and value.upper() in ["FALSE", "FAUX"]):
            return False
        elif value == 1 or (isinstance(value, str) and value.upper() in ["TRUE", "VRAI"]):
            return True
    return value
