#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *


def get_cols_name_from_ref(sh: xlrd.sheet, cols_ref: list[str]) -> dict[str, str]:
    if not cols_ref:
        return []
    xlrd_cols_ref = [get_xlrd_column(col_ref) for col_ref in cols_ref]
    dict_cols_name = dict()
    for n, j in enumerate(xlrd_cols_ref):
        cell1 = f"{sh.cell_value(0, j)}"
        cell2 = f"{sh.cell_value(1, j)}"
        if not cell2:  # merged cells
            dict_cols_name[cols_ref[n]] = f"{cell1}"
        else:
            cell1 = f"{sh.cell_value(0, j)}"
            ref_j = j
            while not cell1:
                ref_j -= 1
                cell1 = f"{sh.cell_value(0, ref_j)}"
            dict_cols_name[cols_ref[n]] = f"{cell1}::{cell2}"
    return dict_cols_name


def get_lim_cols_name_from_ref(sh: xlrd.sheet, col_ref: str, delta_between_limits: int):
    if not col_ref or not delta_between_limits:
        return []
    xlrd_col_ref = get_xlrd_column(col_ref)
    list_attr = list()
    for j in range(xlrd_col_ref, xlrd_col_ref + delta_between_limits):
        list_attr.append(f"{sh.cell_value(1, j)}")
    return list_attr
