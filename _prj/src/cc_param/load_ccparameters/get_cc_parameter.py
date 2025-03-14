#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cc_param_utils import *
from .read_cc_param import *


__all__ = ["get_cc_param_values"]


def get_cc_param_values(param_name: str):
    """ Return a list of all the different values of this CCParameter. """
    list_param_values = list()
    dict_cc_params = get_cc_params()  # dictionary listing for each CCParameter.csv file (for each Cab for each TU)
    # a dictionary listing all CCParameters and the corresponding column info from the csv file.
    for cc_param_dict in dict_cc_params.values():
        cc_param_column_info = cc_param_dict[param_name.lower()]  # we access the info related to the param_name
        value = int(cc_param_column_info[VALUE_TITLE])  # values in CCParameter are all integers.
        conversion = cc_param_column_info[CONVERSION_TITLE]  # conversion is a string (e.g. "x / 100.0")
        if conversion.upper().strip() == "NA":  # no conversion
            converted_value = value
        else:
            converted_value = eval(conversion.lower().strip(), {}, {"x": value})
            # We apply the conversion using the "eval" function:
            # the first argument is the formula string we want to evaluate,
            # the second argument is a globals dictionary, here it is empty,
            # and the third argument is a locals mapping, here we assigned to "x" the value
            # so that it evaluates the formula considering that "x" is the value.
            # For example, conversion is "x / 100.0", value is 60, the eval will return the result of 60 / 100.0 = 0.6.
        list_param_values.append(converted_value)
    return list_param_values
