#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .path_utils import get_all_upstream_segments, get_all_downstream_segments
from .segments_utils import get_len_seg, get_linked_segs, is_seg_depolarized, get_associated_depol


__all__ = ["get_dist", "get_dist_downstream", "get_list_of_paths", "get_min_dist_and_list_of_paths",
           "get_smallest_path", "get_path_len", "get_downstream_path", "get_min_path_downstream",
           "get_virtual_seg_ordered_extremities",
           "is_point_between", "is_seg_downstream", "are_segs_linked"]


def are_segs_linked(seg1: str, seg2: str, x1: float = None, x2: float = None) -> bool:
    return is_seg_downstream(seg1, seg2, x1, x2, downstream=True) or \
           is_seg_downstream(seg1, seg2, x1, x2, downstream=False)


def is_seg_downstream(start_seg: str, end_seg: str, start_x: float = None, end_x: float = None,
                      downstream: bool = True, without_ring_loopback: bool = True) -> bool:
    if start_x is not None:
        start_x = float(start_x)
    if end_x is not None:
        end_x = float(end_x)

    if start_seg == end_seg:
        if (start_x is None or end_x is None) or (downstream and start_x <= end_x) or \
                (not downstream and start_x >= end_x):
            return True
        else:
            return False

    ring_conf = (end_seg in [seg for seg, _ in get_all_downstream_segments(start_seg)]) and \
                (end_seg in [seg for seg, _ in get_all_upstream_segments(start_seg)])
    if not ring_conf:
        return end_seg in [seg for seg, _ in get_all_downstream_segments(start_seg)] if downstream \
            else end_seg in [seg for seg, _ in get_all_upstream_segments(start_seg)]
    # Ring Configuration
    if not without_ring_loopback:
        print_warning(f"Ring configuration: {end_seg=} is at the same time downstream "
                      f"and upstream {start_seg=}.")
        return True
    # We need to find which path is the smallest
    dist1, _, _, _ = get_downstream_path(start_seg, end_seg, start_downstream=True)
    dist2, _, _, _ = get_downstream_path(start_seg, end_seg, start_downstream=False)
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


def get_dist(seg1: str, x1: float, seg2: str, x2: float, verbose: bool = False) -> Optional[float]:
    """ Return the distance between (seg1, x1) and (seg2, x2). """
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


def get_dist_downstream(seg1: str, x1: float, seg2: str, x2: float, downstream: bool) -> Optional[float]:
    x1 = float(x1)
    x2 = float(x2)
    if seg1 == seg2:
        if downstream == (x1 <= x2):
            return round(abs(x1-x2), 3)
        else:
            return None

    # dist, _, _, upstream = get_downstream_path(seg1, seg2, downstream=downstream)
    dist, _, upstream = get_min_path_downstream(seg1, seg2, downstream=downstream)

    if dist is None:
        return None

    if downstream:  # seg2 is downstream of seg1
        dist -= x1
    else:  # seg2 is upstream of seg1
        dist -= (get_len_seg(seg1) - x1)
    if upstream:  # seg1 is upstream of seg2
        dist -= (get_len_seg(seg2) - x2)
    else:  # seg1 is downstream of seg2
        dist -= x2
    return round(dist, 3)


