#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from .joint_utils import *
from .common_utils import *


# Block_Joint
def check_joint(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, float]],
                block_def_dict: Optional[dict[str, list[str]]], buffer_survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheet == DCSYS.CDV
    assert res_sheet_name == "Block_Joint"

    # TODO use block_def_dict

    joints_dict = get_joints_dict()
    list_used_obj_names = list()
    res_dict = dict()
    for joint, obj_val in joints_dict.items():
        tc1, tc2, joint_track = joint
        dc_sys_track, dc_sys_kp = obj_val
        end_of_track_suffix = joint_track.removeprefix(dc_sys_track)
        # end_of_track_suffix is not null if a single block has two end-of-track limits on the same track
        dc_sys_track = dc_sys_track.upper()

        obj_name, survey_name = get_joint_name_in_survey(tc1, tc2, dc_sys_track, survey_info, joint, joints_dict,
                                                         end_of_track_suffix)
        survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict
