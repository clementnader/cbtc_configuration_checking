#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import DCSYS
from .get_joints_dict import get_joints_dict


# BlockJoint
def check_joints(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheet == DCSYS.CDV
    assert res_sheet_name == "BlockJoint"

    joints_dict = get_joints_dict()
    res_dict = dict()
    for joint_name, joint_val in joints_dict.items():
        other_name = joint_val["other_name"]
        if other_name in survey_info:
            joint_name = other_name
        survey_obj_info = survey_info.get(joint_name)
        survey_object_comment = survey_obj_info["obj_comment"] if survey_obj_info is not None else None
        survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
        survey_track_comment = survey_obj_info["track_comment"] if survey_obj_info is not None else None
        surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
        surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
        design_kp = survey_obj_info["design_kp"] if survey_obj_info is not None else None
        design_kp_comment = survey_obj_info["design_kp_comment"] if survey_obj_info is not None else None

        track, dc_sys_kp = joint_val["position"]
        res_dict[joint_name] = {"track": track, "dc_sys_kp": dc_sys_kp}
        res_dict[joint_name].update({"survey_track": survey_track, "surveyed_kp": surveyed_kp, "design_kp": design_kp})
        res_dict[joint_name].update({"survey_object_comment": survey_object_comment,
                                     "survey_track_comment": survey_track_comment,
                                     "surveyed_kp_comment": surveyed_kp_comment,
                                     "design_kp_comment": design_kp_comment})

    res_dict.update(_add_extra_info_from_survey(joints_dict, survey_info))
    return res_dict


def _add_extra_info_from_survey(joints_dict: dict[str, dict[str, str]], survey_info: dict[str, dict[str]]):
    extra_dict = dict()
    for joint_name, joint_val in survey_info.items():
        if _is_joint_in_joints_dict(joint_name, joints_dict):
            continue
        extra_dict[joint_name] = {"track": None, "dc_sys_kp": None}
        extra_dict[joint_name].update({"survey_track": joint_val["track"], "surveyed_kp": joint_val["surveyed_kp"],
                                       "design_kp": joint_val["design_kp"]})
        extra_dict[joint_name].update({"survey_object_comment": joint_val["obj_comment"],
                                       "survey_track_comment": joint_val["track_comment"],
                                       "surveyed_kp_comment": joint_val["surveyed_kp_comment"],
                                       "design_kp_comment": joint_val["design_kp_comment"]})
    return extra_dict


def _is_joint_in_joints_dict(joint_name, joints_dict):
    for key, val in joints_dict.items():
        other_name = val["other_name"]
        if joint_name == key or joint_name == other_name:
            return True
    return False
