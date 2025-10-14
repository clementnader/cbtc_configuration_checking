#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ..dc_sys_path_and_distances import is_seg_downstream


__all__ = ["get_oriented_limits_of_object", "convert_oriented_limits"]


def get_oriented_limits_of_object(object_type: str, object_name: str) -> Optional[list[tuple[str, float, str]]]:
    object_type = get_sheet_name(object_type)
    zone_limits = get_object_zone_limits(object_type, object_name)
    if zone_limits is None:  # not a zone object
        return None
    if len(zone_limits[0]) == 3:  # oriented zone limits
        return zone_limits

    # non-oriented limits, we have to compute them

    # If there are common limits, we consider them in both directions, and we remove them of the computation.
    no_duplicate_zone_limits, common_oriented_limits = _remove_common_limits(zone_limits)
    if common_oriented_limits:
        print_warning(f"For {object_type} {object_name}, there are 2 limits on the same point: "
                      f"{[(seg, x) for seg, x, _ in common_oriented_limits]}")

    other_oriented_limits = _get_orientation_of_zone_limits(object_type, object_name, no_duplicate_zone_limits)

    return _reorder_oriented_limits(common_oriented_limits + other_oriented_limits, zone_limits)


def _reorder_oriented_limits(oriented_limits: list[tuple[str, float, str]], zone_limits: list[tuple[str, float]]):
    # we keep the same order as the order of the non-oriented limits in DC_SYS,
    # in case of double limit in DC_SYS we sort increasing direction before decreasing
    return sorted(oriented_limits, key=lambda limit: (zone_limits.index((limit[0], limit[1])),
                                                      not (limit[2] == Direction.CROISSANT)))


def convert_oriented_limits(oriented_zone_limits: list[tuple[str, float, str]]) -> list[tuple[str, float, bool]]:
    zone_limits = [(seg, x, (direction == Direction.CROISSANT)) for seg, x, direction in oriented_zone_limits]
    return zone_limits


def _remove_common_limits(zone_limits: list[tuple[str, float]]) -> tuple[list[tuple[str, float]],
                                                                         list[tuple[str, float, str]]]:
    common_limits = list()
    oriented_limits = list()
    for i, (seg1, x1) in enumerate(zone_limits):
        if (seg1, x1) in zone_limits[i+1:]:
            common_limits.append((seg1, x1))
            oriented_limits.append((seg1, x1, Direction.CROISSANT))
            oriented_limits.append((seg1, x1, Direction.DECROISSANT))

    if not common_limits:
        return zone_limits, list()

    return [limit for limit in zone_limits if limit not in common_limits], oriented_limits


def _get_orientation_of_zone_limits(object_type: str, object_name: str, zone_limits: list[tuple[str, float]]
                                    ) -> list[tuple[str, float, str]]:
    if not zone_limits:
        return list()

    oriented_zone_limits = list()
    for seg1, x1 in zone_limits:
        are_other_limits_downstream = [is_seg_downstream(seg1, seg2, x1, x2, downstream=True)
                                       for seg2, x2 in zone_limits if (seg2, x2) != (seg1, x1)]
        are_other_limits_upstream = [is_seg_downstream(seg1, seg2, x1, x2, downstream=False)
                                     for seg2, x2 in zone_limits if (seg2, x2) != (seg1, x1)]
        if any(are_other_limits_downstream) and not any(are_other_limits_upstream):
            direction = Direction.CROISSANT
        elif any(are_other_limits_upstream) and not any(are_other_limits_downstream):
            direction = Direction.DECROISSANT
        elif any(are_other_limits_upstream) and any(are_other_limits_downstream):
            direction = None
        else:  # not any upstream and not any downstream
            print_error(f"Unable to find direction for limit {(seg1, x1)} of "
                        f"{Color.beige}{object_type}{Color.reset} {Color.yellow}{object_name}{Color.reset}.")
            direction = None
        if direction is not None:
            oriented_zone_limits.append((seg1, x1, direction))

    missed_limits = _get_missed_limits(oriented_zone_limits, zone_limits)
    if not missed_limits:
        return oriented_zone_limits

    return _update_missed_limits(object_type, object_name, oriented_zone_limits, zone_limits)


def _get_missed_limits(oriented_zone_limits: list[tuple[str, float, str]],
                       zone_limits: list[tuple[str, float]]) -> list[tuple[str, float]]:
    return [limit for limit in zone_limits if limit not in [(seg, x) for seg, x, _ in oriented_zone_limits]]


