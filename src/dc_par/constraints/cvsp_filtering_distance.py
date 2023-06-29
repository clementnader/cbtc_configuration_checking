#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def min_dist_between_platform_osp_and_end_of_next_platform(in_cbtc: bool = True):
    if in_cbtc:
        plt_dict = get_plts_in_cbtc_ter()
    else:
        plt_dict = load_sheet("plt")
    plt_cols_name = get_cols_name("plt")

    dict_min_dist = dict()

    osp_name_cols = ['Y', 'AI', 'AS']
    osp_seg_cols = ['AA', 'AK', 'AU']
    osp_x_cols = ['AB', 'AL', 'AV']
    osp_direction_cols = ['AD', 'AN', 'AX']

    for i, (plt, plt_values) in enumerate(plt_dict.items()):
        for name_col, seg_col, x_col, direction_col in zip(osp_name_cols, osp_seg_cols, osp_x_cols, osp_direction_cols):
            osp_name = plt_values.get(plt_cols_name[name_col])
            if osp_name is not None:  # if OSP exists
                osp_seg = plt_values[plt_cols_name[seg_col]]
                osp_x = plt_values[plt_cols_name[x_col]]
                osp_direction = plt_values[plt_cols_name[direction_col]]
                if osp_direction in ("CROISSANT", "DOUBLE_SENS"):
                    key, value = get_dist_osp_next_plt(osp_name, osp_seg, osp_x, osp_direction, plt, plt_dict,
                                                       plt_cols_name, downstream=True)
                    if key is not None:
                        dict_min_dist[key] = value

                if osp_direction in ("DECROISSANT", "DOUBLE_SENS"):
                    key, value = get_dist_osp_next_plt(osp_name, osp_seg, osp_x, osp_direction, plt, plt_dict,
                                                       plt_cols_name, downstream=False)
                    if key is not None:
                        dict_min_dist[key] = value

    min_dist = min(osp_values["d"] for osp_values in dict_min_dist.values())
    res_list = [{osp_n_dir: osp_values} for osp_n_dir, osp_values in dict_min_dist.items()
                if osp_values['d'] == min_dist]
    print(f"\nThe minimum distance between a platform OSP and the end of the next platform is, "
          f"{print_in_cbtc(in_cbtc)}:"
          f"\n{min_dist = }"
          f"\n > for: {res_list}")
    return plt_dict


def get_dist_osp_next_plt(osp_name, osp_seg, osp_x, osp_direction, osp_plt, plt_dict, plt_cols_name, downstream: bool):
    direction_str = "downstream" if downstream else "upstream"

    closest_plt, d = get_closest_platform(osp_seg, osp_x, osp_plt, plt_dict, plt_cols_name, downstream=downstream)
    if closest_plt is None:
        print(f"{osp_name}_{direction_str} of {osp_plt} in {osp_direction = } is the last before End of Track")
        return None, None

    return f"{osp_name}_{direction_str}", {"origin_plt": osp_plt, "osp_direction": osp_direction,
                                           "closest_plt": closest_plt, "d": d}


def get_closest_platform(osp_seg, osp_x, osp_plt, plt_dict, plt_cols_name, downstream: bool):
    dist_osp_plt_dict = dict()
    for plt, plt_values in plt_dict.items():
        if plt != osp_plt:
            if downstream:
                plt_seg = plt_values[plt_cols_name['I']]  # closest end will be limit 1
                plt_x = float(plt_values[plt_cols_name['J']])
                d = get_dist_downstream(osp_seg, osp_x, plt_seg, plt_x)
            else:
                plt_seg = plt_values[plt_cols_name['Q']]  # closest end will be limit 2
                plt_x = float(plt_values[plt_cols_name['R']])
                d = get_dist_downstream(plt_seg, plt_x, osp_seg, osp_x)
            if d is not None:
                dist_osp_plt_dict[plt] = d
    if not dist_osp_plt_dict:
        return None, None
    min_d = min(dist_osp_plt_dict.values())
    closest_plt = [plt for plt, dist_value in dist_osp_plt_dict.items() if dist_value == min_d][0]
    return closest_plt, min_d
