#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .segments_utils import *
from .cbtc_territory_utils import is_point_in_cbtc_ter
from .dist_utils import get_downstream_path, get_virtual_seg_ordered_extremities


__all__ = ["get_slopes_in_cbtc_ter", "get_min_and_max_slopes_at_point", "get_min_and_max_slopes_on_virtual_seg"]


def get_slopes_in_cbtc_ter():
    slope_dict = load_sheet(DCSYS.Profil)
    within_cbtc_slope_dict = dict()
    for slope, slope_info in slope_dict.items():
        slope_seg = get_dc_sys_value(slope_info, DCSYS.Profil.Seg)
        slope_x = float(get_dc_sys_value(slope_info, DCSYS.Profil.X))
        if is_point_in_cbtc_ter(slope_seg, slope_x) is not False:
            within_cbtc_slope_dict[slope] = slope_info
        if is_point_in_cbtc_ter(slope_seg, slope_x) is None:
            print_warning(f"Slope {slope} is defined on a limit of CBTC Territory. "
                          f"It is still taken into account."
                          f"\n\t{slope_info}")
    return within_cbtc_slope_dict


def get_min_and_max_slopes_at_point(seg, x):
    slope_dict = load_sheet(DCSYS.Profil)

    slopes = get_next_slopes(seg, x, slope_dict, downstream=True)
    slopes.extend(get_next_slopes(seg, x, slope_dict, downstream=False))
    slopes_value = [float(get_dc_sys_value(slope, DCSYS.Profil.Pente)) for slope in slopes]
    return min(slopes_value), max(slopes_value)


def get_next_slopes(start_seg, start_x, slope_dict: dict, downstream: bool):
    slopes = list()

    def inner_recurs_next_seg(seg, x: float = None):
        nonlocal slopes
        slope = is_slope_defined(seg, slope_dict, downstream=downstream, x=x)
        if slope is not False:
            slopes.append(slope)
            return
        for next_seg in get_linked_segs(seg, downstream=downstream):
            inner_recurs_next_seg(next_seg)

    inner_recurs_next_seg(start_seg, start_x)
    return slopes


def is_slope_defined(seg, slope_dict: dict, downstream: bool = True, x: float = None):
    if x is not None:
        x = float(x)
    slopes = list()
    for slope in slope_dict.values():
        slope_seg = get_dc_sys_value(slope, DCSYS.Profil.Seg)
        slope_x = float(get_dc_sys_value(slope, DCSYS.Profil.X))
        if seg == slope_seg:
            if downstream:
                if x is None or x <= slope_x:
                    slopes.append(slope)
            else:
                if x is None or x >= slope_x:
                    slopes.append(slope)
    if not slopes:
        return False
    # Return closest slope
    slopes.sort(key=lambda a: float(get_dc_sys_value(a, DCSYS.Profil.X)))  # sort according to offset value
    if downstream:
        return slopes[0]
    else:
        return slopes[-1]


def get_min_and_max_slopes_on_virtual_seg(seg1, x1, seg2, x2):
    slope_dict = load_sheet(DCSYS.Profil)
    # TODO: manage depolarization
    seg1, x1, seg2, x2 = get_virtual_seg_ordered_extremities(seg1, x1, seg2, x2)  # assert seg1 is upstream of seg2

    slopes = get_next_slopes(seg2, x2, slope_dict, downstream=True)
    slopes.extend(get_next_slopes(seg1, x1, slope_dict, downstream=False))
    slopes.extend(get_slopes_between(seg1, x1, seg2, x2, slope_dict))
    slopes_value = [float(get_dc_sys_value(slope, DCSYS.Profil.Pente)) for slope in slopes]
    return min(slopes_value), max(slopes_value)


def get_slopes_between(start_seg, start_x, end_seg, end_x, slope_dict: dict):
    start_x = float(start_x)
    end_x = float(end_x)

    _, _, list_paths, _ = get_downstream_path(start_seg, end_seg, start_downstream=True)

    slopes = list()
    for _, path in list_paths:
        for seg in path:
            for slope in slope_dict.values():
                slope_seg = get_dc_sys_value(slope, DCSYS.Profil.Seg)
                slope_x = float(get_dc_sys_value(slope, DCSYS.Profil.X))
                if seg == slope_seg:
                    if (start_seg != slope_seg or start_x <= slope_x) \
                            and (end_seg != slope_seg or end_x >= slope_x):
                        slopes.append(slope)

    return slopes
