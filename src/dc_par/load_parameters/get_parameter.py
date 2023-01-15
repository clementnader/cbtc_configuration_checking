#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .load_params import load_params
from ...colors_pkg import *


def get_param_value(param_name: str):
    value, _, _, _ = get_param_info(param_name)
    return value


def get_param_with_unit(param_name: str):
    value, unit, _, _ = get_param_info(param_name)
    return value, unit


def get_param_info(param_name: str):
    params_dict = load_params()
    param = params_dict[param_name.lower()]
    value = param["value"]
    unit = param["unit"]
    s_ns = param["s_ns"]
    fr_name = param["fr_name"]
    is_safety_related = (s_ns.upper() == 'S')

    if not is_safety_related:
        print_warning(f"The parameter {param_name} is not safety-related.")

    return value, unit, is_safety_related, fr_name
