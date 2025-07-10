#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from .path_utils import *


__all__ = ["get_dist", "get_dist_downstream", "get_list_of_paths", "get_min_dist_and_list_of_paths",
           "get_smallest_path", "get_path_len", "get_downstream_path", "get_min_path_downstream",
           "get_dist_between_objects", "print_dist_between_objects",
           "is_seg_downstream"]


def is_seg_downstream(start_seg: str, end_seg: str, start_x: float = None, end_x: float = None,
                      downstream: bool = True, without_ring_loopback: bool = True) -> bool:
    if start_x is not None:
        start_x = float(start_x)
    if end_x is not None:
        end_x = float(end_x)

    if start_seg == end_seg:
        if ((start_x is None or end_x is None)
                or (downstream and start_x <= end_x) or (not downstream and start_x >= end_x)):
            return True
        else:
            return False

    ring_conf = ((end_seg in [seg for seg, _ in get_all_downstream_segments(start_seg)])
                 and (end_seg in [seg for seg, _ in get_all_upstream_segments(start_seg)]))
    if not ring_conf:
        return (end_seg in [seg for seg, _ in get_all_downstream_segments(start_seg)] if downstream
                else end_seg in [seg for seg, _ in get_all_upstream_segments(start_seg)])
    # Ring Configuration
    if not without_ring_loopback:
        return True
    # We need to find which path is the smallest
    if start_x is None or end_x is None:
        dist1, _, _ = get_min_path_downstream(start_seg, end_seg, downstream=True)
        dist2, _, _ = get_min_path_downstream(start_seg, end_seg, downstream=False)
    else:
        dist1 = get_dist_downstream(start_seg, start_x, end_seg, end_x, downstream=True)
        dist2 = get_dist_downstream(start_seg, start_x, end_seg, end_x, downstream=False)
    if dist1 is None and dist2 is None:
        print_error(f"Ring configuration: {end_seg=} is at the same time downstream "
                    f"and upstream {start_seg=}."
                    f"But no path has been found in either direction.")
        return True
    if dist1 is None:
        return not downstream
    if dist2 is None:
        return downstream
    if (downstream and dist1 <= dist2) or (not downstream and dist1 >= dist2):
        return True
    else:
        return False


def print_dist_between_objects(obj_type_1, obj_name_1: str, obj_type_2, obj_name_2: str,
                               direction: str = None) -> None:
    type_str_1 = get_sh_name(obj_type_1)
    type_str_2 = get_sh_name(obj_type_2)
    downstream = None if direction is None else direction == Direction.CROISSANT
    d = get_dist_between_objects(obj_type_1, obj_name_1, obj_type_2, obj_name_2, downstream=downstream)
    if d is None:
        print(f"No path found between {type_str_1} {Color.mint_green}{obj_name_1}{Color.reset} "
              f"and {type_str_2} {Color.mint_green}{obj_name_2}{Color.reset}"
              f"{(' in direction ' + Color.yellow + direction + Color.reset) if direction is not None else ''}.")
    else:
        print(f"Distance between {type_str_1} {Color.mint_green}{obj_name_1}{Color.reset} "
              f"and {type_str_2} {Color.mint_green}{obj_name_2}{Color.reset} is {Color.beige}{d}{Color.reset}"
              f"{(' in direction ' + Color.yellow + direction + Color.reset) if direction is not None else ''}.")


def get_dist_between_objects(obj_type_1, obj_name_1: str, obj_type_2, obj_name_2: str,
                             downstream: bool = None, avoid_zero: bool = False) -> Optional[float]:
    loc1 = get_object_position(obj_type_1, obj_name_1)
    loc2 = get_object_position(obj_type_2, obj_name_2)
    if loc1 is None or loc2 is None:
        return None
    if isinstance(loc1, tuple):
        loc1 = [loc1]
    if isinstance(loc2, tuple):
        loc2 = [loc2]
    min_d = None
    for lim1 in loc1:
        seg1, x1 = lim1[0], lim1[1]
        for lim2 in loc2:
            seg2, x2 = lim2[0], lim2[1]
            current_d = get_dist(seg1, x1, seg2, x2, downstream=downstream)
            if current_d is None:
                continue
            if (min_d is None or current_d < min_d) and (avoid_zero is False or current_d != 0):
                min_d = current_d
    return min_d


