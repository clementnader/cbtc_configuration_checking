#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .cbtc_territory_utils import is_point_in_cbtc_ter
from .dist_utils import get_dist, get_downstream_path, is_seg_downstream
from .segments_utils import *


__all__ = ["get_blocks_in_cbtc_ter", "get_list_len_block", "get_block_associated_to_sw",
           "find_upstream_n_downstream_limits", "does_path_exist_within_block"]


def get_blocks_in_cbtc_ter():
    block_dict = load_sheet(DCSYS.CDV)
    within_cbtc_block_dict = dict()
    for block, block_value in block_dict.items():
        limits_in_cbtc_ter = list()
        for seg, x in get_dc_sys_zip_values(block_value, DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter):
            within_cbtc_block_dict[block] = block_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"Block {block} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_block_dict[block] = block_value
    return within_cbtc_block_dict


def get_list_len_block(block):
    list_dist = list()
    upstream_limits, downstream_limits = find_upstream_n_downstream_limits(block)
    for up_lim in upstream_limits:
        seg1, x1 = up_lim
        for down_lim in downstream_limits:
            seg2, x2 = down_lim
            d = get_dist(seg1, x1, seg2, x2)
            if d is not None:
                list_dist.append(d)
    return list_dist


def find_upstream_n_downstream_limits(block):
    upstream_limits = list()
    downstream_limits = list()
    for seg1, x1 in get_dc_sys_zip_values(block, DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X):
        if is_block_limit_upstream((seg1, x1), block):
            upstream_limits.append((seg1, x1))
        else:
            downstream_limits.append((seg1, x1))
    return upstream_limits, downstream_limits


def is_block_limit_upstream(start_lim: tuple, block):
    start_seg, start_x = start_lim
    other_limits = [(seg, x) for seg, x in get_dc_sys_zip_values(block, DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)
                    if (seg, x) != (start_seg, start_x)]

    for lim in other_limits:
        seg, x = lim
        if seg == start_seg:  # two limits of the block are on the same segment
            return float(start_x) <= float(x)

    for lim in other_limits:
        seg, _ = lim
        if is_seg_downstream(start_seg, seg, downstream=True):  # seg is downstream of start_seg
            if does_path_exist_within_block(start_seg, seg, block, downstream=True):
                return True  # start_seg is upstream of another limit within the block
        if is_seg_downstream(start_seg, seg, downstream=False):  # seg is upstream of start_seg
            if does_path_exist_within_block(start_seg, seg, block, downstream=False):
                return False  # start_seg is downstream of another limit within the block
    return None


def does_path_exist_within_block(seg1, seg2, block, downstream: bool = None):
    seg_limits = [seg for seg, x in get_dc_sys_zip_values(block, DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)]

    if seg1 == seg2:
        return True
    if downstream is None:
        if is_seg_downstream(seg1, seg2, downstream=True):
            downstream = True
        elif is_seg_downstream(seg1, seg2, downstream=False):
            downstream = False
        else:
            return False

    def inner_recurs_seg(seg, end_seg, inner_downstream):
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


def get_segs_in_blocks(block):
    """ Return the list of segments in a block. """
    set_segs = set()
    upstream_limits, downstream_limits = find_upstream_n_downstream_limits(block)
    for up_lim in upstream_limits:
        up_seg, _ = up_lim
        for down_lim in downstream_limits:
            down_seg, _ = down_lim
            _, _, list_paths, _ = get_downstream_path(up_seg, down_seg, downstream=True)
            for _, path in list_paths:
                for seg in path:
                    set_segs.add(seg)
    return set_segs


def is_seg_in_block(block, seg: str):
    """ Return True if a segment is in a block else False. """
    return seg in get_segs_in_blocks(block)


def get_block_associated_to_sw(sw):
    """ Get the block associated to a switch. """
    block_dict = load_sheet(DCSYS.CDV)
    for block_name, block_value in block_dict.items():
        if all(is_seg_in_block(block_value, seg)
               for seg in get_dc_sys_values(sw, DCSYS.Aig.SegmentPointe, DCSYS.Aig.SegmentTd, DCSYS.Aig.SegmentTg)):
            return block_name, block_value
    print(f"Unable to find block associated to SW: {sw}")
