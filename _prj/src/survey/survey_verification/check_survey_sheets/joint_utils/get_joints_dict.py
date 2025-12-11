#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .....cctool_oo_schema import *
from .....dc_sys import *
from .joints_utils import *


__all__ = ["get_joints_dict"]


def get_joints_dict(block_def_dict: Optional[dict[str, dict[tuple[str, float], str]]]
                    ) -> dict[tuple[str, Optional[str], str], tuple[tuple[str, float], str]]:
    joints_dict = dict()
    block_dict = load_sheet(DCSYS.CDV)
    for block_name, block_value in block_dict.items():

        matching_blocks = find_associated_blocks(block_name, block_value, DCSYS.CDV,
                                                 DCSYS.CDV.Extremite.Voie, DCSYS.CDV.Extremite.Pk)
        for limit_position, matching_block_name in matching_blocks.items():
            if block_def_dict is not None and block_name in block_def_dict:
                block_def_limit_name = block_def_dict[block_name].get(limit_position)
            else:
                block_def_limit_name = None

            track = limit_position[0]
            joint = (block_name, matching_block_name, track)
            joint2 = (matching_block_name, block_name, track) if matching_block_name is not None else None

            if joint not in joints_dict and (joint2 is None or joint2 not in joints_dict):
                joints_dict[joint] = (limit_position, block_def_limit_name)
                continue

            if joint2 is not None:
                if joint in joints_dict and limit_position != joints_dict[joint][0]:
                    print_error(f"Found another joint between the same blocks and on the same track: {joint}\n"
                                f"but at a different position {joints_dict[joint][0]} vs {limit_position}.")
                if joint2 in joints_dict and limit_position != joints_dict[joint2][0]:
                    print_error(f"Found another joint between the same blocks and on the same track: {joint2}\n"
                                f"but at a different position {joints_dict[joint2][0]} vs {limit_position}.")
            else:
                if joint in joints_dict and limit_position != joints_dict[joint]:
                    # A block with two end-of-track limits on the same track
                    joints_dict[(block_name, matching_block_name, track + "__1")] = joints_dict[joint]
                    del joints_dict[joint]
                    joints_dict[(block_name, matching_block_name, track + "__2")] = (limit_position,
                                                                                     block_def_limit_name)

    return joints_dict
