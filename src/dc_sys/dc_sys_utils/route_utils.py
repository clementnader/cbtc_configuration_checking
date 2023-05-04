#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils.common_utils import columns_from_to
from ...dc_bop import *
from ..load_database.load_sheets import load_sheet, get_cols_name


def get_routes():
    route_dict = load_sheet("route")
    route_cols_name = get_cols_name("route")

    for route_name, route_value in route_dict.items():
        route_dict[route_name]["Route IVB"] = _get_route_ivb(route_value, route_cols_name)
        route_dict[route_name]["Route Switch"] = _get_route_switch(route_value, route_cols_name)

    return route_dict


def _get_route_ivb(route_value: dict[str, str], route_cols_name: dict[str, str]):
    route_ivb_list = list()
    for col in columns_from_to('D', 'W'):
        ivb = route_value.get(route_cols_name[col])
        if ivb:
            route_ivb_list.append(ivb.upper())
    route_ivb_list.append(route_value[route_cols_name['X']].upper())  # destination ivb
    return route_ivb_list


def _get_route_switch(route_value: dict[str, str], route_cols_name: dict[str, str]):
    sw_list = list()
    sw_cols = columns_from_to('Z', 'BC')
    sw_name_cols = sw_cols[::2]
    sw_pos_cols = sw_cols[1::2]
    for sw_name_col, sw_pos_col in zip(sw_name_cols, sw_pos_cols):
        sw_name = route_value.get(route_cols_name[sw_name_col])
        sw_pos = route_value.get(route_cols_name[sw_pos_col])
        if sw_name:
            sw_pos = convert_switch_pos_to_ixl(sw_name, sw_pos)
            sw_list.append(sw_name.upper() + sw_pos.upper())
    return sw_list
