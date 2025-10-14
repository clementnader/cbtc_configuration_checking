#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ..get_oriented_limits import *


__all__ = ["get_segments_within_zone", "get_zone_limits", "get_all_segments_in_zone"]


ZONE_SEGMENTS = dict()
ZONE_LIMITS = dict()


SHEETS_TO_DISABLE_WARNINGS = ["IXL_Overlap", "Calib"]
# It is normal to have a switch inside these zones, and that the zone is technically not enclosed,
# because the zones are linear.


def get_segments_within_zone(object_type, object_name: str) -> Optional[set[str]]:
    global ZONE_SEGMENTS, ZONE_LIMITS
    object_type = get_sheet_name(object_type)
    if object_type not in ZONE_SEGMENTS:
        ZONE_SEGMENTS[object_type] = dict()
        ZONE_LIMITS[object_type] = dict()
        _update_segs_within_zones(object_type)
    if object_name not in ZONE_SEGMENTS[object_type]:
        return None
    return ZONE_SEGMENTS[object_type][object_name]


def get_zone_limits(object_type, object_name: str) -> list[tuple[str, float, bool]]:
    global ZONE_SEGMENTS, ZONE_LIMITS
    object_type = get_sheet_name(object_type)
    if object_type not in ZONE_LIMITS:
        ZONE_SEGMENTS[object_type] = dict()
        ZONE_LIMITS[object_type] = dict()
        _update_segs_within_zones(object_type)
    return ZONE_LIMITS[object_type][object_name]


def get_all_segments_in_zone(object_type, object_name: str) -> set[str]:
    zone_segments = get_segments_within_zone(object_type, object_name)
    zone_limits = get_zone_limits(object_type, object_name)
    return zone_segments.union([seg for seg, _, _ in zone_limits])


def _update_segs_within_zones(object_type: str) -> None:
    global ZONE_SEGMENTS, ZONE_LIMITS

    object_list = get_objects_list(object_type)
    warning_has_been_printed_on_the_sheet = False
    for object_name in object_list:
        zone_limits = get_oriented_limits_of_object(object_type, object_name)
        if not zone_limits:
            return
        zone_limits = convert_oriented_limits(zone_limits)

        ZONE_SEGMENTS[object_type][object_name] = set()
        for start_seg, start_x, start_downstream in zone_limits:
            warning_has_been_printed = _get_next_segments(object_type, object_name, start_seg, start_x, start_downstream,
                                                          zone_limits)
            if warning_has_been_printed:
                warning_has_been_printed_on_the_sheet = True

        _update_zone_limits(object_type, object_name, zone_limits)

    if warning_has_been_printed_on_the_sheet:
        print_bar(start="\n")


def _get_next_segments(object_type: str, object_name: str, start_seg: str, start_x: float, downstream: bool,
                      zone_limits: list[tuple[str, float, bool]]) -> bool:
    global ZONE_SEGMENTS
    direction = Direction.CROISSANT if downstream else Direction.DECROISSANT
    start_point_and_direction = f"{(start_seg, start_x)} in direction {direction}"

    first_seg_on_another_limit, warning_has_been_printed = _is_first_seg_on_another_limit(
        object_type, object_name, start_seg, start_x, downstream, zone_limits, start_point_and_direction)

    if first_seg_on_another_limit:  # Limit found on the first segment,
        # no need to run the line to get the segments before reaching other limits, we return.
        return warning_has_been_printed

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[str]):
        global ZONE_SEGMENTS
        nonlocal warning_has_already_been_printed

        if not warning_has_already_been_printed and not get_linked_segments(seg, inner_downstream):
            # if an end of track is reached the zone is open
            if object_type not in SHEETS_TO_DISABLE_WARNINGS:
                warning_has_already_been_printed = True
                print_warning(f"{Color.beige}{object_type}{Color.reset} {Color.yellow}{object_name}{Color.reset} is open, "
                              f"an end of track has been reached while inside the zone. "
                              f"The zone was traveled by starting by the point {start_point_and_direction}.")

        for next_seg in get_linked_segments(seg, inner_downstream):
            if next_seg in path:  # a whole loop has been made, terminate the branch
                continue
            if next_seg == start_seg:  # a whole loop has been made, terminate the branch
                continue

            if is_segment_depolarized(next_seg) and seg in get_associated_depolarization(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream

            test, correct_direction = _is_seg_end_limit(object_type, object_name, next_seg, next_inner_downstream, zone_limits,
                                                        start_point_and_direction)
            if test:
                if correct_direction:
                    ZONE_SEGMENTS[object_type][object_name].update(path)  # only append path if another limit is reached
                # if a limit of the object is reached but not in the correct direction, we stop the progression,
                # but we don't add the path
                continue

            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [next_seg])

    warning_has_already_been_printed = False
    inner_recurs_next_seg(start_seg, downstream, [])

    return warning_has_already_been_printed


