#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cc_param import *


__all__ = ["par_traction_cut_time"]


def par_traction_cut_time(variables: dict = None):
    cc_parameter_name = "PAR_traction_cut_time_after_eb_request"
    list_values = get_cc_parameter_values(cc_parameter_name)
    max_value = max(list_values)
    if variables is not None:
        variables.update({"par_traction_cut_time": f"{max_value} s"})
    return max_value
