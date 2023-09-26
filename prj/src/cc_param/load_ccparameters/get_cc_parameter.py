#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .read_cc_param import get_cc_params


def get_cc_param_values(param_name: str):
    list_param_values = list()
    dict_cc_params = get_cc_params()
    for cc_param_dict in dict_cc_params.values():
        value = int(cc_param_dict[param_name.lower()]["VALUE"])
        conversion = cc_param_dict[param_name.lower()]["CONVERSION"]
        if conversion.upper().strip() == "NA":
            converted_value = value
        else:
            converted_value = eval(conversion, {}, {"x": value})
        list_param_values.append(converted_value)
    return list_param_values