def get_dist(seg1: str, x1: float, seg2: str, x2: float, verbose: bool = False,
             downstream: bool = None) -> Optional[float]:
    """ Return the distance between (seg1, x1) and (seg2, x2). """
    if downstream is not None:
        return get_dist_downstream(seg1, x1, seg2, x2, downstream)
    x1 = float(x1)
    x2 = float(x2)
    if seg1 == seg2:
        return round(abs(x1-x2), 3)

    if is_seg_downstream(seg1, seg2, downstream=True):  # seg2 is downstream of seg1
        dist = get_dist_downstream(seg1, x1, seg2, x2, downstream=True)
    elif is_seg_downstream(seg1, seg2, downstream=False):  # seg2 is upstream of seg1
        dist = get_dist_downstream(seg1, x1, seg2, x2, downstream=False)
    else:
        if verbose:
            print(f"No path found between {seg1} and {seg2}.")
        return None
    return dist


def get_dist_downstream(seg1: str, x1: Optional[float], seg2: str, x2: Optional[float], downstream: bool
                        ) -> Optional[float]:
    if x1 is not None:
        x1 = float(x1)
    if x2 is not None:
        x2 = float(x2)
    if seg1 == seg2:
        if x1 is None or x2 is None:
            return 0.
        if downstream == (x1 <= x2):
            return round(abs(x1-x2), 3)
        else:
            return None

    dist, _, upstream = get_min_path_downstream(seg1, seg2, downstream=downstream)

    if dist is None:
        return None

    if x1 is None:
        dist -= get_segment_length(seg1)
    else:
        if downstream:  # seg2 is downstream of seg1
            dist -= x1
        else:  # seg2 is upstream of seg1
            dist -= (get_segment_length(seg1) - x1)

    if x2 is None:
        dist -= get_segment_length(seg2)
    else:
        if upstream:  # seg1 is upstream of seg2
            dist -= (get_segment_length(seg2) - x2)
        else:  # seg1 is downstream of seg2
            dist -= x2
    return round(dist, 3)


