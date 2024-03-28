#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point, get_zones_of_extremities


__all__ = ["get_max_psr_speed_at_point", "get_max_psr_speed_on_zone"]


def get_max_psr_speed_at_point(seg: str, x: float, direction: str = None) -> Optional[float]:
    list_psr = get_zones_on_point(DCSYS.ZLPV, seg, x, direction)
    if not list_psr:
        return None
    psr_dict = load_sheet(DCSYS.ZLPV)
    max_speed = max([get_dc_sys_value(psr_dict[psr_name], DCSYS.ZLPV.VitesseZlpv) for psr_name in list_psr])
    return max_speed / 3.6  # convert to m/s


def get_max_psr_speed_on_zone(limits: Union[list[tuple[str, float]], list[tuple[str, float, str]]]) -> Optional[float]:
    list_psr = get_zones_of_extremities(DCSYS.ZLPV, limits)  # TODO: to update to zone instead of extremities
    if not list_psr:
        return None
    psr_dict = load_sheet(DCSYS.ZLPV)
    max_speed = max([get_dc_sys_value(psr_dict[psr_name], DCSYS.ZLPV.VitesseZlpv) for psr_name in list_psr])
    return max_speed / 3.6  # convert to m/s
