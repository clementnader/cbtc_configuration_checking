#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.route_utils import *
from ...dc_sys_sheet_utils.block_utils import *
from ...dc_sys_sheet_utils.ivb_utils import *
from ...dc_sys_sheet_utils.zc_utils import *


__all__ = ["get_sum_len_route_physical_blocks", "get_first_zc_overlay_route_physical_blocks"]


def get_sum_len_route_physical_blocks():
    route_dict = load_sheet(DCSYS.Iti)

    min_route_length = None
    corresponding_route = None

    for route_name in route_dict:
        route_block_list = get_route_block_list(route_name)

        route_length = 0
        for block_name in route_block_list:
            block_length = min(get_list_len_block(block_name))
            route_length += block_length

        if min_route_length is None or route_length < min_route_length:
            min_route_length = route_length
            corresponding_route = route_name

    print(min_route_length, corresponding_route)


def get_first_zc_overlay_route_physical_blocks():
    route_dict = load_sheet(DCSYS.Iti)

    min_first_block_length = None
    corresponding_route = None
    corresponding_first_block = None
    corresponding_list_zc = None

    for route_name in route_dict:
        route_ivb_list = get_route_ivb_list(route_name)

        in_zc_overlay = False
        list_zc = None
        for ivb_name in route_ivb_list:
            list_zc = get_zc_of_object(DCSYS.IVB, ivb_name)
            if len(list_zc) == 2:
                in_zc_overlay = True
                break

        if not in_zc_overlay:
            continue

        first_ivb_name = route_ivb_list[0]
        first_block_name = get_related_block_of_ivb(first_ivb_name)
        first_block_length = min(get_list_len_block(first_block_name))

        if min_first_block_length is None or first_block_length < min_first_block_length:
            min_first_block_length = first_block_length
            corresponding_route = route_name
            corresponding_first_block = first_block_name
            corresponding_list_zc = list_zc

    print(min_first_block_length, corresponding_route, corresponding_first_block, corresponding_list_zc)
