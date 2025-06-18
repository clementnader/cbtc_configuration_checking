#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_path_and_distances import is_seg_downstream
from ..dc_sys_draw_path.dc_sys_get_zones import (get_objects_in_zone_limits, depolarization_in_zone_limits,
                                                 is_seg_in_zone_limits, get_oriented_limits_of_obj)


__all__ = ["get_slope_at_point", "get_min_and_max_slopes_at_point", "get_next_slopes",
           "get_min_and_max_slopes_in_zone_limits", "get_min_and_max_slopes_in_zone"]


def get_slope_at_point(seg: str, x: float) -> float:
    downstream_slopes = get_next_slopes(seg, x, downstream=True)
    upstream_slopes = get_next_slopes(seg, x, downstream=False)

    list_slopes = list()

    if not downstream_slopes and not upstream_slopes:
        print_error(f"No slopes found downstream nor upstream of point {(seg, x)}")
        return 0.

    if not downstream_slopes:
        for upstream_slope, upstream_polarity, _ in upstream_slopes:
            upstream_slope_value = (get_dc_sys_value(upstream_slope, DCSYS.Profil.Pente)
                                    * (-1 if not upstream_polarity else 1))
            list_slopes.append(upstream_slope_value)
        if not all(slope_value == list_slopes[0] for slope_value in list_slopes):
            print_error(f"Computed slope values are not constant at point {(seg, x)}: {list_slopes}")
        return list_slopes[0]

    if not upstream_slopes:
        for downstream_slope, downstream_polarity, _ in downstream_slopes:
            downstream_slope_value = (get_dc_sys_value(downstream_slope, DCSYS.Profil.Pente)
                                      * (-1 if not downstream_polarity else 1))
            list_slopes.append(downstream_slope_value)
        if not all(slope_value == list_slopes[0] for slope_value in list_slopes):
            print_error(f"Computed slope values are not constant at point {(seg, x)}: {list_slopes}")
        return list_slopes[0]

    for downstream_slope, downstream_polarity, downstream_distance in downstream_slopes:
        downstream_seg, downstream_x = get_dc_sys_values(downstream_slope, DCSYS.Profil.Seg, DCSYS.Profil.X)
        downstream_slope_value = (get_dc_sys_value(downstream_slope, DCSYS.Profil.Pente)
                                  * (-1 if not downstream_polarity else 1))

        if (seg, x) == (downstream_seg, downstream_x):
            list_slopes.append(downstream_slope_value)
            continue

        for upstream_slope, upstream_polarity, upstream_distance in upstream_slopes:
            upstream_seg, upstream_x = get_dc_sys_values(upstream_slope, DCSYS.Profil.Seg, DCSYS.Profil.X)
            upstream_slope_value = (get_dc_sys_value(upstream_slope, DCSYS.Profil.Pente)
                                    * (-1 if not upstream_polarity else 1))

            if (seg, x) == (upstream_seg, upstream_x):
                list_slopes.append(upstream_slope_value)
                continue

            total_distance = downstream_distance + upstream_distance
            # linear approximation of the slope between two points
            slope_value = ((upstream_slope_value - downstream_slope_value) / total_distance
                           * downstream_distance + downstream_slope_value)
            list_slopes.append(round(slope_value, 9))

    if not all(slope_value == list_slopes[0] for slope_value in list_slopes):
        print_error(f"Computed slope values are not constant at point {(seg, x)}: {list_slopes}")
    return list_slopes[0]


def get_min_and_max_slopes_at_point(seg: str, x: float) -> tuple[float, float]:
    slopes = get_next_slopes(seg, x, downstream=True)
    slopes.extend(get_next_slopes(seg, x, downstream=False))
    slopes_value = [float(get_dc_sys_value(slope, DCSYS.Profil.Pente))
                    * (-1 if not polarity else 1) for slope, polarity, _ in slopes]
    return min(slopes_value), max(slopes_value)


def get_next_slopes(start_seg: str, start_x: float, downstream: bool) -> list[tuple[dict[str, Any], bool, float]]:
    """ Return a list of the first slopes reached in the given downstream direction starting from the given point.
    If a switch is met before reaching a slope, the list will be composed of multiple slopes for each path. """
    slopes = list()

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[str], path_len: float,
                              x: float = None) -> None:
        nonlocal slopes
        slope = _is_slope_defined_on_seg(seg, downstream=inner_downstream, x=x)
        if slope is not False:
            slope_x = get_dc_sys_value(slope, DCSYS.Profil.X)
            final_path_len = path_len - ((get_segment_length(start_seg) - slope_x) if inner_downstream else slope_x)
            slopes.append((slope, inner_downstream == downstream, final_path_len))
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
            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [next_seg],
                                  round(path_len + get_segment_length(next_seg), 3))

    start_path_len = (get_segment_length(start_seg) - start_x) if downstream else start_x
    inner_recurs_next_seg(start_seg, downstream, [start_seg], start_path_len, start_x)
    return slopes


