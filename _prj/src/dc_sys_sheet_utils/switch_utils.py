#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["give_sw_kp_pos", "get_heel_position", "get_dc_sys_switch_points_dict"]


def get_heel_position(point_seg, heel) -> tuple[Optional[str], str]:
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


def give_sw_kp_pos(sw):
    """Returns the position of the switch with the track and the KP value. """
    seg_dict = load_sheet(DCSYS.Seg)
    point_seg = get_point_seg(sw)
    upstream = is_sw_point_seg_upstream(sw)
    track = get_dc_sys_value(seg_dict[point_seg], DCSYS.Seg.Voie)
    kp_attr = DCSYS.Seg.Fin if upstream else DCSYS.Seg.Origine
    kp = float(get_dc_sys_value(seg_dict[point_seg], kp_attr))
    return track, kp


SW_INFO_DICT = {
    "left": {"suffix": "_L", "attr": DCSYS.Aig.SegmentTg, "seg_start_if_sw_upstream": True},
    "right": {"suffix": "_R", "attr": DCSYS.Aig.SegmentTd, "seg_start_if_sw_upstream": True},
    "center": {"suffix": "_C", "attr": DCSYS.Aig.SegmentPointe, "seg_start_if_sw_upstream": False}
}


def get_dc_sys_switch_points_dict():
    res_dict = dict()
    sw_dict = load_sheet(DCSYS.Aig)
    seg_dict = load_sheet(DCSYS.Seg)
    for sw_name, sw_val in sw_dict.items():
        upstream = is_sw_point_seg_upstream(sw_val)
        for sw_pos_name, pos_val in SW_INFO_DICT.items():
            sw_name_and_pos = sw_name + pos_val["suffix"]
            seg = get_dc_sys_value(sw_val, pos_val["attr"])
            track = get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Voie)
            kp_attr = DCSYS.Seg.Origine if upstream == pos_val["seg_start_if_sw_upstream"] else DCSYS.Seg.Fin
            kp = get_dc_sys_value(seg_dict[seg], kp_attr)
            res_dict[sw_name_and_pos] = {"track": track, "kp": kp}
    return res_dict
