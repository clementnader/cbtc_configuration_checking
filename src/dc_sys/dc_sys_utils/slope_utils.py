#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database.load_sheets import load_sheet, get_cols_name
from .cbtc_territory_utils import is_point_in_cbtc_ter
from .dist_utils import *
from .path_utils import is_seg_downstream


def get_slopes_in_cbtc_ter():
    slope_dict = load_sheet("slope")
    slope_cols_name = get_cols_name("slope")
    within_cbtc_slope_dict = dict()
    for slope, slope_values in slope_dict.items():
        slope_seg = slope_values[slope_cols_name['B']]
        slope_x = float(slope_values[slope_cols_name['C']])
        if is_point_in_cbtc_ter(slope_seg, slope_x) is not False:
            within_cbtc_slope_dict[slope] = slope_values
        if is_point_in_cbtc_ter(slope_seg, slope_x) is None:
            print_warning(f"Slope {slope} is defined on a limit of CBTC Territory. "
                          f"It is still taken into account."
                          f"\n\t{slope_values}")
    return within_cbtc_slope_dict


def get_min_and_max_slopes_at_point(seg, x):
    slope_dict = load_sheet("slope")
    slope_cols_name = get_cols_name("slope")

    slopes = get_next_slopes(seg, x, slope_dict, slope_cols_name, downstream=True)
    slopes.extend(get_next_slopes(seg, x, slope_dict, slope_cols_name, downstream=False))
    slopes_values = [float(slope[slope_cols_name['A']]) for slope in slopes]
    return min(slopes_values), max(slopes_values)


def get_next_slopes(start_seg, start_x, slope_dict: dict, slope_cols_name: dict[str, str], downstream: bool = True):
    slopes = list()

    def inner_recurs_next_seg(seg, x: float = None):
        nonlocal slopes
        slope = is_slope_defined(seg, slope_dict, slope_cols_name, downstream=downstream, x=x)
        if slope is not False:
            slopes.append(slope)
            return
        for next_seg in get_linked_segs(seg, downstream=downstream):
            inner_recurs_next_seg(next_seg)

    inner_recurs_next_seg(start_seg, start_x)
    return slopes


def is_slope_defined(seg, slope_dict: dict, slope_cols_name: dict[str, str], downstream: bool = True, x: float = None):
    if x is not None:
        x = float(x)
    slopes = list()
    for slope in slope_dict.values():
        slope_seg = slope[slope_cols_name['B']]
        slope_x = float(slope[slope_cols_name['C']])
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
    slopes.sort(key=lambda a: float(a[slope_cols_name['C']]))  # sort according to offset value
    if downstream:
        return slopes[0]
    else:
        return slopes[-1]


def get_min_and_max_slopes_on_virtual_seg(seg1, x1, seg2, x2):
    slope_dict = load_sheet("slope")
    slope_cols_name = get_cols_name("slope")

    if not is_seg_downstream(seg1, seg2, x1, x2):  # assert seg1 is upstream of seg2
        seg1, seg2 = seg2, seg1
        x1, x2 = x2, x1

    slopes = get_next_slopes(seg2, x2, slope_dict, slope_cols_name, downstream=True)
    slopes.extend(get_next_slopes(seg1, x1, slope_dict, slope_cols_name, downstream=False))
    slopes.extend(get_slopes_between(seg1, x1, seg2, x2, slope_dict, slope_cols_name))
    slopes_values = [float(slope[slope_cols_name['A']]) for slope in slopes]
    return min(slopes_values), max(slopes_values)


def get_slopes_between(start_seg, start_x, end_seg, end_x, slope_dict: dict, slope_cols_name: dict[str, str]):
    start_x = float(start_x)
    end_x = float(end_x)

    _, _, list_paths = get_downstream_path(start_seg, end_seg)

    slopes = list()
    for path in list_paths:
        for seg in path:
            for slope in slope_dict.values():
                slope_seg = slope[slope_cols_name['B']]
                slope_x = float(slope[slope_cols_name['C']])
                if seg == slope_seg:
                    if (start_seg != slope_seg or start_x <= slope_x)\
                            and (end_seg != slope_seg or end_x >= slope_x):
                        slopes.append(slope)

    return slopes
