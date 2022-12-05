#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_sys_pkg import *


def compare_sheets(sh_name: str, line_ref: int, cols_ref: list[str], name_col: str = 'A'):
    wb_new = load_wb()
    sh_new = wb_new.sheet_by_name(sh_name)
    wb_old = load_wb(old=True)
    sh_old = wb_old.sheet_by_name(sh_name)
    dict_new = get_dict(sh_new, fixed_cols_ref=cols_ref, name_col=name_col, line_ref=line_ref)
    dict_old = get_dict(sh_old, fixed_cols_ref=cols_ref, name_col=name_col, line_ref=line_ref)
    return compare_dict(dict_new, dict_old, "new", "old")


def compare_limits_sheets(sh_name: str, line_ref: int, col_ref: str, nb_max_limits: int, delta_between_limits: int):
    wb_new = load_wb()
    wb_old = load_wb(old=True)
    sh_new = wb_new.sheet_by_name(sh_name)
    sh_old = wb_old.sheet_by_name(sh_name)
    zc_area_dict_new = get_limits_dict(sh_new, line_ref, col_ref, nb_max_limits, delta_between_limits)
    zc_area_dict_old = get_limits_dict(sh_old, line_ref, col_ref, nb_max_limits, delta_between_limits)
    return compare_dict(zc_area_dict_new, zc_area_dict_old, "new", "old")
