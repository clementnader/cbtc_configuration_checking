#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....dc_sys import *
from ..get_oriented_limits import *


__all__ = ["get_segments_within_zone_limits", "get_all_segments_in_zone_limits"]


def get_segments_within_zone_limits(zone_limits: list[tuple[str, float, str]]) -> set[str]:
    zone_limits = convert_oriented_limits(zone_limits)
    segments_within_zone = list()
    for start_seg, start_x, start_direction in zone_limits:
        segments_within_zone = _get_next_segments(start_seg, start_x, start_direction, zone_limits,
                                                  segments_within_zone)
    return set([seg for seg, _ in segments_within_zone])


def get_all_segments_in_zone_limits(zone_limits: list[tuple[str, float, str]]) -> set[str]:
    zone_segments = get_segments_within_zone_limits(zone_limits)
    return zone_segments.union([seg for seg, _, _ in zone_limits])


def _get_next_segments(start_seg: str, start_x: float, downstream: bool,
                       zone_limits: list[tuple[str, float, bool]], segments_within_zone: list[str, bool]
                       ) -> list[str, bool]:

    if _is_first_seg_on_another_limit(start_seg, start_x, downstream, zone_limits):  # Limit found on the first segment,
        # no need to run the line to get the segments before reaching other limits, we return.
        return segments_within_zone

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[tuple[str, bool]]):
        nonlocal segments_within_zone

        if not get_linked_segments(seg, inner_downstream):
            # if an end of track is reached the zone is open
            pass

        for next_seg in get_linked_segments(seg, inner_downstream):
            if is_segment_depolarized(next_seg) and seg in get_associated_depolarization(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream

            test, correct_direction = _is_seg_end_limit(next_seg, next_inner_downstream, zone_limits)
            if test:
                if correct_direction:
                    segments_within_zone.extend(path)  # only append path if another limit is reached
                # if a limit of the object is reached but not in the correct direction, we stop the progression,
                # but we don't add the path
                continue

            if (next_seg, next_inner_downstream) in segments_within_zone:  # already managed
                segments_within_zone.extend(path)  # append the current path and terminate the branch
                continue

            if (next_seg, next_inner_downstream) in path:  # a whole loop has been made
                segments_within_zone.extend(path)  # append the current path and terminate the branch
                continue

            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [(next_seg, next_inner_downstream)])

    inner_recurs_next_seg(start_seg, downstream, [])

    return segments_within_zone


def _is_first_seg_on_another_limit(start_seg: str, start_x: float, downstream: bool,
                                   zone_limits: list[tuple[str, float, bool]]) -> bool:

    for limit_seg, limit_x, limit_downstream in zone_limits:

        if (limit_seg, limit_x, limit_downstream) == (start_seg, start_x, downstream):
            # the limit corresponding to the start point
            continue

        if (limit_seg, limit_x, limit_downstream) == (start_seg, start_x, not downstream):
            # limit corresponding to the start point in opposite direction, empty zone on this segment
            return True

        if start_seg == limit_seg:
            if (downstream and start_x <= limit_x) or (not downstream and start_x >= limit_x):
                if not downstream == limit_downstream:
                    return True

                # Limit reached in the wrong direction
                return True

    return False


def _is_seg_end_limit(seg: str, downstream: bool,
                      zone_limits: list[tuple[str, float, bool]]) -> tuple[bool, Optional[bool]]:
    if (seg, not downstream) in [(limit_seg, limit_downstream)
                                 for limit_seg, _, limit_downstream in zone_limits]:
        return True, True
    if seg in [limit_seg for limit_seg, _, _ in zone_limits]:
        # limit in the wrong direction
        return True, False
    return False, None