G_ALREADY_PRINTED = list()


def _is_first_seg_on_another_limit(object_type: str, object_name: str, start_seg: str, start_x: float, downstream: bool,
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
            if (object_type, object_name, start_seg, start_x, not downstream) in G_ALREADY_PRINTED:
                return True, warning_has_been_printed  # avoid repeating the message

            G_ALREADY_PRINTED.append((object_type, object_name, start_seg, start_x, downstream))
            print_warning(f"Zone {Color.beige}{object_type}{Color.reset} {Color.yellow}{object_name}{Color.reset} "
                          f"is one point: there are 2 limits on the same point {(start_seg, start_x)}"
                          f" in opposite directions.")
            print_warning(f"The zone was traveled by starting by the point {start_point_and_direction}.")
            warning_has_been_printed = True
            return True, warning_has_been_printed

        if start_seg == limit_seg:
            if (downstream and start_x <= limit_x) or (not downstream and start_x >= limit_x):
                if not downstream == limit_downstream:
                    return True, warning_has_been_printed

                # Limit reached in the wrong direction
                print_error(f"Reach a limit for {Color.beige}{object_type}{Color.reset} "
                            f"{Color.yellow}{object_name}{Color.reset} but not in opposite direction:")
                print_error(limit_seg, limit_x, limit_direction, no_prefix=True)
                print_error(f"The zone was traveled by starting by the point {start_point_and_direction}.",
                            no_prefix=True)
                warning_has_been_printed = True
                return True, warning_has_been_printed

    return False, warning_has_been_printed


def _is_seg_end_limit(object_type: str, object_name: str, seg: str, downstream: bool,
                      zone_limits: list[tuple[str, float, bool]], start_point_and_direction: str
                      ) -> tuple[bool, Optional[bool]]:
    if (seg, not downstream) in [(limit_seg, limit_downstream)
                                 for limit_seg, _, limit_downstream in zone_limits]:
        return True, True
    if seg in [limit_seg for limit_seg, _, _ in zone_limits]:
        print_error(f"Reach a limit for {Color.beige}{object_type}{Color.reset} "
                    f"{Color.yellow}{object_name}{Color.reset} but not in opposite direction:")
        print_error(([(limit_seg, limit_x, Direction.CROISSANT if limit_downstream else Direction.DECROISSANT)
                    for limit_seg, limit_x, limit_downstream in zone_limits if seg == limit_seg]), no_prefix=True)
        print_error(f"The zone was traveled by starting by the point {start_point_and_direction}.",
                    no_prefix=True)
        return True, False
    return False, None


def _update_zone_limits(object_type: str, object_name: str, zone_limits: list[tuple[str, float, bool]]) -> None:
    global ZONE_LIMITS
    ZONE_LIMITS[object_type][object_name] = list()
    for lim in zone_limits:
        ZONE_LIMITS[object_type][object_name].append(lim)
