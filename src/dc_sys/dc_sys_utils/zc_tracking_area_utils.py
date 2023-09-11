#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .segments_utils import *
from .switch_utils import give_sw_pos


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
        zc_limits.append((seg, x, (direction == "CROISSANT")))

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


def _get_zc_of_sw(obj_val: dict[str]) -> list[str]:
    seg, x = give_sw_pos(obj_val)
    return get_zc_of_point(seg, x)


def _get_zc_of_ovl(obj_val: dict[str]) -> list[str]:
    vsp_seg, vsp_x = list(get_dc_sys_zip_values(obj_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Seg,
                                                DCSYS.IXL_Overlap.VitalStoppingPoint.X))[0]
    rp_seg, rp_x = list(get_dc_sys_zip_values(obj_val, DCSYS.IXL_Overlap.ReleasePoint.Seg,
                                              DCSYS.IXL_Overlap.ReleasePoint.X))[0]
    return get_zc_of_extremities([(vsp_seg, vsp_x), (rp_seg, rp_x)])


def _get_zc_of_plt(obj_val: dict[str]) -> list[str]:
    limits = get_dc_sys_zip_values(obj_val, DCSYS.Quai.ExtremiteDuQuai.Seg, DCSYS.Quai.ExtremiteDuQuai.X)
    return get_zc_of_extremities(limits)


def _get_zc_of_traffic_stop(obj_val: dict[str]) -> list[str]:
    list_zc = list()
    plt_dict = load_sheet(DCSYS.Quai)
    for plt_name in get_dc_sys_value(obj_val, DCSYS.Traffic_Stop.PlatformList.Name):
        plt_val = plt_dict[plt_name]
        list_zc.extend([zc for zc in _get_zc_of_plt(plt_val) if zc not in list_zc])
    return list_zc


def _get_zc_of_calib(obj_val: dict[str]) -> list[str]:
    start_tag, end_tag = get_dc_sys_values(obj_val, DCSYS.Calib.BaliseDeb, DCSYS.Calib.BaliseFin)
    list_zc = get_zc_of_obj(DCSYS.Bal, start_tag)
    list_zc.extend([zc for zc in get_zc_of_obj(DCSYS.Bal, end_tag) if zc not in list_zc])
    return list_zc


def get_zc_of_obj(obj_type, obj_name: str) -> list[str]:
    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = get_sheet_attributes_columns_dict(obj_sh).keys()

    if get_sh_name(obj_type) == get_sh_name(DCSYS.Aig):  # a dedicated function for switches
        return _get_zc_of_sw(obj_val)
    elif get_sh_name(obj_type) == get_sh_name(DCSYS.IXL_Overlap):  # a dedicated function for overlaps
        return _get_zc_of_ovl(obj_val)
    elif get_sh_name(obj_type) == get_sh_name(DCSYS.Quai):  # a dedicated function for platforms
        return _get_zc_of_plt(obj_val)
    elif get_sh_name(obj_type) == get_sh_name(DCSYS.Traffic_Stop):  # a dedicated function for traffic stops
        return _get_zc_of_traffic_stop(obj_val)
    elif get_sh_name(obj_type) == get_sh_name(DCSYS.Calib):  # a dedicated function for calibration bases
        return _get_zc_of_calib(obj_val)
    elif "Seg" in sh_attrs and "X" in sh_attrs:
        seg, x = get_dc_sys_values(obj_val, obj_sh.Seg, obj_sh.X)
        return get_zc_of_point(seg, x)
    elif "Limit" in sh_attrs:
        limits = get_dc_sys_zip_values(obj_val, obj_sh.Limit.Seg, obj_sh.Limit.X)
        return get_zc_of_extremities(limits)
    elif "Extremite" in sh_attrs:
        limits = get_dc_sys_zip_values(obj_val, obj_sh.Extremite.Seg, obj_sh.Extremite.X)
        return get_zc_of_extremities(limits)
    elif "From" in sh_attrs and "To" in sh_attrs:
        lim1 = get_dc_sys_values(obj_val, obj_sh.From.Seg, obj_sh.To.X)
        lim2 = get_dc_sys_values(obj_val, obj_sh.To.Seg, obj_sh.To.X)
        return get_zc_of_extremities([lim1, lim2])
    elif "De" in sh_attrs and "A" in sh_attrs:
        lim1 = get_dc_sys_values(obj_val, obj_sh.De.Seg, obj_sh.De.X)
        lim2 = get_dc_sys_values(obj_val, obj_sh.A.Seg, obj_sh.A.X)
        return get_zc_of_extremities([lim1, lim2])
