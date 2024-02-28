#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from .joint_utils import *
from .common_utils import *


# Block_Joint
def check_joint(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, float]],
                block_def_dict: Optional[dict[str, dict[tuple[str, float], str]]],
                buffer_survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheet == DCSYS.CDV
    assert res_sheet_name == "Block_Joint"

    joints_dict = get_joints_dict(block_def_dict)
    list_used_obj_names = list()
    res_dict = dict()
    for joint, obj_val in joints_dict.items():
        tc1, tc2, joint_track = joint
        limit_position, block_def_limit_name = obj_val
        original_dc_sys_track, dc_sys_kp = limit_position
        end_of_track_suffix = joint_track.removeprefix(original_dc_sys_track)
        # end_of_track_suffix is not null if a single block has two end-of-track limits on the same track
        dc_sys_track = original_dc_sys_track.upper()

        obj_name, survey_name, use_buffer = get_joint_name_in_survey(tc1, tc2, dc_sys_track, survey_info,
                                                                     limit_position, end_of_track_suffix,
                                                                     block_def_limit_name, buffer_survey_info)
        obj_name = get_display_name(obj_name, tc1, tc2, dc_sys_track, joints_dict)
        if use_buffer:
            survey_obj_info = buffer_survey_info.get(survey_name)
        else:
            survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                original_dc_sys_track, dc_sys_kp)
        res_dict[(obj_name, dc_sys_track)]["block_def_limit_name"] = block_def_limit_name

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict


def get_display_name(obj_name: str, tc1: str, tc2: Optional[str], track: str,
                     joints_dict: dict[tuple[str, Optional[str], str], tuple[tuple[str, float], str]]) -> str:
    if tc2 is not None:
        same_name_joints = [(block1, block2) for (block1, block2, _) in joints_dict
                            if (block1, block2) == (tc1, tc2)]
        if len(same_name_joints) < 2:
            return obj_name
        # There are multiple joints with this name, we precise in the name the track to get the unicity
        return obj_name + f"__on_{track}"

    else:  # tc2 is None
        same_name_joints = [(block1, block2) for (block1, block2, _) in joints_dict
                            if (block1, block2) == (tc1, tc2)]
        if len(same_name_joints) < 2:
            return obj_name
        if not obj_name.endswith("__end_of_track"):
            return obj_name
        # There are multiple joints with this name, we precise in the name the track to get the unicity
        return obj_name.removesuffix("_track") + f"_{track}"  # joint is already called __end_of_track
