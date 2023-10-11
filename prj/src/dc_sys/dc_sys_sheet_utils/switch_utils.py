#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_common_utils import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


__all__ = ["get_switches_in_cbtc_ter", "is_sw_point_seg_upstream", "give_sw_pos", "give_sw_kp_pos", "get_heel_position",
           "get_switch_position_dict", "get_point_seg"]


def get_switches_in_cbtc_ter():
    sw_dict = load_sheet(DCSYS.Aig)
    within_cbtc_sw_dict = dict()
    for sw_name, sw_value in sw_dict.items():
        seg, x = give_sw_pos(sw_value)
        if is_point_in_cbtc_ter(seg, x) is not False:
            within_cbtc_sw_dict[sw_name] = sw_value
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Switch {sw_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
    return within_cbtc_sw_dict


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
