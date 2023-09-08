#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .cbtc_territory_utils import is_point_in_cbtc_ter
from .dist_utils import is_seg_downstream


__all__ = ["get_plts_in_cbtc_ter", "get_atb_zone_related_to_plt", "is_platform_limit_1_upstream_limit_2"]


def get_plts_in_cbtc_ter():
    plt_dict = load_sheet(DCSYS.Quai)
    within_cbtc_plt_dict = dict()
    for plt_name, plt_value in plt_dict.items():
        limit_in_cbtc = list()
        for limit_seg, limit_x in get_dc_sys_zip_values(plt_value, DCSYS.Quai.ExtremiteDuQuai.Seg,
                                                        DCSYS.Quai.ExtremiteDuQuai.X):
            limit_in_cbtc.append(is_point_in_cbtc_ter(limit_seg, limit_x))

        if all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limit_in_cbtc):
            within_cbtc_plt_dict[plt_name] = plt_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limit_in_cbtc):
            print_warning(f"Platform {plt_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_plt_dict[plt_name] = plt_value
    return within_cbtc_plt_dict


def get_atb_zone_related_to_plt(plt_name):
    atb_zone_dict = load_sheet(DCSYS.ZCRA)
    related_atb_mvt = list()
    for atb_zone_name, atb_zone in atb_zone_dict.items():
        if get_dc_sys_value(atb_zone, DCSYS.ZCRA.MouvZcra.QuaiOrigine)[0] == plt_name:
            related_atb_mvt.append((atb_zone_name, atb_zone))
    return related_atb_mvt


def is_platform_limit_1_upstream_limit_2(plt_name):
    plt_dict = load_sheet(DCSYS.Quai)
    plt = plt_dict[plt_name]
    (seg_lim1, x_lim1), (seg_lim2, x_lim2) = get_dc_sys_zip_values(plt, DCSYS.Quai.ExtremiteDuQuai.Seg,
                                                                   DCSYS.Quai.ExtremiteDuQuai.X)
    is_seg1_upstream = is_seg_downstream(seg_lim2, seg_lim1, x_lim2, x_lim1, downstream=False)
    is_seg1_downstream = is_seg_downstream(seg_lim2, seg_lim1, x_lim2, x_lim1, downstream=True)
    if is_seg1_upstream:
        return True
    if is_seg1_downstream:
        return False
    raise Exception(f"Unable to find a path between the two limits of platform {plt_name}:\n"
                    f"No path between {(seg_lim1, x_lim1)} and {(seg_lim2, x_lim2)}.")
