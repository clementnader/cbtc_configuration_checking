#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...dc_sys_path_and_distances.dist_utils import (get_all_downstream_segments, get_all_upstream_segments,
                                                     get_upstream_segs_according_to_direction)
from ..get_oriented_limits import *
from ..zones_utils.zone_functions import get_segments_within_zone, get_zone_limits, is_seg_in_zone, is_point_in_zone
from .draw_segments_in_zone_limits import *


__all__ = ["is_point_in_zone_limits", "is_seg_in_zone_limits", "get_objects_in_zone_limits",
           "get_zones_intersecting_zone_limits", "depolarization_in_zone_limits",
           "get_dist_downstream_within_zone_limits"]


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


def depolarization_in_zone_limits(zone_limits: list[tuple[str, float, str]]) -> list[list[str]]:
    depolarized_segments = get_depolarized_segments()
    all_depolarized_segments = [segment_name for sub_list in depolarized_segments for segment_name in sub_list]
    segments_in_zone = get_all_segments_in_zone_limits(zone_limits)
    if not any(seg in segments_in_zone for seg in all_depolarized_segments):
        return []

    list_depol_in_zone = list()
    for depol_group in depolarized_segments:
        if len(depol_group) == 2:
            if all(seg in segments_in_zone for seg in depol_group):
                list_depol_in_zone.append(depol_group)
        else:  # len(depol_group) == 3
            if all(seg in segments_in_zone for seg in depol_group):
                list_depol_in_zone.append(depol_group)
                continue

            for i, depol_seg in enumerate(depol_group):
                if depol_seg not in segments_in_zone:
                    continue
                for other_depol_seg in depol_group[i+1:]:
                    if other_depol_seg not in segments_in_zone:
                        continue
                    # in a 3-segment group, there are the 2 heel segments of a switch and if there are only
                    # these 2 segments, there is no depolarization in the zone, so we check if they are connected
                    if (other_depol_seg in get_linked_segments(depol_seg, downstream=True)
                            or other_depol_seg in get_linked_segments(depol_seg, downstream=False)):
                        list_depol_in_zone.append([depol_seg, other_depol_seg])
    return list_depol_in_zone


def get_zones_intersecting_zone_limits(zones_obj_type, zone_limits: list[tuple[str, float, str]]) -> list[str]:
    list_obj = list()
    obj_list = get_objects_list(zones_obj_type)
    for obj_name in obj_list:
        if is_zone_intersecting_zone_limits(zones_obj_type, obj_name, zone_limits):
            list_obj.append(obj_name)
    return list_obj


def is_zone_intersecting_zone_limits(obj_type, obj_name: str, zone_limits: list[tuple[str, float, str]]):
    zone_segments1 = get_segments_within_zone(obj_type, obj_name)
    zone_limits1 = get_zone_limits(obj_type, obj_name)
    zone_segments2 = get_segments_within_zone_limits(zone_limits)
    zone_limits2 = zone_limits

    for seg in zone_segments1:
        if is_seg_in_zone_limits(zone_limits, seg):
            return True
    for seg in zone_segments2:
        if is_seg_in_zone(obj_type, obj_name, seg):
            return True

    for seg, x, downstream in zone_limits1:
        limit_direction = Direction.CROISSANT if downstream else Direction.DECROISSANT
        test_direction = get_reverse_direction(limit_direction)
        # for a single point object, we consider it belongs to the zone upstream of it,
        # behavior is mimicked for the zone limits too
        if is_point_in_zone_limits(zone_limits, seg, x, test_direction):
            return True

    for seg, x, downstream in zone_limits2:
        limit_direction = Direction.CROISSANT if downstream else Direction.DECROISSANT
        test_direction = get_reverse_direction(limit_direction)
        # for a single point object, we consider it belongs to the zone upstream of it,
        # behavior is mimicked for the zone limits too
        if is_point_in_zone(obj_type, obj_name, seg, x, test_direction):
            return True

    return False


def get_dist_downstream_within_zone_limits(seg1: str, x1: float, seg2: str, x2: float, downstream: bool,
                                           zone_limits: list[tuple[str, float, str]]) -> Optional[float]:
    if (is_point_in_zone_limits(zone_limits, seg1, x1) is False
            or is_point_in_zone_limits(zone_limits, seg2, x2) is False):
        return None
    x1 = float(x1)
    x2 = float(x2)
    if seg1 == seg2:
        if downstream == (x1 <= x2):
            return round(abs(x1-x2), 3)
        else:
            return None

    dist, _, upstream = get_min_path_downstream_within_zone_limits(seg1, seg2, downstream, zone_limits)

    if dist is None:
        return None

    if downstream:  # seg2 is downstream of seg1
        dist -= x1
    else:  # seg2 is upstream of seg1
        dist -= (get_segment_length(seg1) - x1)
    if upstream:  # seg1 is upstream of seg2
        dist -= (get_segment_length(seg2) - x2)
    else:  # seg1 is downstream of seg2
        dist -= x2
    return round(dist, 3)


def get_min_path_downstream_within_zone_limits(start_seg: str, end_seg: str, downstream: bool,
                                               zone_limits: list[tuple[str, float, str]]
                                               ) -> tuple[Optional[float], list[str], Optional[bool]]:
    min_len = -1
    min_path = []
    associated_upstream = None
    if ((downstream and end_seg not in [seg for seg, _ in get_all_downstream_segments(start_seg)])
            or (not downstream and end_seg not in [seg for seg, _ in get_all_upstream_segments(start_seg)])):
        return None, [], None

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[str], path_len: float):
        nonlocal min_len, min_path, associated_upstream
        if min_len != -1 and path_len >= min_len:  # we reach a larger distance, we can stop
            return
        if seg == end_seg and inner_downstream == upstream:  # destination segment is reached in the correct direction
            # path_len will be inferior to min_len so no need to do the comparison
            min_len = path_len
            min_path = path
            associated_upstream = upstream
            return
        if seg not in get_all_segments_in_zone_limits(zone_limits):  # not inside the zone limits, we stop
            return
        if (seg, not inner_downstream) not in accessible_segs_from_end:  # to optimize:
            # if we reach a segment not accessible from the end segment in the other direction, we can stop,
            # this path will not lead to the end segment
            return
        for next_seg in get_linked_segments(seg, inner_downstream):
            if next_seg in path:  # a whole loop has been made
                continue
            if is_segment_depolarized(next_seg) and seg in get_associated_depolarization(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [next_seg],
                                  round(path_len + get_segment_length(next_seg), 3))

    for upstream, accessible_segs_from_end in get_upstream_segs_according_to_direction(end_seg, start_seg, downstream):
        inner_recurs_next_seg(start_seg, downstream, [start_seg], get_segment_length(start_seg))

    if min_len == -1:
        return None, [], None
    return min_len, min_path, associated_upstream
