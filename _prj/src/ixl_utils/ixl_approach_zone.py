#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_sheet_utils.ivb_utils import get_related_block_of_ivb
from ..dc_sys_draw_path.dc_sys_path_and_distances import get_dist_downstream
from .load_ixl_apz import get_approach_area_ivb_from_excel_file, ixl_apz_definition_file


__all__ = ["get_distance_between_block_and_approach_zone"]


def get_distance_between_block_and_approach_zone(sig_name: str, ivb_lim_seg, ivb_lim_x, apz_with_tc: bool = False):
    list_ivb = _get_approach_area_ivb(sig_name, apz_with_tc)
    if not list_ivb:
        print(f"\nThe signal {sig_name} has no IXL approach area: {list_ivb}")
        return None, None, None
    ivb_names = ", ".join(list_ivb)
    list_entrance_points = _get_entrance_points_of_approach_zone(sig_name, list_ivb)
    min_dist = None
    corresponding_entrance = None

    sig_dict = load_sheet(DCSYS.Sig)
    sig_direction = get_dc_sys_value(sig_dict[sig_name], DCSYS.Sig.Sens)
    for entrance_seg, entrance_x in list_entrance_points:
        if are_points_matching(entrance_seg, entrance_x, ivb_lim_seg, ivb_lim_x):
            continue
        dist = get_dist_downstream(ivb_lim_seg, ivb_lim_x, entrance_seg, entrance_x,
                                   downstream=sig_direction == Direction.DECROISSANT)  # get dist upstream
        if dist is None:
            continue
        if min_dist is None or dist < min_dist:
            min_dist = dist
            corresponding_entrance = (entrance_seg, entrance_x)
    return min_dist, corresponding_entrance, ivb_names


def _get_entrance_points_of_approach_zone(sig_name: str, list_ivb: list[str]) -> list[tuple[str, float]]:
    ivb_dict = load_sheet(DCSYS.IVB)
    tc_dict = load_sheet(DCSYS.CDV)
    list_points = list()
    for ivb_name in list_ivb:
        if ivb_name not in tc_dict and ivb_name in ivb_dict:
            obj_type = "IVB"
        elif ivb_name not in ivb_dict and ivb_name in tc_dict:
            obj_type = "CDV"
        else:
            print_error(f"For Signal {sig_name}, IXL APZ is defined containing {ivb_name}. "
                        f"But this object does not exist in the DC_SYS (not inside IVB sheet, not inside CDV sheet).")
            continue
        if obj_type == "IVB":
            list_points.extend(list(get_dc_sys_zip_values(ivb_dict[ivb_name],
                                                          DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X)))
        else:
            list_points.extend(list(get_dc_sys_zip_values(tc_dict[ivb_name],
                                                          DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)))

    list_points_without_double = list()
    for i, (entrance_seg, entrance_x) in enumerate(list_points):
        list_points_reduced = list_points[:i] + list_points[i+1:]
        if any(are_points_matching(entrance_seg, entrance_x, seg, x) for seg, x in list_points_reduced):
            continue
        list_points_without_double.append((entrance_seg, entrance_x))

    return list_points_without_double


def _get_approach_area_ivb(sig_name: str, apz_with_tc: bool = False) -> list[str]:
    if ixl_apz_definition_file():
        apz_ivb_list = get_approach_area_ivb_from_excel_file(sig_name)
        if apz_ivb_list is not None:
            return apz_ivb_list
    sig_dict = load_sheet(DCSYS.Sig)
    current_ivb = get_dc_sys_value(sig_dict[sig_name], DCSYS.Sig.IvbJoint.UpstreamIvb)
    if apz_with_tc:
        # IXL Approach Zone = first Track Circuit
        return [get_related_block_of_ivb(current_ivb)]
    return [current_ivb]  # default IXL Approach Zone = first IVB
