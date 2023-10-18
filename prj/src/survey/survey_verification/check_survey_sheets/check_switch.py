#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *
from .common_utils import *


SW_INFO_DICT = {
    "left":  {"suffix": "_L", "attr": DCSYS.Aig.SegmentTg,     "seg_start_if_sw_upstream": True},
    "right": {"suffix": "_R", "attr": DCSYS.Aig.SegmentTd,     "seg_start_if_sw_upstream": True},
    "point": {"suffix": "_C", "attr": DCSYS.Aig.SegmentPointe, "seg_start_if_sw_upstream": False}
}


# Switch
def check_switch(dc_sys_sheet, res_sheet_name: str, survey_info: dict):
    assert dc_sys_sheet == DCSYS.Aig
    assert res_sheet_name == "Switch"

    obj_dict = _get_dc_sys_switch_dict()
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in obj_dict.items():
        track, dc_sys_kp = obj_val["track"], obj_val["dc_sys_kp"]

        other_name = obj_val.get("other_name")
        if other_name is not None and other_name in survey_info:
            survey_name = other_name.upper()
        else:
            survey_name = obj_name.upper()
        survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        obj_name = survey_obj_info["obj_name"] if survey_obj_info is not None else obj_name

        res_dict[obj_name] = add_info_to_survey(survey_obj_info, track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict


def _get_dc_sys_switch_dict():
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
            dc_sys_kp = get_dc_sys_value(seg_dict[seg], kp_attr)
            res_dict[sw_name_and_pos] = {"track": track, "dc_sys_kp": dc_sys_kp}
            if sw_pos_name == "point":  # For Copenhagen first survey, the switch point name is the switch name only
                #                          without the "_C" suffix
                res_dict[sw_name_and_pos]["other_name"] = sw_name
    return res_dict
