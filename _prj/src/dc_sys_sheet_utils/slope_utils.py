#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_path_and_distances import get_dist_downstream, get_virtual_seg_ordered_extremities
from ..dc_sys_draw_path.dc_sys_get_zones import get_objects_in_zone_limits


__all__ = ["get_slope_at_point", "get_min_and_max_slopes_at_point", "get_min_and_max_slopes_on_virtual_seg",
           "get_next_slope", "get_min_and_max_slopes_in_zone_limits"]


def get_slope_at_point(seg: str, x: float) -> float:
    downstream_slope = get_next_slope(seg, x, downstream=True)
    upstream_slope = get_next_slope(seg, x, downstream=False)

    downstream_seg, downstream_x = get_dc_sys_values(downstream_slope, DCSYS.Profil.Seg, DCSYS.Profil.X)
    downstream_slope_value = get_dc_sys_value(downstream_slope, DCSYS.Profil.Pente)

    upstream_seg, upstream_x = get_dc_sys_values(upstream_slope, DCSYS.Profil.Seg, DCSYS.Profil.X)
    upstream_slope_value = get_dc_sys_value(upstream_slope, DCSYS.Profil.Pente)

    if downstream_slope_value == upstream_slope_value:
        # Constant slope
        return downstream_slope_value

    if (seg, x) == (downstream_seg, downstream_x):
        return downstream_slope_value
    if (seg, x) == (upstream_seg, upstream_x):
        return upstream_slope_value

    total_distance = get_dist_downstream(upstream_seg, upstream_x, downstream_seg, downstream_x, downstream=True)
    if total_distance is None:
        # TODO solve problem with depol, cf Milan ML4
        print_error(f"Unable to compute distance for slope:")
        print(upstream_seg, upstream_x, upstream_slope_value, downstream_seg, downstream_x, downstream_slope_value)
        return 0.
    sub_distance = get_dist_downstream(upstream_seg, upstream_x, seg, x, downstream=True)
    # linear approximation of the slope between two points
    slope_value = (downstream_slope_value - upstream_slope_value) / total_distance * sub_distance + upstream_slope_value
    return round(slope_value, 7)


def get_next_slope(start_seg: str, start_x: float, downstream: bool) -> Optional[dict[str, Any]]:
    slopes = list()

    def inner_recurs_next_seg(seg: str, x: float = None):
        nonlocal slopes
        slope = _is_slope_defined(seg, downstream=downstream, x=x)
        if slope is not False:
            slopes.append(slope)
            return
        for next_seg in get_linked_segments(seg, downstream=downstream):
            inner_recurs_next_seg(next_seg)

    inner_recurs_next_seg(start_seg, start_x)

    if not slopes:
        print_log(f"No slope found {'downstream' if downstream else 'upstream'} {(start_seg, start_x)}. "
                  "The first slope in the other direction is taken, assuming slope is constant till end of track.\n")
        return get_next_slope(start_seg, start_x, not downstream)
    if len(slopes) > 1:
        slopes.sort(
            key=lambda slope: get_dist_downstream(start_seg, start_x, *get_dc_sys_values(
                slope, DCSYS.Profil.Seg, DCSYS.Profil.X), downstream=downstream))
    return slopes[0]


def get_min_and_max_slopes_at_point(seg: str, x: float) -> tuple[float, float]:
    slopes = get_next_slopes(seg, x, downstream=True)
    slopes.extend(get_next_slopes(seg, x, downstream=False))
    slopes_value = [float(get_dc_sys_value(slope, DCSYS.Profil.Pente)) for slope in slopes]
    return min(slopes_value), max(slopes_value)


def get_next_slopes(start_seg: str, start_x: float, downstream: bool) -> list[dict[str, Any]]:
    """ Return a list of the first slopes reached in the given downstream direction starting from the given point.
    If a switch is met before reaching a slope, the list will be composed of multiple slopes for each path. """
    slopes = list()

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[str], x: float = None) -> None:
        nonlocal slopes
        slope = _is_slope_defined(seg, downstream=inner_downstream, x=x)
        if slope is not False:
            slopes.append(slope)
            return

        linked_segs = get_linked_segments(seg, inner_downstream)
        if not linked_segs:
            return
        for next_seg in linked_segs:
            if is_segment_depolarized(next_seg) and seg in get_associated_depolarization(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream

            if next_seg in path:
                # We check if we have made a full turn and reach a segment that we have already run through
                # in the current path.
                continue
            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [next_seg])

    inner_recurs_next_seg(start_seg, downstream, [start_seg], start_x)
    return slopes


def _is_slope_defined(seg: str, downstream: bool = True, x: float = None) -> Union[bool, dict[str, Any]]:
    """ Return the first slope on the segment in the given downstream direction (or first slope after the offset x
    if it is specified),
    return False if there is no slope on the segment (or no slope after the offset x if it is specified). """
    slope_dict = load_sheet(DCSYS.Profil)
    if x is not None:
        x = float(x)
    slopes = list()
    for slope in slope_dict.values():
        slope_seg = get_dc_sys_value(slope, DCSYS.Profil.Seg)
        slope_x = float(get_dc_sys_value(slope, DCSYS.Profil.X))
        if seg == slope_seg:
            if downstream:
                if x is None or x <= slope_x:
                    slopes.append(slope)
            else:
                if x is None or x >= slope_x:
                    slopes.append(slope)
    if not slopes:
        return False
    # Return closest slope
    slopes.sort(key=lambda a: float(get_dc_sys_value(a, DCSYS.Profil.X)))  # sort according to offset value
    if downstream:
        return slopes[0]  # return the slope closest from the segment start
    else:
        return slopes[-1]  # return the slope closest from the segment end


def get_min_and_max_slopes_on_virtual_seg(seg1: str, x1: float, seg2: str, x2: float):
    # TODO: manage depolarization -> to delete and use next function with oriented limits
    seg1, x1, seg2, x2 = get_virtual_seg_ordered_extremities(seg1, x1, seg2, x2)  # assert seg1 is upstream of seg2

    slopes = get_objects_in_zone_limits(DCSYS.Profil, [(seg1, x1, Direction.CROISSANT),
                                                       (seg2, x2, Direction.DECROISSANT)])
    slopes_values = [float(get_dc_sys_value(slope, DCSYS.Profil.Pente)) for slope in slopes]
    slopes_values.append(get_slope_at_point(seg1, x1))
    slopes_values.append(get_slope_at_point(seg2, x2))
    return min(slopes_values), max(slopes_values)


def get_min_and_max_slopes_in_zone_limits(zone_limits: list[tuple[str, float, str]]
                                          ) -> tuple[float, float]:
    # If there is slope changes inside the zone
    in_slopes = get_objects_in_zone_limits(DCSYS.Profil, zone_limits)
    if in_slopes is None:
        slopes_values = []
    else:
        slopes_values = [float(get_dc_sys_value(slope, DCSYS.Profil.Pente)) for slope in in_slopes]

    # Add the first slope gotten after each limit in the opposite direction (outside the zone)
    for limit in zone_limits:
        seg, x, direction = limit
        slopes_after_limit = get_next_slopes(seg, x, downstream=(direction == Direction.DECROISSANT))
        slopes_values.extend(float(get_dc_sys_value(slope_after_limit, DCSYS.Profil.Pente))
                             for slope_after_limit in slopes_after_limit)

    return min(slopes_values), max(slopes_values)