def get_min_path_downstream(start_seg: str, end_seg: str, downstream: bool
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


def get_list_of_paths(seg1: str, seg2: str, verbose: bool = False) -> list[tuple[bool, list[str]]]:
    """ Return the list of paths between seg1 and seg2. """
    _, _, list_paths, _, _ = get_min_dist_and_list_of_paths(seg1, seg2, verbose=verbose)
    return list_paths


def get_min_dist_and_list_of_paths(seg1: str, seg2: str, max_nb_paths: int = None, verbose: bool = False,
                                   end_upstream: bool = None) -> tuple[Optional[float],
                                                                       list[str],
                                                                       list[tuple[bool, list[str]]],
                                                                       Optional[bool],
                                                                       Optional[bool]]:
    """ Return the list of paths between seg1 and seg2. """
    if is_seg_downstream(seg1, seg2, downstream=True):  # seg2 is downstream of seg1
        dist, min_path, list_paths, upstream = (
            get_downstream_path(seg1, seg2, start_downstream=True,
                                max_nb_paths=max_nb_paths, end_upstream=end_upstream))
        downstream = True
    elif is_seg_downstream(seg1, seg2, downstream=False):  # seg2 is upstream of seg1
        dist, min_path, list_paths, upstream = (
            get_downstream_path(seg1, seg2, start_downstream=False,
                                max_nb_paths=max_nb_paths, end_upstream=end_upstream))
        downstream = False
    else:
        if verbose:
            print(f"No path found between {seg1} and {seg2}")
        return None, [], [], None, None
    return dist, min_path, list_paths, downstream, upstream


def get_downstream_path(start_seg: str, end_seg: str, start_downstream: bool, max_nb_paths: int = None,
                        end_upstream: bool = None) -> tuple[Optional[float],
                                                            list[str],
                                                            list[tuple[bool, list[str]]],
                                                            Optional[bool]]:
    """ Look for the paths between start_seg and end_seg, if end_seg is downstream of start_seg.
    Return the smallest path alongside its length, and the list of paths. """
    list_paths: list[tuple[bool, list[str]]] = list()
    if ((start_downstream and end_seg not in [seg for seg, _ in get_all_downstream_segments(start_seg)])
            or (not start_downstream and end_seg not in [seg for seg, _ in get_all_upstream_segments(start_seg)])):
        return None, [], [], None

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[str]):
        nonlocal list_paths
        if seg == end_seg:
            list_paths.append((upstream, path))
            return
        if (seg, not inner_downstream) not in accessible_segs_from_end:  # to optimize:
            # if we reach a segment not accessible from the end segment in the other direction, we can stop,
            # this path will not lead to the end segment
            return
        if max_nb_paths is not None and len(list_paths) > max_nb_paths:
            return
        for next_seg in get_linked_segments(seg, inner_downstream):
            if next_seg in path:  # a whole loop has been made
                continue
            if is_segment_depolarized(next_seg) and seg in get_associated_depolarization(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [next_seg])

    for upstream, accessible_segs_from_end in get_upstream_segs_according_to_direction(end_seg, start_seg,
                                                                                       start_downstream):
        if end_upstream is not None and upstream != end_upstream:
            continue
        inner_recurs_next_seg(start_seg, start_downstream, [start_seg])

    if not list_paths:
        return None, [], [], None
    if max_nb_paths is not None and len(list_paths) > max_nb_paths:
        return None, [], [], None
    min_len, min_path, upstream = get_smallest_path(list_paths)
    return round(min_len, 3), min_path, list_paths, upstream


def get_upstream_segs_according_to_direction(end_seg: str, start_seg: str, downstream: bool
                                             ) -> list[tuple[bool, set[tuple[str, bool]]]]:
    if downstream:
        upstream_list = [upstream for seg, upstream in get_all_downstream_segments(start_seg) if seg == end_seg]
    else:
        upstream_list = [upstream for seg, upstream in get_all_upstream_segments(start_seg) if seg == end_seg]

    list_of_lists_of_accessible_segs = list()
    for upstream in upstream_list:
        if upstream:  # even number of depol between the segments
            accessible_segs_from_end = get_all_upstream_segments(end_seg)
        else:  # odd number of depol between the segments
            accessible_segs_from_end = get_all_downstream_segments(end_seg)
        list_of_lists_of_accessible_segs.append((upstream, accessible_segs_from_end))
    return list_of_lists_of_accessible_segs


def get_smallest_path(list_paths: list[tuple[bool, list[str]]]) -> tuple[float, list[str], bool]:
    """ Return the smallest path along its length,
    if there are multiple smallest paths with the same length, compare the number of segments. """
    list_paths_length = [get_path_len(path) for _, path in list_paths]
    min_len = min(list_paths_length)
    list_min_paths = [path for path, path_len in zip(list_paths, list_paths_length) if path_len == min_len]
    if len(list_min_paths) == 1:
        upstream, path = list_min_paths[0]
        return min_len, path, upstream
    # If various paths have the same length, we return one with the smallest number of segments.
    min_nb_seg = min(len(path) for _, path in list_min_paths)
    list_min_paths = [(upstream, path) for upstream, path in list_min_paths if len(path) == min_nb_seg]
    upstream, path = list_min_paths[0]
    return min_len, path, upstream


def get_path_len(path: list[str]) -> float:
    """ Return the length of a path: the sum of the segments lengths. """
    return round(sum([get_segment_length(seg) for seg in path]), 3)
