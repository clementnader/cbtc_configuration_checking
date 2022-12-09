#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...xl_pkg import *
from .sheet_cols_name import get_cols_name_from_ref, get_lim_cols_name_from_ref


def get_dict_fixed_col(sh: xlrd.sheet, line_ref: int, cols_ref: list[str], generic_obj_name: bool) -> dict:
    xlrd_line_ref = get_xlrd_line(line_ref)
    xlrd_cols_ref = [get_xlrd_column(col_ref) for col_ref in cols_ref]
    xlrd_name_col = get_xlrd_column('A')
    list_cols_name = list(get_cols_name_from_ref(sh, cols_ref).values())

    sh_dict = dict()
    for i in range(xlrd_line_ref, sh.nrows):
        if sh.cell_value(i, xlrd_name_col) != "":
            if not generic_obj_name:
                obj_name = f"{sh.cell_value(i, xlrd_name_col)}"
            else:
                obj_name = f"{sh.name}_{i-xlrd_line_ref+1}"
            sh_dict[obj_name] = dict()
            for k, j in enumerate(xlrd_cols_ref):
                value = f"{sh.cell_value(i, j)}"
                if value:
                    sh_dict[obj_name][list_cols_name[k]] = f"{sh.cell_value(i, j)}"
    return sh_dict


def get_limits_dict(sh: xlrd.sheet, line_ref: int, col_ref: str, nb_max_limits: int,
                    delta_between_limits: int):
    xlrd_line_ref = get_xlrd_line(line_ref)
    xlrd_col_ref = get_xlrd_column(col_ref)
    list_attr = get_lim_cols_name_from_ref(sh, col_ref, delta_between_limits)

    limits_dict = dict()
    for i in range(xlrd_line_ref, sh.nrows):
        obj_name = f"{sh.cell_value(i, 0)}"
        limits_dict[obj_name] = {"limits": list()}
        for j in range(xlrd_col_ref, xlrd_col_ref + nb_max_limits * delta_between_limits, delta_between_limits):
            seg = f"{sh.cell_value(i, j)}"
            if not seg:
                break
            current_limit = dict()
            for k in range(0, delta_between_limits):
                current_limit[list_attr[k]] = f"{sh.cell_value(i, j + k)}"
            limits_dict[obj_name]["limits"].append(current_limit)
    return limits_dict


def get_dict(sh: xlrd.sheet, fixed_cols_ref: list[str], generic_obj_name: bool = False, line_ref: int = 3,
             lim_first_col: str = None, nb_max_limits: int = 0, delta_between_limits: int = 0) -> dict:

    sh_dict = get_dict_fixed_col(sh, line_ref=line_ref, cols_ref=fixed_cols_ref, generic_obj_name=generic_obj_name)
    if lim_first_col and nb_max_limits and delta_between_limits:
        sh_dict_lim = get_limits_dict(sh, line_ref=line_ref, col_ref=lim_first_col, nb_max_limits=nb_max_limits,
                                      delta_between_limits=delta_between_limits)
        for key in sh_dict_lim:
            sh_dict[key].update(sh_dict_lim[key])
    return sh_dict
