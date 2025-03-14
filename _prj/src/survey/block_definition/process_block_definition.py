#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


__all__ = ["associate_block_def_to_dc_sys"]


def associate_block_def_to_dc_sys(block_def_dict: Optional[dict[str, list[tuple[tuple[str, float], str]]]]
                                  ) -> Optional[dict[str, dict[tuple[str, float], str]]]:
    if block_def_dict is None:
        return None

    res_block_def_dict = dict()
    for block_name, list_info in block_def_dict.items():
        track_list = list()
        for i, info in enumerate(list_info):
            (seg, x), limit_name = info
            if seg is None or x is None:
                track, kp = None, None
            else:
                try:
                    track, kp = from_seg_offset_to_kp(seg, x)
                except KeyError:
                    track, kp = None, None
            track_list.append(((seg, x, track, kp), limit_name))
        res_block_def_dict[block_name] = track_list

    return _find_correspondence_in_dc_sys(res_block_def_dict)


def _find_correspondence_in_dc_sys(block_def_dict: dict[str, list[tuple[tuple[str, float, str, float], str]]]
                                   ) -> dict[str, dict[tuple[str, float], str]]:
    res_block_def_dict = dict()
    for block_name, block_def_limits_info in block_def_dict.items():
        if not block_def_limits_info:
            continue

        block_dict = load_sheet(DCSYS.CDV)
        if block_name not in block_dict:
            print_warning(f"Block {block_name} from Block Def. file is not in DC_SYS.")
            continue

        block_value = block_dict[block_name]
        dc_sys_limits_track_kp = list(get_dc_sys_zip_values(block_value, DCSYS.CDV.Extremite.Voie,
                                                            DCSYS.CDV.Extremite.Pk))

        res_block_def_dict[block_name] = _get_association_block_limits_dict(block_name, block_def_limits_info,
                                                                            dc_sys_limits_track_kp)

    return res_block_def_dict


def _get_association_block_limits_dict(block_name: str,
                                       block_def_limits_info: list[tuple[tuple[str, float, str, float], str]],
                                       dc_sys_limits_track_kp: list[tuple[str, float]]):

    block_limits_dict = dict()
    if all(limit_info[0][2] is None for limit_info in block_def_limits_info):  # if all tracks are None
        for (dc_sys_track, dc_sys_kp), (_, limit_name) in zip(dc_sys_limits_track_kp, block_def_limits_info):
            block_limits_dict[(dc_sys_track, dc_sys_kp)] = limit_name
        return block_limits_dict

    dc_sys_limit_tracks = set([track for (track, _) in dc_sys_limits_track_kp])
    for test_track in dc_sys_limit_tracks:
        dc_sys_limits_on_track = [(track, dc_sys_kp) for (track, dc_sys_kp) in dc_sys_limits_track_kp
                                  if track.upper() == test_track.upper()]
        block_def_limits_info_on_track = [((seg, x, track, dc_sys_kp), limit_name)
                                          for ((seg, x, track, dc_sys_kp), limit_name) in block_def_limits_info
                                          if track is not None and track.upper() == test_track.upper()]
        if len(dc_sys_limits_on_track) != len(block_def_limits_info_on_track):
            print_warning(f"In Block Def. file, for block {block_name}, there are not the same number of limits "
                          f"on track {test_track} as in the DC_SYS:\n"
                          f"{Color.default}{dc_sys_limits_on_track = }\n"
                          f"{block_def_limits_info_on_track = }\n"
                          f"{block_def_limits_info = }{Color.reset}")
            continue
        if len(dc_sys_limits_on_track) == 1:  # only one limit on this track
            _, dc_sys_kp = dc_sys_limits_on_track[0]
            block_limits_dict[(test_track, dc_sys_kp)] = block_def_limits_info_on_track[0][1]

        elif len(dc_sys_limits_on_track) == 2:  # two limits on this track
            # (there cannot be more than two limits on a same track)
            _, dc_sys_kp1 = dc_sys_limits_on_track[0]
            _, dc_sys_kp2 = dc_sys_limits_on_track[1]

            first_value, second_value = _find_correct_order_two_limits_on_track(dc_sys_kp1, dc_sys_kp2,
                                                                                block_def_limits_info_on_track)
            block_limits_dict[(test_track, dc_sys_kp1)] = first_value
            block_limits_dict[(test_track, dc_sys_kp2)] = second_value

    return block_limits_dict


def _find_correct_order_two_limits_on_track(dc_sys_kp1: float, dc_sys_kp2: float,
                                            block_def_limits_info_on_track: list[
                                                tuple[tuple[str, float, str, float], str]]
                                            ) -> tuple[str, str]:

    # Find the closest combination
    block_def_seg1, block_def_x1, _, _ = block_def_limits_info_on_track[0][0]
    block_def_seg2, block_def_x2, _, _ = block_def_limits_info_on_track[1][0]

    if block_def_seg1 != block_def_seg2:  # we don't need the values but only the polarity,
        # the segment lengths can have changed and then the translation from seg, x to track, kp
        # can be wrong if offsets are larger than segment lengths, we set the offsets at zero to only
        # test the polarity of the segments
        _, seg1_kp = from_seg_offset_to_kp(block_def_seg1, 0)
        _, seg2_kp = from_seg_offset_to_kp(block_def_seg2, 0)
        same_polarity = (dc_sys_kp1 >= dc_sys_kp2) == (seg1_kp >= seg2_kp)
    else:  # on the same segment, there is no problem of wrong kp order
        _, seg1_kp = from_seg_offset_to_kp(block_def_seg1, block_def_x1)
        _, seg2_kp = from_seg_offset_to_kp(block_def_seg2, block_def_x2)
        same_polarity = (dc_sys_kp1 >= dc_sys_kp2) == (seg1_kp >= seg2_kp)

    if same_polarity:  # normal order
        first_value = block_def_limits_info_on_track[0][1]
        second_value = block_def_limits_info_on_track[1][1]
    else:  # reverse order
        first_value = block_def_limits_info_on_track[1][1]
        second_value = block_def_limits_info_on_track[0][1]

    return first_value, second_value
