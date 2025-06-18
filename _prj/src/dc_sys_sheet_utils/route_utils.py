#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_bop import *
from .ivb_utils import get_related_block_of_ivb


__all__ = ["get_routes", "get_route_ivb_list", "get_route_block_list", "get_route_switch_list"]


def get_routes():
    route_dict = load_sheet(DCSYS.Iti)
    for route_name in route_dict:
        route_dict[route_name]["Route IVB"] = get_route_ivb_list(route_name)
        route_dict[route_name]["Route Switch"] = get_route_switch_list(route_name)
    return route_dict


def get_route_ivb_list(route_name: str) -> list[str]:
    route_dict = load_sheet(DCSYS.Iti)
    route_value = route_dict[route_name]
    route_ivb_list = list()
    for ivb in get_dc_sys_value(route_value, DCSYS.Iti.RouteIvb.Ivb):
        if ivb:
            route_ivb_list.append(ivb.upper())
    # Add the destination IVB
    route_ivb_list.append(get_dc_sys_value(route_value, DCSYS.Iti.DestinationIvb))

    return route_ivb_list


def get_route_block_list(route_name: str) -> list[str]:
    route_ivb_list = get_route_ivb_list(route_name)

    route_block_list = list()
    for ivb_name in route_ivb_list:
        block_name = get_related_block_of_ivb(ivb_name)
        # We can have multiple IVBs on the same block, so we check if we don't have already added this block
        if block_name not in route_block_list:
            route_block_list.append(block_name)

    return route_block_list


def get_route_switch_list(route_name: str) -> list[str]:
    route_dict = load_sheet(DCSYS.Iti)
    route_value = route_dict[route_name]
    sw_list = list()
    for sw_name, sw_pos in get_dc_sys_zip_values(route_value, DCSYS.Iti.Aiguille.Nom, DCSYS.Iti.Aiguille.Position):
        if sw_name:
            sw_pos = convert_switch_pos_to_ixl(sw_name, sw_pos)
            sw_list.append(sw_name.upper() + sw_pos.upper())
    return sw_list
