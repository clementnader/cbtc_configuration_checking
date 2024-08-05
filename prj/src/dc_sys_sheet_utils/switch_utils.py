#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["give_sw_kp_pos", "get_heel_position", "get_switch_position_dict",
           "get_dc_sys_switch_points_dict", "get_corresponding_center_switch_point_track",
           "get_corresponding_heels_switch_point_track"]


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


def get_switch_position_dict():
    sw_dict = load_sheet(DCSYS.Aig)
    sw_pos_dict = dict()
    for sw, sw_info in sw_dict.items():
        track, kp = give_sw_kp_pos(sw_info)
        sw_pos_dict[sw] = {"track": track, "kp": kp}
    return sw_pos_dict


SW_INFO_DICT = {
    "left":  {"suffix": "_L", "attr": DCSYS.Aig.SegmentTg, "seg_start_if_sw_upstream": True},
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
            if sw_pos_name == "center":  # The center point name in the survey is sometimes the switch name only
                #                          without the "_C" suffix
                res_dict[sw_name_and_pos]["other_name"] = sw_name
    return res_dict


def get_corresponding_center_switch_point_track(heel_point_name: str
                                                ) -> tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    is_left = (heel_point_name.endswith("_L") or heel_point_name.endswith("_G"))
    is_right = (heel_point_name.endswith("_R") or heel_point_name.endswith("_D"))
    if not is_left and not is_right:
        return None, None, None, None

    sw_dict = {sw_name.upper(): sw_value for sw_name, sw_value in load_sheet(DCSYS.Aig).items()}
    seg_dict = load_sheet(DCSYS.Seg)

    sw_name = (heel_point_name.removesuffix("_L").removesuffix("_G") if is_left
               else heel_point_name.removesuffix("_R").removesuffix("_D"))
    if sw_name not in sw_dict:
        return None, None, None, None
    point_seg = get_dc_sys_value(sw_dict[sw_name], SW_INFO_DICT["center"]["attr"])
    track = get_dc_sys_value(seg_dict[point_seg], DCSYS.Seg.Voie)
    return sw_name + SW_INFO_DICT["center"]["suffix"], sw_name, track, "left" if is_left else "right"


def get_corresponding_heels_switch_point_track(switch_point_name: str
                                               ) -> tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    is_left = (switch_point_name.endswith("_L") or switch_point_name.endswith("_G"))
    is_right = (switch_point_name.endswith("_R") or switch_point_name.endswith("_D"))
    is_center = not is_left and not is_right
    if not is_center:
        return None, None, None, None

    sw_dict = {sw_name.upper(): sw_value for sw_name, sw_value in load_sheet(DCSYS.Aig).items()}
    seg_dict = load_sheet(DCSYS.Seg)

    sw_name = switch_point_name.removesuffix(SW_INFO_DICT["center"]["suffix"])
    if sw_name not in sw_dict:
        return None, None, None, None

    center_seg = get_dc_sys_value(sw_dict[sw_name], SW_INFO_DICT["center"]["attr"])
    left_seg = get_dc_sys_value(sw_dict[sw_name], SW_INFO_DICT["left"]["attr"])
    right_seg = get_dc_sys_value(sw_dict[sw_name], SW_INFO_DICT["right"]["attr"])
    center_track = get_dc_sys_value(seg_dict[center_seg], DCSYS.Seg.Voie)
    left_track = get_dc_sys_value(seg_dict[left_seg], DCSYS.Seg.Voie)
    right_track = get_dc_sys_value(seg_dict[right_seg], DCSYS.Seg.Voie)

    # left and right segments cannot be on the same track
    if left_track == center_track:
        return sw_name + SW_INFO_DICT["left"]["suffix"], sw_name + "_G", left_track, "left"
    if right_track == center_track:
        return sw_name + SW_INFO_DICT["right"]["suffix"], sw_name + "_D", right_track, "right"
    return None, None, None, None
