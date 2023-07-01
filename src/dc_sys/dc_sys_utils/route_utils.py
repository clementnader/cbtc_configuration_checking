#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_bop import *
from ...cctool_oo_schema import DCSYS
from ..load_database import *


def get_routes():
    route_dict = load_sheet(DCSYS.Iti)
    for route_name, route_value in route_dict.items():
        route_dict[route_name]["Route IVB"] = _get_route_ivb(route_value)
        route_dict[route_name]["Route Switch"] = _get_route_switch(route_value)
    return route_dict


def _get_route_ivb(route_value: dict[str, str]):
    route_ivb_list = list()
    for ivb, in get_dc_sys_zip_values(route_value, DCSYS.Iti.RouteIvb.Ivb):
        if ivb:
            route_ivb_list.append(ivb.upper())
    route_ivb_list.append(get_dc_sys_value(route_value, DCSYS.Iti.DestinationIvb))
    return route_ivb_list


def _get_route_switch(route_value: dict[str, str]):
    sw_list = list()
    for sw_name, sw_pos in get_dc_sys_zip_values(route_value, DCSYS.Iti.Aiguille.Nom, DCSYS.Iti.Aiguille.Position):
        if sw_name:
            sw_pos = convert_switch_pos_to_ixl(sw_name, sw_pos)
            sw_list.append(sw_name.upper() + sw_pos.upper())
    return sw_list
