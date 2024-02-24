#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from .get_oriented_limits import *


__all__ = ["get_segments_within_zone", "get_zone_limits", "get_all_segments_in_zone",
           "is_point_in_zone", "get_zones_on_point", "get_zones_of_extremities"]


ZONE_SEGMENTS = dict()
ZONE_LIMITS = dict()


def get_segments_within_zone(obj_type, obj_name: str) -> set[str]:
    global ZONE_SEGMENTS, ZONE_LIMITS
    obj_type_name = get_sh_name(obj_type)
    if obj_type_name not in ZONE_SEGMENTS:
        ZONE_SEGMENTS[obj_type_name] = dict()
        ZONE_LIMITS[obj_type_name] = dict()
        update_segs_within_zones(obj_type_name)
    return set([seg for seg, _ in ZONE_SEGMENTS[obj_type_name][obj_name]])


def get_zone_limits(obj_type, obj_name: str) -> list[tuple[str, float, bool]]:
    global ZONE_SEGMENTS, ZONE_LIMITS
    obj_type_name = get_sh_name(obj_type)
    if obj_type_name not in ZONE_LIMITS:
        ZONE_SEGMENTS[obj_type_name] = dict()
        ZONE_LIMITS[obj_type_name] = dict()
        update_segs_within_zones(obj_type_name)
    return ZONE_LIMITS[obj_type_name][obj_name]


def get_all_segments_in_zone(obj_type, obj_name: str) -> set[str]:
    zone_segments = get_segments_within_zone(obj_type, obj_name)
    zone_limits = get_zone_limits(obj_type, obj_name)
    return zone_segments.union([seg for seg, _, _ in zone_limits])


def update_segs_within_zones(obj_type_name: str) -> None:
    global ZONE_SEGMENTS, ZONE_LIMITS

    obj_dict = load_sheet(obj_type_name)
    for obj_name, obj_info in obj_dict.items():
        zone_limits = get_oriented_limits_of_obj(obj_type_name, obj_name)
        if not zone_limits:
            return

        ZONE_SEGMENTS[obj_type_name][obj_name] = list()
        for start_seg, start_x, start_direction in zone_limits:
            get_next_segments(obj_type_name, obj_name, start_seg, start_x, start_direction, zone_limits)

        update_zone_limits(obj_type_name, obj_name, zone_limits)


def get_next_segments(obj_type_name: str, obj_name: str, start_seg: str, start_x: float, downstream: bool,
                      zone_limits: list[tuple[str, float, bool]]) -> None:
    global ZONE_SEGMENTS

    if is_first_seg_on_another_limit(obj_type_name, obj_name, start_seg, start_x, downstream, zone_limits):
        return

    def inner_recurs_next_seg(seg: str, inner_downstream: bool):
        global ZONE_SEGMENTS
        for next_seg in get_linked_segs(seg, inner_downstream):
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            if is_seg_end_limit(obj_type_name, obj_name, next_seg, next_inner_downstream, zone_limits):
                continue
            if (next_seg, next_inner_downstream) in ZONE_SEGMENTS[obj_type_name][obj_name]:
                continue
            ZONE_SEGMENTS[obj_type_name][obj_name].append((next_seg, next_inner_downstream))
            inner_recurs_next_seg(next_seg, next_inner_downstream)

    inner_recurs_next_seg(start_seg, downstream)


def is_first_seg_on_another_limit(obj_type_name: str, obj_name: str, start_seg: str, start_x: float, downstream: bool,
                                  zone_limits: list[tuple[str, float, bool]]) -> bool:
    for limit_seg, limit_x, limit_downstream in zone_limits:
        if start_seg == limit_seg:
            if (downstream and start_x < limit_x) or (not downstream and start_x > limit_x):
                if not downstream == limit_downstream:
                    return True
                print_warning(f"Reach a limit for {obj_type_name} {obj_name} but with a different direction.")
                print(f"{start_seg = }, {start_x = }, {downstream = }")
                print((limit_seg, limit_x, limit_downstream))
                return True
    return False


def is_seg_end_limit(obj_type_name: str, obj_name: str, seg: str, downstream: bool,
                     zone_limits: list[tuple[str, float, bool]]) -> bool:
    if (seg, not downstream) in [(limit_seg, limit_downstream)
                                 for limit_seg, _, limit_downstream in zone_limits]:
        return True
    if seg in [limit_seg for limit_seg, _, _ in zone_limits]:
        print_warning(f"Reach a limit for {obj_type_name} {obj_name} but with a different direction.")
        print(f"{seg = }, {downstream = }")
        print([limit_seg for limit_seg, _, _ in zone_limits if seg == limit_seg])
        return True
    return False


def update_zone_limits(obj_type_name: str, obj_name: str, zone_limits: list[tuple[str, float, bool]]) -> None:
    global ZONE_LIMITS
    ZONE_LIMITS[obj_type_name][obj_name] = list()
    for lim in zone_limits:
        ZONE_LIMITS[obj_type_name][obj_name].append(lim)


def is_point_in_zone(obj_type, obj_name: str, seg: str, x: float, direction: str = None) -> Optional[bool]:
    x = float(x)
    zone_segments = get_segments_within_zone(obj_type, obj_name)
    zone_limits = get_zone_limits(obj_type, obj_name)
    if seg in zone_segments:
        return True

    # limit point
    limits_on_point = [(lim_seg, lim_x, lim_downstream) for lim_seg, lim_x, lim_downstream in zone_limits
                       if are_points_matching(lim_seg, lim_x, seg, x)]
    if limits_on_point:
        if len(limits_on_point) > 1:
            print_warning(f"Weird zone for {obj_type} {Color.blue}{obj_name}{Color.reset} with multiple limits defined "
                          f"on the same point:\n{limits_on_point}")
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


def get_zones_on_point(obj_type, seg: str, x: float, direction: str = None) -> Optional[list[str]]:
    list_obj = list()
    obj_dict = load_sheet(obj_type)
    for obj_name in obj_dict.keys():
        if is_point_in_zone(obj_type, obj_name, seg, x, direction) is True:
            list_obj.append(obj_name)
    if not list_obj:
        # print_warning(f"No {obj_type} has been found covering {(seg, x)}.")
        return None
    return list_obj


def get_zones_of_extremities(obj_type, limits: Union[list[tuple[str, float]], list[tuple[str, float, str]]]
                             ) -> list[str]:
    list_obj = list()
    for lim in limits:
        seg, x = lim[0], lim[1]
        if len(lim) > 2:
            direction = get_reverse_direction(lim[2])  # for a single point object,
            # we consider it belongs to the zone upstream of it,
            # behavior is mimicked for the zone too
        else:
            direction = None
        zones = get_zones_on_point(obj_type, seg, x, direction)
        if zones is not None:
            list_obj.extend([obj for obj in zones if obj not in list_obj])
    return list_obj
