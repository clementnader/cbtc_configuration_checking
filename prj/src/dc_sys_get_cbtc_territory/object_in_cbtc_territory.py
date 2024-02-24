#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_common_utils import *
from .cbtc_territory_utils import *


__all__ = ["get_objects_in_cbtc_ter"]


def get_objects_in_cbtc_ter(obj_type) -> dict[str, dict]:
    obj_type = get_sh_name(obj_type)

    if "IXL_Overlap" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.IXL_Overlap):
        return _get_overlap_in_cbtc_ter()
    elif "StaticTag_Group" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.StaticTag_Group):
        return _get_tag_gr_in_cbtc_ter()
    elif "Voie" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.Voie):
        return _get_track_in_cbtc_ter()
    elif "Traffic_Stop" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.Traffic_Stop):
        return _get_traffic_stop_in_cbtc_ter()
    else:
        obj_dict = load_sheet(obj_type)

        within_cbtc_object_dict = dict()
        for obj_name, obj_value in obj_dict.items():
            position = get_obj_position(obj_type, obj_name)
            if position is None:
                continue
            if isinstance(position, tuple):  # single point object
                if _test_for_single_point(position, obj_type, obj_name):
                    within_cbtc_object_dict[obj_name] = obj_value
            else:  # zone object
                if _test_for_zone(position, obj_type, obj_name):
                    within_cbtc_object_dict[obj_name] = obj_value
        return within_cbtc_object_dict


def _test_for_single_point(position: tuple[str, float], obj_type: str, obj_name: str) -> bool:
    seg = position[0]
    x = position[1]

    if is_point_in_cbtc_ter(seg, x) is True:
        test = True
    elif is_point_in_cbtc_ter(seg, x) is None:
        print_log(f"{obj_type} {obj_name} is on a limit of CBTC Territory. "
                  f"It is still taken into account.")
        test = True
    else:
        test = False
    return test


def _test_for_zone(position: list[tuple[str, float]], obj_type: str, obj_name: str) -> bool:
    limits_in_cbtc_ter = list()
    for limit_pos in position:
        seg = limit_pos[0]
        x = limit_pos[1]
        limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))

    if (any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter)
            and all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter)):
        test = True
    elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
        print_log(f"{obj_type} {obj_name} is both inside and outside CBTC Territory. "
                  f"It is still taken into account.")
        test = True
    else:
        test = False
    return test


def _get_overlap_in_cbtc_ter():
    ovl_dict = load_sheet(DCSYS.IXL_Overlap)
    sig_in_cbtc = get_objects_in_cbtc_ter(DCSYS.Sig)

    within_cbtc_ovl_dict = dict()
    for ovl_name, ovl_value in ovl_dict.items():
        related_sig = get_dc_sys_value(ovl_value, DCSYS.IXL_Overlap.DestinationSignal)
        if related_sig in sig_in_cbtc:
            within_cbtc_ovl_dict[ovl_name] = ovl_value
    return within_cbtc_ovl_dict


def _get_tag_gr_in_cbtc_ter():
    within_cbtc_tag_dict = get_objects_in_cbtc_ter(DCSYS.Bal)
    tag_gr_dict = load_sheet(DCSYS.StaticTag_Group)
    within_cbtc_tag_gr_dict = dict()
    for tag_gr_name, tag_gr_value in tag_gr_dict.items():
        tags = [tag for tag in get_dc_sys_value(tag_gr_value, DCSYS.StaticTag_Group.TagList.Tag) if tag is not None]
        if all(tag in within_cbtc_tag_dict for tag in tags):
            within_cbtc_tag_gr_dict[tag_gr_name] = tag_gr_value
        elif any(tag in within_cbtc_tag_dict for tag in tags):
            print_warning(f"Tag group {tag_gr_name} possesses tags within and without CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_tag_gr_dict[tag_gr_name] = tag_gr_value
    return within_cbtc_tag_gr_dict


def _get_track_in_cbtc_ter():
    seg_dict = load_sheet(DCSYS.Seg)
    list_tracks = list()
    for seg in get_all_segs_in_cbtc_ter():
        track = get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Voie)
        if track not in list_tracks:
            list_tracks.append(track)
    track_dict = load_sheet(DCSYS.Voie)
    within_cbtc_track_dict = {key: track_dict[key] for key in sorted(list_tracks)}
    return within_cbtc_track_dict


def _get_traffic_stop_in_cbtc_ter():
    stop_dict = load_sheet(DCSYS.Traffic_Stop)
    platforms_in_cbtc = get_objects_in_cbtc_ter(DCSYS.Voie)

    within_cbtc_stop_dict = dict()
    for stop_name, stop_value in stop_dict.items():
        rel_plts_in_cbtc_ter = list()
        for rel_plt_name in get_dc_sys_value(stop_value, DCSYS.Traffic_Stop.PlatformList.Name):
            rel_plts_in_cbtc_ter.append(rel_plt_name in platforms_in_cbtc)
        if any(rel_plt_in_cbtc_ter is True for rel_plt_in_cbtc_ter in rel_plts_in_cbtc_ter):
            within_cbtc_stop_dict[stop_name] = stop_value
    return within_cbtc_stop_dict