def get_min_path_downstream(start_seg: str, end_seg: str, downstream: bool
                            ) -> tuple[Optional[float], list[str], Optional[bool]]:
    min_len = -1
    min_path = []
    associated_upstream = None
    if (downstream and end_seg not in [seg for seg, _ in get_all_downstream_segments(start_seg)]) or \
            (not downstream and end_seg not in [seg for seg, _ in get_all_upstream_segments(start_seg)]):
        return None, [], None

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[str], path_len: float):
        nonlocal min_len, min_path, associated_upstream
        if min_len != -1 and path_len >= min_len:  # we reach a larger distance, we can stop
            return
        if seg == end_seg:
            min_len = path_len
            min_path = path
            associated_upstream = upstream
            return
        if (seg, not inner_downstream) not in accessible_segs_from_end:  # to optimize:
            # if we reach a segment not accessible from the end segment in the other direction, we can stop,
            # this path will not lead to the end segment
            return
        for next_seg in get_linked_segs(seg, inner_downstream):
            if next_seg in path:  # for ring
                continue
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [next_seg],
                                  round(path_len + get_len_seg(next_seg), 3))

    for upstream, accessible_segs_from_end in get_upstream_segs_according_to_direction(end_seg, start_seg, downstream):
        inner_recurs_next_seg(start_seg, downstream, [start_seg], get_len_seg(start_seg))

    if min_len is None:
        print_warning(f"{end_seg=} is in the accessible segments of {start_seg=} in direction "
                      f"{'downstream' if downstream else 'upstream'}, but no path was found.")
        return None, [], None
    return min_len, min_path, associated_upstream


def get_list_of_paths(seg1: str, seg2: str, verbose: bool = False):
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
        dist, min_path, list_paths, upstream = \
            get_downstream_path(seg1, seg2, start_downstream=True,
                                max_nb_paths=max_nb_paths, end_upstream=end_upstream)
        downstream = True
    elif is_seg_downstream(seg1, seg2, downstream=False):  # seg2 is upstream of seg1
        dist, min_path, list_paths, upstream = \
            get_downstream_path(seg1, seg2, start_downstream=False,
                                max_nb_paths=max_nb_paths, end_upstream=end_upstream)
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
    if (start_downstream and end_seg not in [seg for seg, _ in get_all_downstream_segments(start_seg)]) or \
            (not start_downstream and end_seg not in [seg for seg, _ in get_all_upstream_segments(start_seg)]):
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
        for next_seg in get_linked_segs(seg, inner_downstream):
            if next_seg in path:  # for ring
                continue
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
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
        if end_upstream is None:  # if we specify a direction to arrive to the end segment, we may have no path found
            print_warning(f"{end_seg=} is in the accessible segments of {start_seg=} in direction "
                          f"{'downstream' if start_downstream else 'upstream'}, but no path was found.")
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
    return round(sum([get_len_seg(seg) for seg in path]), 3)


def get_virtual_seg_ordered_extremities(seg1: str, x1: float, seg2: str, x2: float):
    if seg1 == seg2 and x1 == x2:
        return seg1, x1, seg2, x2
    else:
        if is_seg_downstream(seg1, seg2, x1, x2, downstream=True):
            return seg1, x1, seg2, x2
        elif is_seg_downstream(seg1, seg2, x1, x2, downstream=False):
            return seg2, x2, seg1, x1
        else:
            return None, None, None, None


def is_point_between(seg: str, x: float, limit_seg_1: str, limit_x_1: float, limit_seg_2: str, limit_x_2: float,
                     extra_limit=None):
    if limit_seg_1 is None:
        return False

    limit_seg_1, limit_x_1, limit_seg_2, limit_x_2 = \
        get_virtual_seg_ordered_extremities(limit_seg_1, limit_x_1, limit_seg_2, limit_x_2)

    if limit_seg_1 == limit_seg_2:
        if seg != limit_seg_1:
            return False
        if float(limit_x_1) <= float(x) <= float(limit_x_2):
            return True
        return False

    if seg == limit_seg_1:
        if float(x) >= float(limit_x_1):
            return True
        else:
            return False
    if seg == limit_seg_2:
        if float(x) <= float(limit_x_2):
            return True
        else:
            return False
    if extra_limit is not None and seg == extra_limit[0]:
        return None

    def inner_recurs_seg(current_seg: str, end_seg: str):
        next_segs = get_linked_segs(current_seg, downstream=True)
        for next_seg in next_segs:
            if next_seg == end_seg:
                return True
            if not (next_seg == limit_seg_2 or (extra_limit is not None and next_seg == extra_limit[0])):
                return inner_recurs_seg(next_seg, end_seg)
        return False

    return inner_recurs_seg(limit_seg_1, seg)