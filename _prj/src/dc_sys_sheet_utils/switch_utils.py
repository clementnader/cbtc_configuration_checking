#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["give_switch_kp_position", "get_heel_position", "get_dc_sys_switch_points_dict",
           "get_switch_on_path"]


def get_heel_position(point_seg: str, heel: str) -> tuple[Optional[str], str]:
    sw_dict = load_sheet(DCSYS.Aig)
    for sw_name, sw_value in sw_dict.items():
        sw_point_seg = get_dc_sys_value(sw_value, DCSYS.Aig.SegmentPointe)
        sw_right_heel = get_dc_sys_value(sw_value, DCSYS.Aig.SegmentTd)
        sw_left_heel = get_dc_sys_value(sw_value, DCSYS.Aig.SegmentTg)
        if point_seg == sw_point_seg:
            if heel == sw_right_heel:
                return sw_name, Switch_Position.DROITE
            if heel == sw_left_heel:
                return sw_name, Switch_Position.GAUCHE
    return None, ""


def give_switch_kp_position(sw_name: str):
    """Returns the position of the switch with the track and the KP value. """
    seg_dict = load_sheet(DCSYS.Seg)
    point_seg = get_dc_sys_value(sw_name, DCSYS.Aig.SegmentPointe)
    upstream = is_switch_point_upstream_heels(sw_name)
    track = get_dc_sys_value(seg_dict[point_seg], DCSYS.Seg.Voie)
    kp_attr = DCSYS.Seg.Fin if upstream else DCSYS.Seg.Origine
    kp = float(get_dc_sys_value(seg_dict[point_seg], kp_attr))
    return track, kp


SWITCH_INFO_DICT = {
    "left": {"suffix": "_L", "attr": DCSYS.Aig.SegmentTg, "seg_start_if_sw_upstream": True},
    "right": {"suffix": "_R", "attr": DCSYS.Aig.SegmentTd, "seg_start_if_sw_upstream": True},
    "center": {"suffix": "_C", "attr": DCSYS.Aig.SegmentPointe, "seg_start_if_sw_upstream": False}
}

def get_dc_sys_switch_points_dict() -> dict[str, dict[str, Union[str, float]]]:
    """Returns the switches position dictionary with the 3 different positions SWP_L, SWP_R and SWP_C for each switch
    from the DC_SYS."""
    res_dict = dict()
    sw_dict = load_sheet(DCSYS.Aig)
    seg_dict = load_sheet(DCSYS.Seg)
    for sw_name in sw_dict:
        upstream = is_switch_point_upstream_heels(sw_name)
        for sw_pos_name, pos_val in SWITCH_INFO_DICT.items():
            sw_name_and_pos = sw_name + pos_val["suffix"]
            seg = get_dc_sys_value(sw_name, pos_val["attr"])
            track = get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Voie)
            kp_attr = DCSYS.Seg.Origine if upstream == pos_val["seg_start_if_sw_upstream"] else DCSYS.Seg.Fin
            kp = get_dc_sys_value(seg_dict[seg], kp_attr)
            res_dict[sw_name_and_pos] = {"track": track, "kp": kp}
    return res_dict


def get_switch_on_path(path: list[str]) -> list[tuple[str, str]]:
    list_sw = list()
    for seg, next_seg in zip(path[:-1], path[1:]):
        if is_segment_upstream_of_a_switch(seg) or is_segment_downstream_of_a_switch(seg):
            sw_name, sw_pos = get_heel_position(seg, next_seg)
            if sw_name is not None:
                list_sw.append((sw_name, sw_pos))
        if is_segment_upstream_of_a_switch(next_seg) or is_segment_downstream_of_a_switch(next_seg):
            sw_name, sw_pos = get_heel_position(next_seg, seg)
            if sw_name is not None:
                list_sw.append((sw_name, sw_pos))
    return list_sw
