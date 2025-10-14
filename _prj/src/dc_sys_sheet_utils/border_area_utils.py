#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point, get_segments_within_zone
from ..dc_sys_draw_path.dc_sys_path_and_distances import get_downstream_path


__all__ = ["get_all_possible_border_areas"]


def get_all_possible_border_areas():
    zc_limits_within_other_zc = _get_zc_limits_within_other_zc()
    for zc1, sub_dict1 in zc_limits_within_other_zc.items():
        for zc2, list_of_zc1_limits in sub_dict1.items():
            sub_dict2 = zc_limits_within_other_zc.get(zc2)
            if sub_dict2 is None:
                continue
            list_of_zc2_limits = sub_dict2.get(zc1)
            if list_of_zc2_limits is None:
                continue

            for limit1 in list_of_zc1_limits:
                for limit2 in list_of_zc2_limits:
                    _get_tc_along_the_route(limit1, limit2, zc1, zc2)


def _get_zc_limits_within_other_zc() -> dict[str, dict[str, list[tuple[str, float, str]]]]:
    zc_limits_within_other_zc = dict()
    zc_list = get_objects_list(DCSYS.PAS)
    for zc_name in zc_list:
        zc_limits = get_object_zone_limits(DCSYS.PAS, zc_name)
        for limit_seg, limit_x, limit_direction in zc_limits:
            test_direction = get_opposite_direction(limit_direction)
            # for a single point object, we consider it belongs to the zone upstream of it,
            # behavior is mimicked for the zone limits too
            other_zc = get_zones_on_point(DCSYS.PAS, limit_seg, limit_x, test_direction)
            other_zc = [zc for zc in other_zc if zc != zc_name]

            if other_zc:  # ZC limit is in another ZC
                if len(other_zc) > 1:
                    print_error(f"3 ZCs are overlapping: {zc_name} limit {limit_seg, limit_x, limit_direction} "
                                f"is on multiple other ZCs: {other_zc}")

                other_zc = other_zc[0]
                if zc_name not in zc_limits_within_other_zc:
                    zc_limits_within_other_zc[zc_name] = dict()
                if other_zc not in zc_limits_within_other_zc[zc_name]:
                    zc_limits_within_other_zc[zc_name][other_zc] = list()
                zc_limits_within_other_zc[zc_name][other_zc].append((limit_seg, limit_x, limit_direction))

    return zc_limits_within_other_zc


def _get_tc_along_the_route(limit1: tuple[str, float, str], limit2: tuple[str, float, str],
                            zc1: str, zc2: str):
    lim_seg1, lim_x1, lim_direction1 = limit1
    lim_downstream1 = (lim_direction1 == Direction.CROISSANT)
    lim_seg2, lim_x2, lim_direction2 = limit2
    lim_upstream2 = (lim_direction2 == Direction.DECROISSANT)

    _, _, list_of_paths, _ = get_downstream_path(start_seg=lim_seg1, end_seg=lim_seg2,
                                                 start_downstream=lim_downstream1, end_upstream=lim_upstream2)
    if not list_of_paths:
        return None

    list_of_paths_within_zcs = list()
    for _, path in list_of_paths:
        if (all(seg in get_segments_within_zone(DCSYS.PAS, zc1) for seg in path[1:-1])
                and all(seg in get_segments_within_zone(DCSYS.PAS, zc2) for seg in path[1:-1])):
            list_of_paths_within_zcs.append(path)
    if not list_of_paths_within_zcs:
        return None

    print(zc1, zc2, lim_seg1, lim_downstream1, lim_seg2, lim_upstream2, list_of_paths_within_zcs)
    exit(0)
