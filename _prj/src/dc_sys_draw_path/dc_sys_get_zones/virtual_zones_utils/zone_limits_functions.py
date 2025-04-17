#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ..get_oriented_limits import *
from .draw_segments_in_zone_limits import *


__all__ = ["is_point_in_zone_limits", "is_seg_in_zone_limits", "get_objects_in_zone_limits"]


def is_point_in_zone_limits(zone_limits: list[tuple[str, float, str]],
                            seg: str, x: float, direction: str = None) -> Optional[bool]:
    x = float(x)
    zone_segments = get_segments_within_zone_limits(zone_limits)
    zone_limits = convert_oriented_limits(zone_limits)
    if seg in zone_segments:
        return True

    # limit point
    limits_on_point = [(lim_seg, lim_x, lim_downstream) for lim_seg, lim_x, lim_downstream in zone_limits
                       if are_points_matching(lim_seg, lim_x, seg, x)]
    if limits_on_point:
        lim_downstream = limits_on_point[0][2]
        if direction is not None:
            if lim_downstream != (direction == Direction.CROISSANT):  # for a single point object,
                # we consider it belongs to the zone upstream of it,
                # so the limit of the zone should have an opposite direction to the point
                return True
            else:
                return False
        return None

    limits_on_seg = [(lim_seg, lim_x, lim_downstream) for lim_seg, lim_x, lim_downstream in zone_limits
                     if lim_seg == seg]
    if not limits_on_seg:
        return False

    closest_limit = sorted(limits_on_seg, key=lambda a: abs(a[1] - x))[0]
    lim_seg, lim_x, lim_downstream = closest_limit
    if (lim_downstream and x > lim_x) or (not lim_downstream and x < lim_x):
        return True
    return False


def is_seg_in_zone_limits(zone_limits: list[tuple[str, float, str]], seg: str) -> Optional[bool]:
    zone_segments = get_all_segments_in_zone_limits(zone_limits)
    return seg in zone_segments


def get_objects_in_zone_limits(obj_type, zone_limits: list[tuple[str, float, str]]) -> Optional[list[str]]:
    obj_type = get_sh_name(obj_type)
    list_obj = list()

    obj_list = get_objects_list(obj_type)
    for obj_name in obj_list:
        obj_position = get_object_position(obj_type, obj_name)
        if obj_position is None:
            continue

        if isinstance(obj_position, tuple):  # single point object
            if is_point_in_zone_limits(zone_limits, *obj_position):
                list_obj.append(obj_name)
        else:  # zone object
            pass
    if not list_obj:
        return None
    return list_obj
