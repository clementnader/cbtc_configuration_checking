#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils.common_utils import columns_from_to
from ...dc_bop import *
from ..load_database.load_sheets import load_sheet, get_cols_name


def get_overlap():
    overlap_dict = load_sheet("overlap")
    overlap_cols_name = get_cols_name("overlap")

    for ovl_name, ovl_value in overlap_dict.items():
        overlap_dict[ovl_name]["Overlap Path Switch"] = _get_overlap_switch(ovl_value, overlap_cols_name)

    return overlap_dict


def _get_overlap_switch(ovl_value: dict[str, str], overlap_cols_name: dict[str, str]):
    sw_list = list()
    sw_cols = columns_from_to('O', 'V')
    sw_name_cols = sw_cols[::2]
    sw_pos_cols = sw_cols[1::2]
    for sw_name_col, sw_pos_col in zip(sw_name_cols, sw_pos_cols):
        sw_name = ovl_value.get(overlap_cols_name[sw_name_col])
        sw_pos = ovl_value.get(overlap_cols_name[sw_pos_col])
        if sw_name:
            sw_pos = convert_switch_pos_to_ixl(sw_name, sw_pos)
            sw_list.append(sw_name.upper() + sw_pos.upper())
    return sw_list
