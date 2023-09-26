#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *


SW_INFO_DICT = {
    "left":  {"suffix": "_L", "attr": DCSYS.Aig.SegmentTg,     "seg_start_if_sw_upstream": True},
    "right": {"suffix": "_R", "attr": DCSYS.Aig.SegmentTd,     "seg_start_if_sw_upstream": True},
    "point": {"suffix": "_C", "attr": DCSYS.Aig.SegmentPointe, "seg_start_if_sw_upstream": False}
}


# Switch
def check_switch(dc_sys_sheet, res_sheet_name: str, survey_info: dict):
    assert dc_sys_sheet == DCSYS.Aig
    assert res_sheet_name == "Switch"

    sw_dict = _get_dc_sys_sw_dict()
    res_dict = dict()
    for sw_name, sw_val in sw_dict.items():
        survey_obj_info = survey_info.get(sw_name)
        survey_object_comment = survey_obj_info["obj_comment"] if survey_obj_info is not None else None
        survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
        survey_track_comment = survey_obj_info["track_comment"] if survey_obj_info is not None else None
        surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
        surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
        design_kp = survey_obj_info["design_kp"] if survey_obj_info is not None else None
        design_kp_comment = survey_obj_info["design_kp_comment"] if survey_obj_info is not None else None
        res_dict[sw_name] = {"track": sw_val[0], "dc_sys_kp": sw_val[1]}
        res_dict[sw_name].update({"survey_track": survey_track, "surveyed_kp": surveyed_kp, "design_kp": design_kp})
        res_dict[sw_name].update({"survey_object_comment": survey_object_comment,
                                  "survey_track_comment": survey_track_comment,
                                  "surveyed_kp_comment": surveyed_kp_comment,
                                  "design_kp_comment": design_kp_comment})

    res_dict.update(_add_extra_info_from_survey(list(sw_dict.keys()), survey_info))
    return res_dict


def _get_dc_sys_sw_dict():
    res_dict = dict()
    sw_dict = load_sheet(DCSYS.Aig)
    seg_dict = load_sheet(DCSYS.Seg)
    for sw_name, sw_val in sw_dict.items():
        upstream = is_sw_point_seg_upstream(sw_val)
        for pos_val in SW_INFO_DICT.values():
            sw_name_and_pos = sw_name + pos_val["suffix"]
            seg = get_dc_sys_value(sw_val, pos_val["attr"])
            track = get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Voie)
            kp_attr = DCSYS.Seg.Origine if upstream == pos_val["seg_start_if_sw_upstream"] else DCSYS.Seg.Fin
            dc_sys_kp = get_dc_sys_value(seg_dict[seg], kp_attr)
            res_dict[sw_name_and_pos] = (track, dc_sys_kp)
    return res_dict


def _add_extra_info_from_survey(list_sw_names: list[str], survey_info: dict[str, dict[str]]):
    extra_dict = dict()
    for sw_name, sw_val in survey_info.items():
        if sw_name in list_sw_names:
            continue
        extra_dict[sw_name] = {"track": None, "dc_sys_kp": None}
        extra_dict[sw_name].update({"survey_track": sw_val["track"], "surveyed_kp": sw_val["surveyed_kp"],
                                    "design_kp": sw_val["design_kp"]})
        extra_dict[sw_name].update({"survey_object_comment": sw_val["obj_comment"],
                                    "survey_track_comment": sw_val["track_comment"],
                                    "surveyed_kp_comment": sw_val["surveyed_kp_comment"],
                                    "design_kp_comment": sw_val["design_kp_comment"]})
    return extra_dict
