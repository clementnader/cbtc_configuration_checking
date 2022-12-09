#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_sys import *


def get_slope_at_plt():
    plt_dict = load_sheet("plt")
    plt_cols_name = get_cols_name("plt")

    slope_dict = load_sheet("slope")
    slope_cols_name = get_cols_name("slope")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    dict_plt_slopes = dict()
    for plt in plt_dict:
        dict_plt_slopes[plt] = get_slope_plt(plt_dict[plt], plt_cols_name,
                                             slope_dict, slope_cols_name, seg_dict, seg_cols_name)

    min_slope = min(dict_plt_slopes[plt] for plt in dict_plt_slopes)
    max_slope = max(dict_plt_slopes[plt] for plt in dict_plt_slopes)
    print(f"{min_slope=:.4%}"
          f"\nfor {[plt for plt in dict_plt_slopes if dict_plt_slopes[plt] == min_slope]}"
          f"\n{max_slope=:.4%}"
          f"\nfor {[plt for plt in dict_plt_slopes if dict_plt_slopes[plt] == max_slope]}")
    return dict_plt_slopes


def get_slope_plt(plt, plt_cols_name, slope_dict, slope_cols_name, seg_dict, seg_cols_name):
    seg_lim1 = plt[plt_cols_name['I']]
    x_lim1 = float(plt[plt_cols_name['J']])

    def inner_recurs_previous_seg(seg, x: float = None):
        seg_slope = slope_on_seg_upstream(seg, slope_dict, slope_cols_name, x)
        if seg_slope is not None:
            return seg_slope
        for previous_seg in get_linked_segs(seg, seg_dict=seg_dict, seg_cols_name=seg_cols_name, downstream=False):
            if previous_seg:
                return inner_recurs_previous_seg(previous_seg)

    return inner_recurs_previous_seg(seg_lim1, x_lim1)


def slope_on_seg_upstream(seg, slope_dict, slope_cols_name, x: float = None):
    list_slopes = list()
    for slope in slope_dict:
        if slope_dict[slope][slope_cols_name['B']] == seg:
            if x is None or float(slope_dict[slope][slope_cols_name['C']]) <= x:  # if x is specified,
                # check if the slope is taken upstream (on the left) of the (seg, x) point
                list_slopes.append(slope_dict[slope])
    if list_slopes:
        max_x = max(float(slope[slope_cols_name['C']]) for slope in list_slopes)  # get the value with the greatest x,
        # i.e. corresponding to the furthest in the right
        return [float(slope[slope_cols_name['A']]) for slope in list_slopes
                if float(slope[slope_cols_name['C']]) == max_x][0]
    else:
        return None
