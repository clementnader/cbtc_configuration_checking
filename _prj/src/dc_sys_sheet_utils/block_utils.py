#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys_draw_path.dc_sys_path_and_distances import get_dist_downstream, is_seg_downstream
from ..dc_sys_draw_path.dc_sys_get_zones import get_zones_on_object, get_oriented_limits_of_obj


__all__ = ["get_list_len_block", "get_block_associated_to_sw"]


def get_list_len_block(block_name: str):
    list_dist = list()
    oriented_limits = get_oriented_limits_of_obj(DCSYS.CDV, block_name)
    for i, lim1 in enumerate(oriented_limits):
        seg1, x1, direction1 = lim1
        for lim2 in oriented_limits[i+1:]:
            seg2, x2, direction2 = lim2
            if (is_seg_downstream(seg1, seg2, x1, x2, downstream=direction1==Direction.CROISSANT)
                    and is_seg_downstream(seg2, seg1, x2, x1, downstream=direction2==Direction.CROISSANT)):
                d = get_dist_downstream(seg1, x1, seg2, x2, downstream=direction1==Direction.CROISSANT)
                if d is not None:
                    list_dist.append(d)
    return list_dist


def get_block_associated_to_sw(sw_name: str) -> Optional[str]:
    """ Get the block associated to a switch. """
    list_blocks = get_zones_on_object(DCSYS.CDV, DCSYS.Aig, sw_name)
    if not list_blocks:
        print_error(f"Unable to find block associated to switch {sw_name}.")
        return None
    if len(list_blocks) > 1:
        print_error(f"Multiple blocks on switch {sw_name}: {list_blocks}.")
        return None
    block_name = list_blocks[0]
    return block_name
