#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_common_utils import *
from ..dc_sys_path_and_distances import *


__all__ = ["get_min_and_max_slopes_at_point", "get_min_and_max_slopes_on_virtual_seg"]


def get_slope_at_point(seg: str, x: float) -> float:
    slope_dict = load_sheet(DCSYS.Profil)

    downstream_slope = get_next_slope(seg, x, slope_dict, downstream=True)
    upstream_slope = get_next_slope(seg, x, slope_dict, downstream=False)

    downstream_seg, downstream_x = get_dc_sys_values(downstream_slope, DCSYS.Profil.Seg, DCSYS.Profil.X)
    downstream_slope_value = get_dc_sys_value(downstream_slope, DCSYS.Profil.Pente)

    upstream_seg, upstream_x = get_dc_sys_values(upstream_slope, DCSYS.Profil.Seg, DCSYS.Profil.X)
    upstream_slope_value = get_dc_sys_value(upstream_slope, DCSYS.Profil.Pente)

    if (seg, x) == (downstream_seg, downstream_x):
        return downstream_slope_value
    if (seg, x) == (upstream_seg, upstream_x):
        return upstream_slope_value

    total_distance = get_dist_downstream(upstream_seg, upstream_x, downstream_seg, downstream_x, downstream=True)
    if total_distance is None:
        # TODO solve problem with depol, cf Milan
        print(upstream_seg, upstream_x, downstream_seg, downstream_x)
        return 0.
    sub_distance = get_dist_downstream(upstream_seg, upstream_x, seg, x, downstream=True)
    # linear approximation of the slope between two points
    slope_value = (downstream_slope_value - upstream_slope_value) / total_distance * sub_distance + upstream_slope_value
    return slope_value


def get_next_slope(start_seg: str, start_x: float, slope_dict: dict, downstream: bool) -> Optional[dict]:
    slopes = list()

    def inner_recurs_next_seg(seg: str, x: float = None):
        nonlocal slopes
        slope = is_slope_defined(seg, slope_dict, downstream=downstream, x=x)
        if slope is not False:
            slopes.append(slope)
            return
        for next_seg in get_linked_segs(seg, downstream=downstream):
            inner_recurs_next_seg(next_seg)

    inner_recurs_next_seg(start_seg, start_x)

    if not slopes:
        print_warning(f"No slope found {'downstream' if downstream else 'upstream'} {(start_seg, start_x)}.")
        return None
    if len(slopes) > 1:
        slopes.sort(
            key=lambda slope: get_dist_downstream(start_seg, start_x, *get_dc_sys_values(
                slope, DCSYS.Profil.Seg, DCSYS.Profil.X), downstream=downstream))
    return slopes[0]


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

    slopes = get_slopes_between(seg1, x1, seg2, x2, slope_dict)
    slopes_values = [float(get_dc_sys_value(slope, DCSYS.Profil.Pente)) for slope in slopes]
    slopes_values.append(get_slope_at_point(seg1, x1))
    slopes_values.append(get_slope_at_point(seg2, x2))
    return min(slopes_values), max(slopes_values)


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
                    if ((start_seg != slope_seg or start_x <= slope_x)
                            and (end_seg != slope_seg or end_x >= slope_x)):
                        slopes.append(slope)

    return slopes