def _update_missed_limits(object_type: str, object_name: str,
                          oriented_zone_limits: list[tuple[str, float, Optional[str]]],
                          zone_limits: list[tuple[str, float]]) -> list[tuple[str, float, Optional[str]]]:
    nb_limits = len(zone_limits)
    for cnt in range(nb_limits):
        missed_limits = _get_missed_limits(oriented_zone_limits, zone_limits)
        if not missed_limits:  # all limits orientations have been found
            break

        if cnt < len(oriented_zone_limits):  # we try to reach limits from an already oriented limit
            start_limit = oriented_zone_limits[cnt]
            other_limits, wrong_limit_direction = _find_other_limits(start_limit, zone_limits)
            if wrong_limit_direction:
                print_error(f"Reached the end of track, the zone is not closed for "
                            f"{Color.beige}{object_type}{Color.reset} {Color.yellow}{object_name}{Color.reset}:\n"
                            f"problem starting from {start_limit}: "
                            f"end of track has been reached or a whole loop has been made.")
                continue
            oriented_zone_limits.extend([limit for limit in other_limits if limit not in oriented_zone_limits])

        else:  # we try to reach limits from a non-oriented limit (we will try in both directions)
            cnt -= len(oriented_zone_limits)
            start_limit_seg, start_limit_x = missed_limits[cnt]
            # try in increasing direction
            start_limit = (start_limit_seg, start_limit_x, Direction.CROISSANT)
            other_limits, wrong_limit_direction = _find_other_limits(start_limit, zone_limits)
            if wrong_limit_direction:
                # try in decreasing direction
                start_limit = (start_limit_seg, start_limit_x, Direction.DECROISSANT)
                other_limits, wrong_limit_direction = _find_other_limits(start_limit, zone_limits)
                if wrong_limit_direction:
                    print_error(f"Reached the end of track, the zone is not closed for "
                                f"{Color.beige}{object_type}{Color.reset} {Color.yellow}{object_name}{Color.reset}:\n"
                                f"problem starting from {(start_limit_seg, start_limit_x)} (tried in both directions): "
                                f"end of track has been reached or a whole loop has been made.")
                    continue
            oriented_zone_limits.append(start_limit)
            oriented_zone_limits.extend([limit for limit in other_limits if limit not in oriented_zone_limits])

    missed_limits = _get_missed_limits(oriented_zone_limits, zone_limits)
    if missed_limits:  # Not all limits orientation has been found
        print_error(f"Unable to get all oriented limits for {Color.beige}{object_type}{Color.reset} "
                    f"{Color.yellow}{object_name}{Color.reset}.")
        print(f"{zone_limits = }\n{oriented_zone_limits = }")
        oriented_zone_limits.extend([(seg, x, None) for seg, x in missed_limits])

    return oriented_zone_limits


def _find_other_limits(start_limit: tuple[str, float, str], zone_limits: list[tuple[str, float]]
                      ) -> tuple[list[tuple[str, float, str]], bool]:
    start_seg, start_x, start_direction = start_limit
    downstream = start_direction == Direction.CROISSANT
    other_limit = _first_seg_on_another_limit(start_seg, start_x, start_direction, downstream, zone_limits)
    if other_limit is not None:
        return [other_limit], False

    other_limits = list()
    wrong_limit_direction = False
    all_accessed_segs = list()

    def inner_recurs_next_seg(seg: str, inner_downstream: bool):
        nonlocal other_limits, wrong_limit_direction, all_accessed_segs
        if wrong_limit_direction:
            return
        if not get_linked_segments(seg, inner_downstream):  # reach end of track
            wrong_limit_direction = True
            return

        all_accessed_segs.append((seg, inner_downstream))
        for next_seg in get_linked_segments(seg, inner_downstream):
            if is_segment_depolarized(next_seg) and seg in get_associated_depolarization(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream

            if (next_seg, next_inner_downstream) in all_accessed_segs:  # a whole loop has been made
                wrong_limit_direction = True
                return

            reached_limit = _reached_other_limit(next_seg, next_inner_downstream, zone_limits)
            if reached_limit is not None:
                if reached_limit not in other_limits:
                    other_limits.append(reached_limit)
                continue
            inner_recurs_next_seg(next_seg, next_inner_downstream)

    inner_recurs_next_seg(start_seg, downstream)
    return other_limits, wrong_limit_direction


def _first_seg_on_another_limit(start_seg: str, start_x: float, start_direction: str, downstream: bool,
                               zone_limits: list[tuple[str, float]]) -> Optional[tuple[str, float, str]]:
    for limit_seg, limit_x in zone_limits:
        if start_seg == limit_seg:
            if (downstream and start_x < limit_x) or (not downstream and start_x > limit_x):
                return limit_seg, limit_x, get_opposite_direction(start_direction)
    return None


def _reached_other_limit(start_seg: str, downstream: bool,
                        zone_limits: list[tuple[str, float]]) -> Optional[tuple[str, float, str]]:
    start_direction = Direction.CROISSANT if downstream else Direction.DECROISSANT
    for limit_seg, limit_x in zone_limits:
        if start_seg == limit_seg:
            return limit_seg, limit_x, get_opposite_direction(start_direction)
    return None
