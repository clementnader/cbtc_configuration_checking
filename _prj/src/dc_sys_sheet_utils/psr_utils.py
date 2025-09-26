#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point, get_zones_intersecting_zone
from ..dc_sys_draw_path.dc_sys_get_zones import get_zones_intersecting_zone_limits


__all__ = ["get_max_psr_speed_at_point", "get_max_psr_speed_on_zone", "get_max_psr_speed_on_zone_limits",
           "get_min_psr_speed_at_point", "get_min_psr_speed_on_zone", "get_min_psr_speed_on_zone_limits"]


def get_max_psr_speed_at_point(seg: str, x: float, direction: str = None) -> Optional[float]:
    list_psr = get_zones_on_point(DCSYS.ZLPV, seg, x, direction)
    if not list_psr:
        return None
    max_speed = max([get_dc_sys_value(psr_name, DCSYS.ZLPV.VitesseZlpv) for psr_name in list_psr])
    return max_speed / 3.6  # convert to m/s


def get_max_psr_speed_on_zone(obj_type, obj_name: str) -> Optional[float]:
    # TODO check if there is a part of the zone not covered by any ZLPV -> because in that case it should be max speed
    #  even though there is a ZLPV intersecting the zone
    list_psr = get_zones_intersecting_zone(DCSYS.ZLPV, obj_type, obj_name)
    if not list_psr:
        return None
    max_speed = max([get_dc_sys_value(psr_name, DCSYS.ZLPV.VitesseZlpv) for psr_name in list_psr])
    return max_speed / 3.6  # convert to m/s


def get_max_psr_speed_on_zone_limits(zone_limits) -> Optional[float]:
    # TODO check if there is a part of the zone not covered by any ZLPV -> because in that case it should be max speed
    #  even though there is a ZLPV intersecting the zone
    list_psr = get_zones_intersecting_zone_limits(DCSYS.ZLPV, zone_limits)
    if not list_psr:
        return None
    max_speed = max([get_dc_sys_value(psr_name, DCSYS.ZLPV.VitesseZlpv) for psr_name in list_psr])
    return max_speed / 3.6  # convert to m/s


def get_min_psr_speed_at_point(seg: str, x: float, direction: str = None) -> Optional[float]:
    list_psr = get_zones_on_point(DCSYS.ZLPV, seg, x, direction)
    if not list_psr:
        return None
    min_speed = min([get_dc_sys_value(psr_name, DCSYS.ZLPV.VitesseZlpv) for psr_name in list_psr])
    return min_speed / 3.6  # convert to m/s


def get_min_psr_speed_on_zone(obj_type, obj_name: str) -> Optional[float]:
    # TODO check if there is a part of the zone not covered by any ZLPV -> because in that case it should be max speed
    #  even though there is a ZLPV intersecting the zone
    list_psr = get_zones_intersecting_zone(DCSYS.ZLPV, obj_type, obj_name)
    if not list_psr:
        return None
    min_speed = min([get_dc_sys_value(psr_name, DCSYS.ZLPV.VitesseZlpv) for psr_name in list_psr])
    return min_speed / 3.6  # convert to m/s


def get_min_psr_speed_on_zone_limits(zone_limits) -> Optional[float]:
    # TODO check if there is a part of the zone not covered by any ZLPV -> because in that case it should be max speed
    #  even though there is a ZLPV intersecting the zone
    list_psr = get_zones_intersecting_zone_limits(DCSYS.ZLPV, zone_limits)
    if not list_psr:
        return None
    min_speed = min([get_dc_sys_value(psr_name, DCSYS.ZLPV.VitesseZlpv) for psr_name in list_psr])
    return min_speed / 3.6  # convert to m/s
