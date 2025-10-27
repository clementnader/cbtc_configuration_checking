#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_par import *
from ...dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point


__all__ = ["check_zc_limits_definition"]


def check_zc_limits_definition():
    eid_is_allowed = get_parameter_value("eid_is_allowed")
    print_section_title(f"{eid_is_allowed = }")
    print_bar(end="")

    for zc_name in get_objects_list(DCSYS.PAS):
        print_section_title(zc_name)
        for seg, x, direction in get_object_position(DCSYS.PAS, zc_name):
            vb1 = get_zones_on_point(DCSYS.CV, seg, x, get_opposite_direction(direction))
            if vb1 is None:  # No last VB inside the ZC
                print_error(f"{zc_name} limit {seg, x, direction} is on no VB.")
                continue
            if len(vb1) > 1:
                print_error(f"{zc_name} limit {seg, x, direction} has multiple VBs on it before it.")
            vb1 = vb1[0]

            vb2 = get_zones_on_point(DCSYS.CV, seg, x, direction)
            if vb2 is None:  # End of track
                continue
            if len(vb2) > 1:
                print_error(f"{zc_name} limit {seg, x, direction} has multiple VBs on it after it.")
            vb2 = vb2[0]

            if direction == Direction.DECROISSANT:
                if x == 0.:
                    print_warning(f"{zc_name} limit {seg, x, direction} should be on segment "
                                  f"where offset is equal to segment length.")
            else:
                if x == get_segment_length(seg):
                    print_warning(f"{zc_name} limit {seg, x, direction} should be on segment "
                                  f"where offset is equal to 0.")

            if vb1 == vb2:
                print_error(f"{zc_name} limit {seg, x, direction} is not on a VB limit, it is inside {vb1}\n"
                            f"(it does not respect CC_ZSUIVI_5: "
                            f"\"Any tracking area limit shall be located at a virtual block limit.\")")
                continue

            vb1_limits = get_object_position(DCSYS.CV, vb1)
            vb2_limits = get_object_position(DCSYS.CV, vb2)

            if not ((seg, x) in vb1_limits):
                print_error(f"{zc_name} limit {seg, x, direction} does not match VB limit of {vb1}.")

            if not ((seg, x) in vb2_limits):
                print_error(f"{zc_name} limit {seg, x, direction} does not match VB limit of {vb2}.")
