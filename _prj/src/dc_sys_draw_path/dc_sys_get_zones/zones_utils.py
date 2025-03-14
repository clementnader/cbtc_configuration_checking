#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from .get_oriented_limits import *


__all__ = ["get_segments_within_zone", "get_zone_limits", "get_all_segments_in_zone",
           "is_point_in_zone", "is_seg_in_zone", "get_zones_on_point", "get_zones_on_segment",
           "get_zones_intersecting_zone"]


ZONE_SEGMENTS = dict()
ZONE_LIMITS = dict()


def get_segments_within_zone(obj_type, obj_name: str) -> Optional[set[str]]:
    global ZONE_SEGMENTS, ZONE_LIMITS
    obj_type_name = get_sh_name(obj_type)
    if obj_type_name not in ZONE_SEGMENTS:
        ZONE_SEGMENTS[obj_type_name] = dict()
        ZONE_LIMITS[obj_type_name] = dict()
        _update_segs_within_zones(obj_type_name)
    if obj_name not in ZONE_SEGMENTS[obj_type_name]:
        return None
    return set([seg for seg, _ in ZONE_SEGMENTS[obj_type_name][obj_name]])


def get_zone_limits(obj_type, obj_name: str) -> list[tuple[str, float, bool]]:
    global ZONE_SEGMENTS, ZONE_LIMITS
    obj_type_name = get_sh_name(obj_type)
    if obj_type_name not in ZONE_LIMITS:
        ZONE_SEGMENTS[obj_type_name] = dict()
        ZONE_LIMITS[obj_type_name] = dict()
        _update_segs_within_zones(obj_type_name)
    return ZONE_LIMITS[obj_type_name][obj_name]


def get_all_segments_in_zone(obj_type, obj_name: str) -> set[str]:
    zone_segments = get_segments_within_zone(obj_type, obj_name)
    zone_limits = get_zone_limits(obj_type, obj_name)
    return zone_segments.union([seg for seg, _, _ in zone_limits])


def _update_segs_within_zones(obj_type_name: str) -> None:
    global ZONE_SEGMENTS, ZONE_LIMITS

    obj_dict = load_sheet(obj_type_name)
    warning_has_been_printed_on_the_sheet = False
    for obj_name, obj_info in obj_dict.items():
        zone_limits = get_oriented_limits_of_obj(obj_type_name, obj_name)
        if not zone_limits:
            return

        ZONE_SEGMENTS[obj_type_name][obj_name] = list()
        for start_seg, start_x, start_direction in zone_limits:
            warning_has_been_printed = _get_next_segments(obj_type_name, obj_name, start_seg, start_x, start_direction,
                                                          zone_limits)
            if warning_has_been_printed:
                warning_has_been_printed_on_the_sheet = True

        _update_zone_limits(obj_type_name, obj_name, zone_limits)

    if warning_has_been_printed_on_the_sheet:
        print_bar(start="\n")


def _get_next_segments(obj_type_name: str, obj_name: str, start_seg: str, start_x: float, downstream: bool,
                      zone_limits: list[tuple[str, float, bool]]) -> bool:
    global ZONE_SEGMENTS
    direction = Direction.CROISSANT if downstream else Direction.DECROISSANT
    start_point_and_direction = f"{(start_seg, start_x)} in direction {direction}"

    first_seg_on_another_limit, warning_has_been_printed = _is_first_seg_on_another_limit(
        obj_type_name, obj_name, start_seg, start_x, downstream, zone_limits, start_point_and_direction)

    if first_seg_on_another_limit:  # Limit found on the first segment,
        # no need to run the line to get the segments before reaching other limits, we return.
        return warning_has_been_printed

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[tuple[str, float]]):
        global ZONE_SEGMENTS
        nonlocal warning_has_already_been_printed

        if not warning_has_already_been_printed and not get_linked_segs(seg, inner_downstream):
            # if an end of track is reached the zone is open
            warning_has_already_been_printed = True
            print_warning(f"{Color.beige}{obj_type_name}{Color.reset} {Color.yellow}{obj_name}{Color.reset} is open, "
                          f"an end of track has been reached while inside the zone. "
                          f"The zone was traveled by starting by the point {start_point_and_direction}.")

        for next_seg in get_linked_segs(seg, inner_downstream):
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream

            if _is_seg_end_limit(obj_type_name, obj_name, next_seg, next_inner_downstream, zone_limits,
                                 start_point_and_direction):
                ZONE_SEGMENTS[obj_type_name][obj_name].extend(path)  # only append path if another limit is reached
                continue

            if (next_seg, next_inner_downstream) in ZONE_SEGMENTS[obj_type_name][obj_name]:  # already managed
                ZONE_SEGMENTS[obj_type_name][obj_name].extend(path)  # append the current path and terminate the branch
                continue

            if (next_seg, next_inner_downstream) in path:  # a whole loop has been made
                ZONE_SEGMENTS[obj_type_name][obj_name].extend(path)  # append the current path and terminate the branch
                continue

            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [(next_seg, next_inner_downstream)])

    warning_has_already_been_printed = False
    inner_recurs_next_seg(start_seg, downstream, [])

    return warning_has_already_been_printed


G_ALREADY_PRINTED = list()


