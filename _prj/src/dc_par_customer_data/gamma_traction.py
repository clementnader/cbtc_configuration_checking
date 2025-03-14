#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["par_gamma_traction_max"]


def par_gamma_traction_max(variables: dict = None):
    traction_dict = load_sheet(DCSYS.Traction_Profiles)

    traction_list = list()
    for traction_value in traction_dict.values():
        traction = get_dc_sys_value(traction_value, DCSYS.Traction_Profiles.Vital)
        traction_list.append(traction)

    max_traction = max(traction_list)
    if variables is not None:
        variables.update({"par_gamma_traction_max": f"{max_traction} m/s^2"})
    return max_traction
