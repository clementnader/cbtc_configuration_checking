#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


def min_dist_between_platform_osp_and_end_of_next_platform(in_cbtc: bool = True):
    if in_cbtc:
        plt_dict = get_platforms_in_cbtc_ter()
    else:
        plt_dict = load_sheet(DCSYS.Quai)
    dict_min_dist = dict()

    i: int
    for i, (plt, plt_value) in enumerate(plt_dict.items()):
        for osp_name, osp_seg, osp_x, osp_direction in get_dc_sys_zip_values(
                plt_value, DCSYS.Quai.PointDArret.Name, DCSYS.Quai.PointDArret.Seg,
                DCSYS.Quai.PointDArret.X, DCSYS.Quai.PointDArret.SensApproche):
            if osp_name is not None:  # if OSP exists
                if osp_direction in [StoppingPointApproachType.CROISSANT, StoppingPointApproachType.DOUBLE_SENS]:
                    key, value = get_dist_osp_next_plt(osp_name, osp_seg, osp_x, osp_direction, plt, plt_dict,
                                                       downstream=True)
                    if key is not None:
                        dict_min_dist[key] = value

                if osp_direction in [StoppingPointApproachType.DECROISSANT, StoppingPointApproachType.DOUBLE_SENS]:
                    key, value = get_dist_osp_next_plt(osp_name, osp_seg, osp_x, osp_direction, plt, plt_dict,
                                                       downstream=False)
                    if key is not None:
                        dict_min_dist[key] = value

    cvsp_filtering_distance = min(osp_value["d"] for osp_value in dict_min_dist.values())
    res_list = [{osp_n_dir: osp_value} for osp_n_dir, osp_value in dict_min_dist.items()
                if osp_value['d'] == cvsp_filtering_distance]
    print(f"\nThe minimum distance between a platform OSP and the end of the next platform is, "
          f"{print_in_cbtc(in_cbtc)}:"
          f"\n{cvsp_filtering_distance = }"
          f"\n > for: {res_list}")
    return plt_dict


def get_dist_osp_next_plt(osp_name, osp_seg, osp_x, osp_direction, osp_plt, plt_dict, downstream: bool):
    direction_str = "downstream" if downstream else "upstream"

    closest_plt, d = get_closest_platform(osp_seg, osp_x, osp_plt, plt_dict, downstream=downstream)
    if closest_plt is None:
        print_log(f"{osp_name}_{direction_str} of {osp_plt} in {osp_direction = } is the last before End of Track")
        return None, None

    return f"{osp_name}_{direction_str}", {"origin_plt": osp_plt, "osp_direction": osp_direction,
                                           "closest_plt": closest_plt, "d": d}


def get_closest_platform(osp_seg, osp_x, osp_plt, plt_dict, downstream: bool):
    dist_osp_plt_dict = dict()
    for plt, plt_value in plt_dict.items():
        if plt != osp_plt:
            plt_limits = list(get_dc_sys_zip_values(plt_value, DCSYS.Quai.ExtremiteDuQuai.Seg,
                                                    DCSYS.Quai.ExtremiteDuQuai.X))
            if downstream:
                plt_seg, plt_x = plt_limits[0]  # closest end will be limit 1
                d = get_dist_downstream(osp_seg, osp_x, plt_seg, plt_x, downstream=True)
            else:
                plt_seg, plt_x = plt_limits[1]  # closest end will be limit 2
                d = get_dist_downstream(osp_seg, osp_x, plt_seg, plt_x, downstream=False)
            if d is not None:
                dist_osp_plt_dict[plt] = d
    if not dist_osp_plt_dict:
        return None, None
    min_d = min(dist_osp_plt_dict.values())
    closest_plt = [plt for plt, dist_value in dist_osp_plt_dict.items() if dist_value == min_d][0]
    return closest_plt, min_d