def _is_first_seg_on_another_limit(obj_type_name: str, obj_name: str, start_seg: str, start_x: float, downstream: bool,
                                  zone_limits: list[tuple[str, float, bool]], start_point_and_direction: str
                                   ) -> tuple[bool, bool]:
    global G_ALREADY_PRINTED
    warning_has_been_printed = False

    for limit_seg, limit_x, limit_downstream in zone_limits:
        limit_direction = Direction.CROISSANT if limit_downstream else Direction.DECROISSANT
        if (limit_seg, limit_x, limit_downstream) == (start_seg, start_x, downstream):  # the limit corresponding to the
            # start point
            continue
        if (limit_seg, limit_x, limit_downstream) == (start_seg, start_x, not downstream):  # limit corresponding to the
            # start point in opposite direction
            if (obj_type_name, obj_name, start_seg, start_x, not downstream) in G_ALREADY_PRINTED:
                return True, warning_has_been_printed
            G_ALREADY_PRINTED.append((obj_type_name, obj_name, start_seg, start_x, downstream))
            print_warning(f"Zone {Color.beige}{obj_type_name}{Color.reset} {Color.yellow}{obj_name}{Color.reset} "
                          f"is one point: there are 2 limits on the same point {(start_seg, start_x)}"
                          f" in opposite directions.")
            print_warning(f"The zone was traveled by starting by the point {start_point_and_direction}.")
            warning_has_been_printed = True
            return True, warning_has_been_printed
        if start_seg == limit_seg:
            if (downstream and start_x <= limit_x) or (not downstream and start_x >= limit_x):
                if not downstream == limit_downstream:
                    return True, warning_has_been_printed
                print_error(f"Reach a limit for {Color.beige}{obj_type_name}{Color.reset} "
                            f"{Color.yellow}{obj_name}{Color.reset} but not in opposite direction:")
                print_error(limit_seg, limit_x, limit_direction, no_prefix=True)
                print_error(f"The zone was traveled by starting by the point {start_point_and_direction}.",
                            no_prefix=True)
                warning_has_been_printed = True
                return True, warning_has_been_printed
    return False, warning_has_been_printed


def _is_seg_end_limit(obj_type_name: str, obj_name: str, seg: str, downstream: bool,
                     zone_limits: list[tuple[str, float, bool]], start_point_and_direction: str) -> bool:
    if (seg, not downstream) in [(limit_seg, limit_downstream)
                                 for limit_seg, _, limit_downstream in zone_limits]:
        return True
    if seg in [limit_seg for limit_seg, _, _ in zone_limits]:
        print_error(f"Reach a limit for {Color.beige}{obj_type_name}{Color.reset} "
                    f"{Color.yellow}{obj_name}{Color.reset} but not in opposite direction:")
        print_error(([(limit_seg, limit_x, Direction.CROISSANT if limit_downstream else Direction.DECROISSANT)
                    for limit_seg, limit_x, limit_downstream in zone_limits if seg == limit_seg]), no_prefix=True)
        print_error(f"The zone was traveled by starting by the point {start_point_and_direction}.",
                    no_prefix=True)
        return True
    return False


def _update_zone_limits(obj_type_name: str, obj_name: str, zone_limits: list[tuple[str, float, bool]]) -> None:
    global ZONE_LIMITS
    ZONE_LIMITS[obj_type_name][obj_name] = list()
    for lim in zone_limits:
        ZONE_LIMITS[obj_type_name][obj_name].append(lim)


def is_point_in_zone(obj_type, obj_name: str, seg: str, x: float, direction: str = None) -> Optional[bool]:
    obj_type_name = get_sh_name(obj_type)
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
            print_warning(f"Weird zone for {obj_type_name} {Color.blue}{obj_name}{Color.reset} with multiple limits "
                          f"defined on the same point:\n{limits_on_point}")
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


def is_seg_in_zone(obj_type, obj_name: str, seg: str) -> Optional[bool]:
    zone_segments = get_all_segments_in_zone(obj_type, obj_name)
    return seg in zone_segments


def get_zones_on_point(obj_type, seg: str, x: float, direction: str = None) -> Optional[list[str]]:
    list_obj = list()
    obj_dict = load_sheet(obj_type)
    for obj_name in obj_dict.keys():
        if is_point_in_zone(obj_type, obj_name, seg, x, direction) is True:
            list_obj.append(obj_name)
    if not list_obj:
        # print_warning(f"No {get_sh_name(obj_type)} has been found covering {(seg, x)}.")
        return None
    return list_obj


def get_zones_on_segment(obj_type, seg: str) -> Optional[list[str]]:
    list_obj = list()
    obj_dict = load_sheet(obj_type)
    for obj_name in obj_dict.keys():
        if is_seg_in_zone(obj_type, obj_name, seg) is True:
            list_obj.append(obj_name)
    if not list_obj:
        # print_warning(f"No {get_sh_name(obj_type)} has been found covering {(seg, x)}.")
        return None
    return list_obj


def get_zones_intersecting_zone(zones_obj_type, my_obj_type, my_obj_name: str) -> list[str]:
    my_zone_segments = get_segments_within_zone(my_obj_type, my_obj_name)
    my_zone_limits = get_zone_limits(my_obj_type, my_obj_name)

    list_obj = list()
    for seg in my_zone_segments:
        zones = get_zones_on_segment(zones_obj_type, seg)
        if zones is not None:
            list_obj.extend([obj for obj in zones if obj not in list_obj])

    # TODO manage when no segment inside zone
    for seg, x, downstream in my_zone_limits:
        direction = get_reverse_direction(Direction.CROISSANT if downstream else Direction.DECROISSANT)
        # for a single point object, we consider it belongs to the zone upstream of it,
        # behavior is mimicked for the zone too
        zones = get_zones_on_point(zones_obj_type, seg, x, direction)
        if zones is not None:
            list_obj.extend([obj for obj in zones if obj not in list_obj])

    return list_obj
