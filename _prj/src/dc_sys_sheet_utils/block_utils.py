#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_path_and_distances import is_seg_downstream, get_dist
from ..dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point


__all__ = ["get_list_len_block", "get_block_associated_to_sw",
           "find_upstream_n_downstream_limits", "does_path_exist_within_block"]


def get_list_len_block(block_value):
    list_dist = list()
    upstream_limits, downstream_limits = find_upstream_n_downstream_limits(block_value)
    for up_lim in upstream_limits:
        seg1, x1 = up_lim
        for down_lim in downstream_limits:
            seg2, x2 = down_lim
            d = get_dist(seg1, x1, seg2, x2)
            if d is not None:
                list_dist.append(d)
    return list_dist


def find_upstream_n_downstream_limits(block_value):
    upstream_limits = list()
    downstream_limits = list()
    for seg1, x1 in get_dc_sys_zip_values(block_value, DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X):
        test_direction = is_block_limit_upstream((seg1, x1), block_value)
        if test_direction is True:
            upstream_limits.append((seg1, x1))
        elif test_direction is False:
            downstream_limits.append((seg1, x1))
        else:
            print(f"unable to find if limit is upstream or downstream: "
                  f"{(seg1, x1)}")
    return upstream_limits, downstream_limits


def is_block_limit_upstream(start_lim: tuple[str, float], block_value):
    start_seg, start_x = start_lim
    other_limits = [(seg, x) for seg, x in get_dc_sys_zip_values(block_value,
                                                                 DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)
                    if (seg, x) != (start_seg, start_x)]

    for seg, x in other_limits:
        if seg == start_seg:  # two limits of the block are on the same segment
            return float(start_x) <= float(x)

    for seg, _ in other_limits:
        if is_seg_downstream(start_seg, seg, downstream=True):  # seg is downstream of start_seg
            if does_path_exist_within_block(start_seg, seg, block_value, downstream=True):
                return True  # start_seg is upstream of another limit within the block
        if is_seg_downstream(start_seg, seg, downstream=False):  # seg is upstream of start_seg
            if does_path_exist_within_block(start_seg, seg, block_value, downstream=False):
                return False  # start_seg is downstream of another limit within the block
    return None


def does_path_exist_within_block(seg1: str, seg2: str, block_value, downstream: bool = None):
    seg_limits = [seg for seg, x in get_dc_sys_zip_values(block_value,
                                                          DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)]

    if seg1 == seg2:
        return True
    if downstream is None:
        if is_seg_downstream(seg1, seg2, downstream=True):
            downstream = True
        elif is_seg_downstream(seg1, seg2, downstream=False):
            downstream = False
        else:
            return False

    def inner_recurs_seg(seg: str, end_seg: str, inner_downstream: bool):
        for next_seg in get_linked_segs(seg, inner_downstream):
            if next_seg == end_seg:
                return True
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            if next_seg not in seg_limits:
                return inner_recurs_seg(next_seg, end_seg, next_inner_downstream)
        return False

    return inner_recurs_seg(seg1, seg2, downstream)


def get_block_associated_to_sw(sw_value: dict) -> Optional[tuple[str, dict]]:
    """ Get the block associated to a switch. """
    point_seg, x = get_sw_pos(sw_value)
    list_blocks = get_zones_on_point(DCSYS.CDV, point_seg, x)
    if not list_blocks:
        print_error(f"Unable to find block associated to switch:\n{sw_value}")
        return None
    if len(list_blocks) > 1:
        print_error(f"Multiple blocks on switch:\n{sw_value}\n\t{list_blocks}")
        return None
    block_name = list_blocks[0]
    block_dict = load_sheet(DCSYS.CDV)
    return block_name, block_dict[block_name]
