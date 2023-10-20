#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .ivb_utils import get_next_ivb_limits_from_point


__all__ = ["get_related_overlaps", "get_routes_starting_from_signal", "get_ivb_limit_of_a_signal"]


def get_related_overlaps(sig_name: str):
    ovl_dict = load_sheet(DCSYS.IXL_Overlap)
    related_ovl = list()
    for ovl_name, ovl in ovl_dict.items():
        if get_dc_sys_value(ovl, DCSYS.IXL_Overlap.DestinationSignal) == sig_name:
            related_ovl.append((ovl_name, ovl))
    return related_ovl


def get_routes_starting_from_signal(sig_name: str):
    route_dict = load_sheet(DCSYS.Iti)
    related_routes = list()
    for route_name, route in route_dict.items():
        if get_dc_sys_value(route, DCSYS.Iti.SignalOrig) == sig_name:
            related_routes.append((route_name, route))
    return related_routes


def get_ivb_limit_of_a_signal(sig_name: str, sig) -> tuple[tuple[str, float], str]:
    sig_seg, sig_x = get_dc_sys_values(sig, DCSYS.Sig.Seg, DCSYS.Sig.X)
    sig_direction = get_dc_sys_value(sig, DCSYS.Sig.Sens)
    next_ivb_limits = get_next_ivb_limits_from_point(sig_seg, sig_x, downstream=sig_direction == Direction.CROISSANT)
    if len(next_ivb_limits) != 1:
        print_error(f"There is not a direct IVB limit after the signal {sig_name}")
        print(f"{next_ivb_limits = }")
    return next_ivb_limits[0]


def get_approach_zone_entrances(sig_name: str):
    sig_zone_dict = load_sheet(DCSYS.Sig_Zone)
    if sig_name not in sig_zone_dict:
        return []
    return list(get_dc_sys_zip_values(sig_zone_dict[sig_name], DCSYS.Sig_Zone.PointsDEntreeZoneDApproche.Seg,
                                      DCSYS.Sig_Zone.PointsDEntreeZoneDApproche.X))
