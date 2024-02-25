#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


__all__ = ["add_tracks_to_block_def"]


def add_tracks_to_block_def(block_def_dict: Optional[dict[str, list[tuple[tuple[str, float], str]]]]
                            ) -> Optional[dict[str, dict[tuple[str, float], str]]]:
    if block_def_dict is None:
        return None

    res_block_def_dict = dict()
    for block_name, list_info in block_def_dict.items():
        track_list = list()
        for info in list_info:
            (seg, x), limit_name = info
            track, kp = from_seg_offset_to_kp(seg, x)
            track_list.append(((track, kp), limit_name))
        res_block_def_dict[block_name] = track_list
    return find_correspondence_in_dc_sys(res_block_def_dict)


def find_correspondence_in_dc_sys(block_def_dict: dict[str, list[tuple[tuple[str, float], str]]]
                                  ) -> dict[str, dict[tuple[str, float], str]]:
    res_block_def_dict = dict()
    for block_name, block_def_limits_info in block_def_dict.items():
        block_dict = load_sheet(DCSYS.CDV)
        if block_name not in block_dict:
            print_warning(f"Block {block_name} from Block Def. file is not in DC_SYS.")
            continue
        block_limits_dict = dict()
        dc_sys_limits_track_kp = list(get_dc_sys_zip_values(block_dict[block_name], DCSYS.CDV.Extremite.Voie,
                                                            DCSYS.CDV.Extremite.Pk))
        if len(block_def_limits_info) != len(dc_sys_limits_track_kp):
            print_error(f"In Block Def. file, for block {block_name}, there are not the same number of limits as in "
                        f"the DC_SYS:\n"
                        f"{block_def_limits_info = }\n"
                        f"{dc_sys_limits_track_kp = }")
            continue

        dc_sys_limit_tracks = set([track for (track, _) in dc_sys_limits_track_kp])
        for test_track in dc_sys_limit_tracks:
            dc_sys_limits_on_track = [(track, dc_sys_kp) for (track, dc_sys_kp) in dc_sys_limits_track_kp
                                      if track.upper() == test_track.upper()]
            block_def_limits_info_on_track = [((track, dc_sys_kp), limit_name) for ((track, dc_sys_kp), limit_name)
                                              in block_def_limits_info if track.upper() == test_track.upper()]
            if len(dc_sys_limits_on_track) != len(block_def_limits_info_on_track):
                print_error(f"In Block Def. file, for block {block_name}, there are not the same number of limits "
                            f"on track {test_track} as in the DC_SYS:\n"
                            f"{block_def_limits_info_on_track = }\n"
                            f"{dc_sys_limits_on_track = }")
                continue
            if len(dc_sys_limits_on_track) == 1:  # only one limit on this track
                _, dc_sys_kp = dc_sys_limits_on_track[0]
                block_limits_dict[(test_track, dc_sys_kp)] = block_def_limits_info_on_track[0][1]

            elif len(dc_sys_limits_on_track) == 2:  # two limits on this track
                # (there cannot be more than two limits on a same track)

                # Find the closest combination
                _, dc_sys_kp1 = dc_sys_limits_on_track[0]
                _, dc_sys_kp2 = dc_sys_limits_on_track[1]
                _, block_def_kp1 = block_def_limits_info_on_track[0][0]
                _, block_def_kp2 = block_def_limits_info_on_track[1][0]

                sum_delta_normal_order = abs(dc_sys_kp1 - block_def_kp1) + abs(dc_sys_kp2 - block_def_kp2)
                sum_delta_reverse_order = abs(dc_sys_kp2 - block_def_kp1) + abs(dc_sys_kp1 - block_def_kp2)

                if sum_delta_normal_order < sum_delta_reverse_order:  # normal order is the closest
                    block_limits_dict[(test_track, dc_sys_kp1)] = block_def_limits_info_on_track[0][1]
                    block_limits_dict[(test_track, dc_sys_kp2)] = block_def_limits_info_on_track[1][1]
                else:  # reverse order is the closest
                    block_limits_dict[(test_track, dc_sys_kp1)] = block_def_limits_info_on_track[1][1]
                    block_limits_dict[(test_track, dc_sys_kp2)] = block_def_limits_info_on_track[0][1]

        res_block_def_dict[block_name] = block_limits_dict

    return res_block_def_dict
