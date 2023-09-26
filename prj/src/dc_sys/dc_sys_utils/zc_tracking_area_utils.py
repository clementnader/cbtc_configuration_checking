#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .global_utils import *
from .segments_utils import *


__all__ = ["get_all_zc", "get_segs_within_zc", "get_all_segs_in_zc", "get_zc_limits",
           "is_point_in_zc", "get_zc_of_point", "get_zc_of_extremities", "get_zc_of_obj"]


ZC_SEGMENTS = dict()
ZC_LIMITS = dict()


def get_all_zc():
    zc_dict = load_sheet(DCSYS.PAS)
    return list(zc_dict.keys())


def get_segs_within_zc(zc_name: str) -> set[str]:
    global ZC_SEGMENTS
    if not ZC_SEGMENTS:
        update_segs_within_zc()
    return set([seg for seg, _ in ZC_SEGMENTS[zc_name]])


def get_all_segs_in_zc(zc_name: str) -> set[str]:
    zc_segments = get_segs_within_zc(zc_name)
    zc_limits = get_zc_limits(zc_name)
    return zc_segments.union([seg for seg, _, _ in zc_limits])


def get_zc_limits(zc_name: str) -> list[tuple[str, float, bool]]:
    global ZC_LIMITS
    if not ZC_LIMITS:
        update_segs_within_zc()
    return ZC_LIMITS[zc_name]


def update_segs_within_zc() -> None:
    global ZC_SEGMENTS
    if ZC_SEGMENTS:
        return

    zc_dict = load_sheet(DCSYS.PAS)
    for zc_name, zc_info in zc_dict.items():
        ZC_SEGMENTS[zc_name] = list()

        zc_limits = get_start_and_end_limits_zc(zc_info)

        for start_lim in zc_limits:
            start_seg, _, start_direction = start_lim
            get_next_segments(zc_name, start_seg, start_direction, zc_limits)

        update_zc_limits(zc_name, zc_limits)


def get_start_and_end_limits_zc(zc_info: dict[str]) -> list[tuple[str, float, bool]]:
    zc_limits = list()

    for seg, x, direction in get_dc_sys_zip_values(zc_info, DCSYS.PAS.ExtremiteSuivi.Seg,
                                                   DCSYS.PAS.ExtremiteSuivi.X, DCSYS.PAS.ExtremiteSuivi.Sens):
        zc_limits.append((seg, x, (direction == Direction.CROISSANT)))

    return zc_limits


def get_next_segments(zc_name: str, start_seg: str, downstream: bool, zc_limits: list[tuple[str, float, bool]]) -> None:
    global ZC_SEGMENTS

    def inner_recurs_next_seg(seg: str, inner_downstream: bool):
        global ZC_SEGMENTS
        for next_seg in get_linked_segs(seg, inner_downstream):
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            if is_seg_end_limit(next_seg, next_inner_downstream, zc_limits):
                continue
            if (next_seg, next_inner_downstream) in ZC_SEGMENTS[zc_name]:
                continue
            ZC_SEGMENTS[zc_name].append((next_seg, next_inner_downstream))
            inner_recurs_next_seg(next_seg, next_inner_downstream)

    inner_recurs_next_seg(start_seg, downstream)


def is_seg_end_limit(seg: str, downstream: bool, zc_limits: list[tuple[str, float, bool]]) -> bool:
    if (seg, not downstream) in [(limit_seg, limit_downstream) for limit_seg, _, limit_downstream in zc_limits]:
        return True
    if seg in [limit_seg for limit_seg, _, _ in zc_limits]:
        print_warning("Reach a ZC Tracking limit but with a different direction.")
        print(f"{seg = }, {downstream = }")
        print([limit_seg for limit_seg, _, _ in zc_limits if seg == limit_seg])
        return True
    return False


def update_zc_limits(zc_name: str, zc_limits: list[tuple[str, float, bool]]) -> None:
    global ZC_LIMITS
    ZC_LIMITS[zc_name] = list()
    for lim in zc_limits:
        ZC_LIMITS[zc_name].append(lim)


def is_point_in_zc(seg: str, x: float, zc_name: str) -> Optional[bool]:
    x = float(x)
    zc_segments = get_segs_within_zc(zc_name)
    zc_limits = get_zc_limits(zc_name)
    if seg in zc_segments:
        return True
    for lim in zc_limits:
        lim_seg, lim_x, lim_downstream = lim
        if seg == lim_seg:
            if x == lim_x:  # limit point
                return None
            if lim_downstream and x > lim_x:
                return True
            if not lim_downstream and x < lim_x:
                return True
    return False


def get_zc_of_point(seg: str, x: float) -> list[str]:
    list_zc = list()
    for zc_name in get_all_zc():
        if is_point_in_zc(seg, x, zc_name) is True:
            list_zc.append(zc_name)
        # if is_point_in_zc(seg, x, zc_name) is None:
        #     print(f"Point {(seg, x)} is at limit of {zc_name}.")
    return list_zc


def get_zc_of_extremities(limits: list[tuple[str, float]]) -> list[str]:
    list_zc = list()
    for lim in limits:
        seg, x = lim[0], lim[1]
        list_zc.extend([zc for zc in get_zc_of_point(seg, x) if zc not in list_zc])
    return list_zc


def _get_zc_of_traffic_stop(obj_name: str) -> list[str]:
    obj_dict = load_sheet(DCSYS.Traffic_Stop)
    obj_val = obj_dict[obj_name]
    list_zc = list()
    for plt_name in get_dc_sys_value(obj_val, DCSYS.Traffic_Stop.PlatformList.Name):
        list_zc.extend([zc for zc in get_zc_of_obj(DCSYS.Quai, plt_name) if zc not in list_zc])
    return list_zc


def get_zc_of_obj(obj_type, obj_name: str) -> Optional[list[str]]:
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Traffic_Stop):  # a dedicated function for traffic stops
        return _get_zc_of_traffic_stop(obj_name)
    position = get_obj_position(obj_type, obj_name)
    if isinstance(position, tuple):
        return get_zc_of_point(*position)
    if isinstance(position, list):
        return get_zc_of_extremities(position)
    return None
