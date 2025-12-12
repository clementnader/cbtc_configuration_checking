#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


__all__ = ["verify_switches_along_the_routes"]


def verify_switches_along_the_routes():  # TODO
    route_dict = _get_route_dict()
    ivb_dict = load_sheet(DCSYS.IVB)
    for route_name, route in route_dict.items():
        route_ivb = route["Route IVB"]
        route_switch = route["Route Switch"]

        next_ivb = route_ivb[-1]
        for ivb in route_ivb[:-1][::-1]:
            lim = _common_limit(next_ivb, ivb, ivb_dict)
            if not lim:
                print_warning(f"Route IVB are not in order for {route_name}: "
                              f"{ivb} is not connected to {next_ivb}.")
            next_ivb = ivb


def _common_limit(ivb1: str, ivb2: str, ivb_dict) -> Optional[tuple[str, float]]:
    common_limit = None
    for seg1, x1 in get_dc_sys_zip_values(ivb_dict[ivb1], DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X):
        if any(are_points_matching(seg1, x1, seg2, x2)
               for seg2, x2 in get_dc_sys_zip_values(ivb_dict[ivb2], DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X)):
            if common_limit is not None:
                print_error(f"Multiple limits are matching between {ivb1} and {ivb2}: "
                            f"{common_limit} and {(seg1, x1)}.")
            else:
                common_limit = (seg1, x1)
    return common_limit


def _get_route_dict():
    route_dict = load_sheet(DCSYS.Iti)
    for route_name, route in route_dict.items():
        route_ivb_list = list()
        for ivb in get_dc_sys_value(route, DCSYS.Iti.RouteIvb.Ivb):
            route_ivb_list.append(ivb)
        route_ivb_list.append(get_dc_sys_value(route, DCSYS.Iti.DestinationIvb))
        route_switch_list = list(get_dc_sys_zip_values(route, DCSYS.Iti.Aiguille.Nom, DCSYS.Iti.Aiguille.Position))
        route_dict[route_name]["Route IVB"] = route_ivb_list
        route_dict[route_name]["Route Switch"] = route_switch_list
    return route_dict
