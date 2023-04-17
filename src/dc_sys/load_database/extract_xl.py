#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .sheet_cols_name import get_cols_name_from_ref, get_lim_cols_name_from_ref

START_LINE = 3


def read_cell(sh: xlrd.sheet, i: int, j: int):
    value = sh.cell_value(i, j)
    if value in ("", None):
        return None
    if isinstance(value, str):
        try:
            value = float(value.replace(",", "."))
        except ValueError:
            pass
    return value


def get_dict_fixed_col(sh: xlrd.sheet, cols_ref: list[str], generic_obj_name: bool) -> dict:
    xlrd_line_ref = get_xlrd_line(START_LINE)
    xlrd_cols_ref = [get_xlrd_column(col_ref) for col_ref in cols_ref]
    xlrd_name_col = get_xlrd_column('A')
    list_cols_name = list(get_cols_name_from_ref(sh, cols_ref).values())

    sh_dict = dict()
    for i in range(xlrd_line_ref, sh.nrows):
        obj_name = read_cell(sh, i, xlrd_name_col)
        if obj_name is not None:
            if generic_obj_name:
                obj_name = f"{sh.name}_line_{i+1}"
            sh_dict[obj_name] = dict()
            for n, j in enumerate(xlrd_cols_ref):
                value = read_cell(sh, i, j)
                if value is not None:
                    sh_dict[obj_name][list_cols_name[n]] = value
    return sh_dict


def get_limits_dict(sh: xlrd.sheet, col_ref: str, nb_max_limits: int, delta_between_limits: int):
    xlrd_line_ref = get_xlrd_line(START_LINE)
    xlrd_col_ref = get_xlrd_column(col_ref)
    list_attr = get_lim_cols_name_from_ref(sh, col_ref, delta_between_limits)

    limits_dict = dict()
    for i in range(xlrd_line_ref, sh.nrows):
        obj_name = read_cell(sh, i, 0)
        limits_dict[obj_name] = {"limits": list()}
        for j in range(xlrd_col_ref, xlrd_col_ref + nb_max_limits * delta_between_limits, delta_between_limits):
            seg = read_cell(sh, i, j)
            if seg is None:
                break
            current_limit = dict()
            for n in range(0, delta_between_limits):
                current_limit[list_attr[n]] = read_cell(sh, i, j + n)
            limits_dict[obj_name]["limits"].append(current_limit)
    return limits_dict


def get_dict(sh: xlrd.sheet, fixed_cols_ref: list[str], generic_obj_name: bool = False,
             lim_first_col: str = None, nb_max_limits: int = 0, delta_between_limits: int = 0) -> dict:

    sh_dict = get_dict_fixed_col(sh, fixed_cols_ref, generic_obj_name)
    if lim_first_col is not None and nb_max_limits and delta_between_limits:
        sh_dict_lim = get_limits_dict(sh,  lim_first_col, nb_max_limits, delta_between_limits)
        for key in sh_dict_lim:
            sh_dict[key].update(sh_dict_lim[key])
    return sh_dict
