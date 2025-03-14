#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point


__all__ = ["get_maz_of_point", "get_maz_of_extremities"]


def get_maz_of_point(seg: str, x: float, direction: str = None) -> Optional[str]:
    list_maz = get_zones_on_point(DCSYS.Zaum, seg, x, direction)
    if not list_maz:
        print_warning(f"No MAZ has been found covering {(seg, x)}.")
        return None
    if len(list_maz) > 1:
        print_warning(f"{(seg, x, direction)} is covered by multiple MAZ: {list_maz}.")
    return list_maz[0]


def get_maz_of_extremities(limits: Union[list[tuple[str, float]], list[tuple[str, float, str]]]) -> list[str]:
    list_maz = list()
    for lim in limits:
        seg, x = lim[0], lim[1]
        if len(lim) > 2:
            direction = get_reverse_direction(lim[2])  # for a single point object,
            # we consider it belongs to the zone upstream of it,
            # behavior is mimicked for the zone too
        else:
            direction = None
        maz = get_maz_of_point(seg, x, direction)
        if maz not in list_maz:
            list_maz.append(maz)
    return list_maz
