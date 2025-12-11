#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .....utils import *
from .....cctool_oo_schema import *
from ....survey_utils import clean_object_name
from .get_other_block_joint import *


__all__ = ["get_joint_possible_names"]


def get_joint_possible_names(tc1: str, tc2: Optional[str], limit_position: tuple[str, float]) -> list[str]:
    list_names = list()
    other_tc1, other_tc2 = get_other_corresponding_tc_joint_on_limit_of_track(tc1, tc2, limit_position)
    if "IVB" not in get_class_attributes_dict(DCSYS):
        ivb1, ivb2 = None, None
        other_ivb1, other_ivb2 = None, None
    else:
        ivb1, ivb2 = get_corresponding_ivb_joint(tc1, tc2, limit_position)
        if ivb1 is None:
            other_ivb1, other_ivb2 = None, None
        else:
            other_ivb1, other_ivb2 = get_other_corresponding_ivb_joint_on_limit_of_track(ivb1, ivb2, limit_position)

    for block1, block2 in [[other_ivb1, other_ivb2], [ivb1, ivb2], [other_tc1, other_tc2], [tc1, tc2]]:
        if block1 is None:
            continue
        if block2 is None:
            joint_name = ("JOI_" + block1.removeprefix("IVB_").removeprefix("TC_") + "__end_of_track")
            if joint_name not in list_names:
                list_names.append(joint_name)
        else:
            for func in [get_classic_joint_name, get_joint_name_one_merge, get_joint_name_not_merged]:
                joint_name1 = func(block1, block2)
                joint_name2 = func(block2, block1)
                list_names.extend([joint_name for joint_name in [joint_name1, joint_name2]
                                   if joint_name not in list_names])

    return list_names


def get_classic_joint_name(block_name: str, matching_block_name: str) -> str:
    return ("JOI_" + block_name.removeprefix("IVB_").removeprefix("TC_")
            + _get_joint_suffix_name(block_name, matching_block_name))


def get_joint_name_one_merge(block_name: str, matching_block_name: str) -> str:
    return ("JOI_" + block_name.removeprefix("IVB_").removeprefix("TC_")
            + _get_joint_suffix_name(block_name, matching_block_name, one_merge=True))


def get_joint_name_not_merged(block_name: str, matching_block_name: str) -> str:
    return ("JOI_" + block_name.removeprefix("IVB_").removeprefix("TC_") + "_"
            + matching_block_name.removeprefix("IVB_").removeprefix("TC_"))


def _get_joint_suffix_name(block1_name: str, block2_name: str, one_merge: bool = False) -> str:
    split_diff_start = -1
    split1 = block1_name.split("_")[1:]  # remove the TC_ or IVB_
    split2 = block2_name.split("_")[1:]  # remove the TC_ or IVB_
    max_nb_merge = min(len(split1), len(split2)) - 1
    if not split1 or not split2:
        # There is no underscore in block1_name or block2_name.
        return "_" + block2_name

    for i, (t1, t2) in enumerate(zip(split1, split2)):
        if t1 != t2:
            split_diff_start = i
            break

    if split_diff_start == -1:  # split1 is included inside split2, or the other way around
        split_diff_start = max_nb_merge

    elif one_merge and split_diff_start > 1 and split_diff_start == max_nb_merge:  # remove the last merge
        return "_" + "_".join(split2[split_diff_start-1:])

    return "_" + "_".join(split2[split_diff_start:])
