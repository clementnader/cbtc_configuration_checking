#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ..load_database import *
from .segments_utils import *
from .switch_utils import give_sw_pos


__all__ = ["get_all_zc", "is_point_in_zc", "get_zc_of_point", "get_zc_of_obj"]


ZC_SEGMENTS = dict()
ZC_LIMITS = dict()


def get_all_zc():
    zc_dict = load_sheet(DCSYS.PAS)
    return list(zc_dict.keys())


def update_segs_within_zc():
    global ZC_SEGMENTS, ZC_LIMITS
    if ZC_SEGMENTS:
        return

    zc_dict = load_sheet(DCSYS.PAS)
    for zc_name, zc_info in zc_dict.items():
        ZC_SEGMENTS[zc_name] = list()
        ZC_LIMITS[zc_name] = list()

        start_zc_limits, end_zc_limits = get_start_and_end_limits_zc(zc_info)

        for start_lim in start_zc_limits:
            start_seg, _, _ = start_lim
            get_next_segments(start_seg, end_zc_limits, ZC_SEGMENTS[zc_name])

        update_zc_limits(zc_name, start_zc_limits)
        update_zc_limits(zc_name, end_zc_limits)


def get_start_and_end_limits_zc(zc_info):
    start_zc_limits = list()
    end_zc_limits = list()

    for seg, x, direction in get_dc_sys_zip_values(zc_info, DCSYS.PAS.ExtremiteSuivi.Seg,
                                                   DCSYS.PAS.ExtremiteSuivi.X, DCSYS.PAS.ExtremiteSuivi.Sens):
        if direction == "CROISSANT":
            start_zc_limits.append((seg, x, direction))
        else:
            end_zc_limits.append((seg, x, direction))
    return start_zc_limits, end_zc_limits


def get_next_segments(start_seg, end_zc_limits, zc_segments):
    # check downstream segments

    def inner_recurs_next_seg(seg):
        nonlocal zc_segments
        if is_seg_end_limit(seg, end_zc_limits):
            return zc_segments
        zc_segments.append(seg)
        for next_seg in get_linked_segs(seg, downstream=True):
            if next_seg not in zc_segments:
                inner_recurs_next_seg(next_seg)

    inner_recurs_next_seg(start_seg)


def is_seg_end_limit(seg, end_zc_limits):
    return seg in [end_seg for end_seg, _, _ in end_zc_limits]


def update_zc_limits(zc_name, zc_limits):
    global ZC_LIMITS
    for lim in zc_limits:
        ZC_LIMITS[zc_name].append(lim)


def is_point_in_zc(seg: str, x: float, zc_name: str):
    global ZC_SEGMENTS, ZC_LIMITS
    x = float(x)
    if not ZC_SEGMENTS:
        update_segs_within_zc()
    if seg in ZC_SEGMENTS[zc_name]:
        return True
    for lim in ZC_LIMITS[zc_name]:
        lim_seg, lim_x, lim_direction = lim
        if seg == lim_seg:
            if x == lim_x:  # limit point
                return None
            if lim_direction == "CROISSANT" and x > lim_x:
                return True
            if lim_direction == "DECROISSANT" and x < lim_x:
                return True
    return False


def get_zc_of_point(seg: str, x: float):
    global ZC_SEGMENTS
    if not ZC_SEGMENTS:
        update_segs_within_zc()

    list_zc = list()
    for zc_name in ZC_SEGMENTS.keys():
        if is_point_in_zc(seg, x, zc_name) is True:
            list_zc.append(zc_name)
    return list_zc


def get_zc_of_extremities(extremities: list):
    list_zc = list()
    for lim in extremities:
        seg, x = lim[0], lim[1]
        list_zc.extend([zc for zc in get_zc_of_point(seg, x) if zc not in list_zc])
    return list_zc


def _get_zc_of_sw(obj_val):
    seg, x = give_sw_pos(obj_val)
    return get_zc_of_point(seg, x)


def _get_zc_of_ovl(obj_val):
    vsp_seg, vsp_x = list(get_dc_sys_zip_values(obj_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Seg,
                                                DCSYS.IXL_Overlap.VitalStoppingPoint.X))[0]
    rp_seg, rp_x = list(get_dc_sys_zip_values(obj_val, DCSYS.IXL_Overlap.ReleasePoint.Seg,
                                              DCSYS.IXL_Overlap.ReleasePoint.X))[0]
    return get_zc_of_extremities([(vsp_seg, vsp_x), (rp_seg, rp_x)])


def _get_zc_of_plt(obj_val):
    limits = get_dc_sys_zip_values(obj_val, DCSYS.Quai.ExtremiteDuQuai.Seg, DCSYS.Quai.ExtremiteDuQuai.X)
    return get_zc_of_extremities(limits)


def _get_zc_of_traffic_stop(obj_val):
    list_zc = list()
    plt_dict = load_sheet(DCSYS.Quai)
    for plt_name in get_dc_sys_value(obj_val, DCSYS.Traffic_Stop.PlatformList.Name):
        plt_val = plt_dict[plt_name]
        list_zc.extend([zc for zc in _get_zc_of_plt(plt_val) if zc not in list_zc])
    return list_zc


def _get_zc_of_calib(obj_val):
    start_tag, end_tag = get_dc_sys_values(obj_val, DCSYS.Calib.BaliseDeb, DCSYS.Calib.BaliseFin)
    list_zc = get_zc_of_obj(DCSYS.Bal, start_tag)
    list_zc.extend([zc for zc in get_zc_of_obj(DCSYS.Bal, end_tag) if zc not in list_zc])
    return list_zc


def get_zc_of_obj(obj_type, obj_name: str):
    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = list(get_sheet_attributes_columns_dict(obj_sh).keys())

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
