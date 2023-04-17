#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database.load_sheets import load_sheet, get_cols_name, get_lim_cols_name
from .cbtc_territory_utils import is_point_in_cbtc_ter
from .dist_utils import get_dist_downstream, get_downstream_path
from .links_utils import is_seg_downstream
from .segments_utils import get_linked_segs


def get_blocks_in_cbtc_ter():
    block_dict = load_sheet("block")
    block_lim_cols_name = get_lim_cols_name("block")
    within_cbtc_block_dict = dict()
    for block, block_values in block_dict.items():
        limits_in_cbtc_ter = list()
        for lim in block_values["limits"]:
            seg = lim[block_lim_cols_name[0]]
            x = lim[block_lim_cols_name[1]]
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter):
            within_cbtc_block_dict[block] = block_values
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"Block {block} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_block_dict[block] = block_values
    return within_cbtc_block_dict


def get_list_len_block(block):
    block_lim_cols_name = get_lim_cols_name("block")
    list_dist = get_len_block_list(block, block_lim_cols_name)
    return list_dist


def get_len_block_list(block, block_lim_cols_name):
    list_dist = list()
    upstream_limits, downstream_limits = find_upstream_n_downstream_limits(block)
    for up_lim in upstream_limits:
        seg1 = up_lim[block_lim_cols_name[0]]
        x1 = float(up_lim[block_lim_cols_name[1]])
        for down_lim in downstream_limits:
            seg2 = down_lim[block_lim_cols_name[0]]
            x2 = float(down_lim[block_lim_cols_name[1]])
            d = get_dist_downstream(seg1, x1, seg2, x2)
            if d is not None:
                list_dist.append(d)
    return list_dist


def find_upstream_n_downstream_limits(block):
    block_lim_cols_name = get_lim_cols_name("block")
    upstream_limits = list()
    downstream_limits = list()
    for lim1 in block["limits"]:
        if is_block_limit_upstream(lim1, block["limits"], block_lim_cols_name):
            upstream_limits.append(lim1)
        else:
            downstream_limits.append(lim1)
    return upstream_limits, downstream_limits


def is_block_limit_upstream(start_lim: dict, limits: list[dict], block_lim_cols_name):
    start_seg = start_lim[block_lim_cols_name[0]]
    start_x = float(start_lim[block_lim_cols_name[1]])
    other_limits = [lim for lim in limits if lim != start_lim]

    for lim in other_limits:
        if lim[block_lim_cols_name[0]] == start_seg:  # two limits of the block are on the same segment
            return start_x <= float(lim[block_lim_cols_name[1]])

    for lim in other_limits:
        seg = lim[block_lim_cols_name[0]]
        if is_seg_downstream(start_seg, seg):  # seg is downstream of start_seg
            if does_path_exist_within_block(start_lim, lim, limits, block_lim_cols_name, downstream=True):
                return True  # start_seg is upstream of another limit within the block
        if is_seg_downstream(seg, start_seg):  # seg is upstream of start_seg
            if does_path_exist_within_block(start_lim, lim, limits, block_lim_cols_name, downstream=False):
                return False  # start_seg is downstream of another limit within the block
    return None


def does_path_exist_within_block(lim1, lim2, block_limits, block_lim_cols_name, downstream: bool = None):
    seg1 = lim1[block_lim_cols_name[0]]
    seg2 = lim2[block_lim_cols_name[0]]
    seg_limits = [lim[block_lim_cols_name[0]] for lim in block_limits]

    if seg1 == seg2:
        return True
    if downstream is None:
        if is_seg_downstream(seg1, seg2):
            downstream = True
        elif is_seg_downstream(seg2, seg1):
            downstream = False
        else:
            return False

    def inner_recurs_seg(seg, end_seg):
        next_segs = get_linked_segs(seg)
        for next_seg in next_segs:
            if next_seg == end_seg:
                return True
            if next_seg not in seg_limits:
                return inner_recurs_seg(next_seg, end_seg)
        return False

    if downstream:
        return inner_recurs_seg(seg1, seg2)
    else:
        return inner_recurs_seg(seg2, seg1)


def get_segs_in_blocks(block):
    """ Return the list of segments in a block. """
    set_segs = set()
    block_lim_cols_name = get_lim_cols_name("block")
    upstream_limits, downstream_limits = find_upstream_n_downstream_limits(block)
    for up_lim in upstream_limits:
        up_seg = up_lim[block_lim_cols_name[0]]
        for down_lim in downstream_limits:
            down_seg = down_lim[block_lim_cols_name[0]]
            _, _, list_paths = get_downstream_path(up_seg, down_seg)
            for path in list_paths:
                for seg in path:
                    set_segs.add(seg)
    return set_segs


def is_seg_in_block(block, seg: str):
    """ Return True if a segment is in a block else False. """
    return seg in get_segs_in_blocks(block)


def get_block_associated_to_sw(sw):
    """ Get the block associated to a switch. """
    sw_cols_name = get_cols_name("sw")
    block_dict = load_sheet("block")
    for block_name, block_value in block_dict.items():
        if all(is_seg_in_block(block_value, sw[sw_cols_name[j]]) for j in ['B', 'C', 'D']):
            return block_name, block_value
    print(f"Unable to find block associated to SW: {sw}")