def _is_slope_defined_on_seg(seg: str, downstream: bool = True, x: float = None) -> Union[bool, dict[str, Any]]:
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


def get_min_and_max_slopes_in_zone_limits(zone_limits: list[tuple[str, float, str]],
                                          polarity_ref_seg: str = None) -> tuple[float, float]:
    depol_in_zone = bool(depolarization_in_zone_limits(zone_limits))
    if depol_in_zone:  # if there is a depolarization inside the zone
        if polarity_ref_seg is None:
            print_log(f"There is a depolarization inside zone limits:\n"
                      f"\t{zone_limits}\n"
                      f"\tWe take as reference segment for slope polarity the first limit segment "
                      f"\"{zone_limits[0][0]}\".")
            polarity_ref_seg = zone_limits[0][0]  # take the first limit segment as our reference segment for the slope polarity
        elif not is_seg_in_zone_limits(zone_limits, polarity_ref_seg):
            print_error(f"Polarity reference segment {polarity_ref_seg} is not inside zone limits:\n"
                        f"\t{zone_limits}\n"
                        f"\tWe take as reference segment for slope polarity the first limit segment "
                        f"\"{zone_limits[0][0]}\".")
            polarity_ref_seg = zone_limits[0][0]  # take the first limit segment as our reference segment for the slope polarity

        polarity_dict = {polarity_ref_seg: True}
        checked_limits = set()
        for _ in range(len(zone_limits)):  # we need at max the same number of iterations as of limits
            if checked_limits == set(zone_limits):
                break
            for limit in zone_limits:
                if limit in checked_limits:
                    continue
                seg, _, _ = limit
                if seg in polarity_dict:
                    checked_limits.add(limit)
                    continue
                for ref_seg, ref_polarity in polarity_dict.items():
                    if is_seg_downstream(ref_seg, seg, downstream=True):
                        polarity = is_seg_downstream(seg, ref_seg, downstream=False)
                        if seg not in polarity_dict:
                            polarity_dict[seg] = polarity if ref_polarity else not polarity
                        checked_limits.add(limit)
                        break
                    elif is_seg_downstream(ref_seg, seg, downstream=False):
                        polarity = is_seg_downstream(seg, ref_seg, downstream=True)
                        if seg not in polarity_dict:
                            polarity_dict[seg] = polarity if ref_polarity else not polarity
                        checked_limits.add(limit)
                        break
        if not checked_limits == set(zone_limits):
            print_error(f"Computation of the polarity of the limit segments has failed.")
    else:
        polarity_dict = dict()

    # If there is slope changes inside the zone
    in_slopes = get_objects_in_zone_limits(DCSYS.Profil, zone_limits)
    if in_slopes is None:
        slopes_values = []
    else:
        if not depol_in_zone:
            slopes_values = [float(get_dc_sys_value(slope, DCSYS.Profil.Pente)) for slope in in_slopes]
        else:
            slopes_values = list()
            for slope in in_slopes:
                slope_seg = get_dc_sys_value(slope, DCSYS.Profil.Seg)
                if slope_seg in polarity_dict:
                    continue
                for ref_seg, ref_polarity in polarity_dict.items():
                    if is_seg_downstream(ref_seg, slope_seg, downstream=True):
                        polarity = is_seg_downstream(slope_seg, ref_seg, downstream=False)
                        if slope_seg not in polarity_dict:
                            polarity_dict[slope_seg] = polarity if ref_polarity else not polarity
                        break
                    elif is_seg_downstream(ref_seg, slope_seg, downstream=False):
                        polarity = is_seg_downstream(slope_seg, ref_seg, downstream=True)
                        if slope_seg not in polarity_dict:
                            polarity_dict[slope_seg] = polarity if ref_polarity else not polarity
                        break
                slopes_values.append(float(get_dc_sys_value(slope, DCSYS.Profil.Pente))
                                     * (1 if polarity_dict[slope_seg] else -1))

    # Add the slope computed at each limit
    for limit in zone_limits:
        seg, x, direction = limit
        slope = get_slope_at_point(seg, x)
        if not depol_in_zone:
            slopes_values.append(slope)
        else:
            slopes_values.append(slope * (1 if polarity_dict[seg] else -1))

    return min(slopes_values), max(slopes_values)


def get_min_and_max_slopes_in_zone(obj_type, obj_name: str,
                                   polarity_ref_seg: str = None) -> Optional[tuple[float, float]]:
    zone_limits = get_oriented_limits_of_obj(obj_type, obj_name)
    if zone_limits is None:
        print(f"{get_sh_name(obj_type)} {obj_name} is not a zone object.")
        return None
    return get_min_and_max_slopes_in_zone_limits(zone_limits, polarity_ref_seg)
