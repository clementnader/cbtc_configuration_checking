#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .path_utils import get_all_upstream_segs, get_all_downstream_segs
from .segments_utils import get_len_seg, get_linked_segs, is_seg_depolarized, get_associated_depol


def get_dist_downstream(seg1, x1, seg2, x2):
    """ Return the distance between (seg1, x1) and (seg2, x2) if 2 is downstream of 1. """
    if seg1 is None or x1 is None or seg2 is None or x2 is None:
        return None
    x1 = float(x1)
    x2 = float(x2)
    if seg1 == seg2:
        if x1 > x2:  # 2 is not downstream of 1
            return None
        return round(x2-x1, 3)
    if seg2 not in get_all_downstream_segs(seg1):  # seg2 is not downstream of seg1
        return None
    dist, _, _ = get_downstream_path(seg1, seg2)
    dist -= x1 + (get_len_seg(seg2) - x2)
    return round(dist, 3)


def get_dist(seg1, x1, seg2, x2, verbose: bool = False):
    """ Return the distance between (seg1, x1) and (seg2, x2). """
    x1 = float(x1)
    x2 = float(x2)
    if seg1 == seg2:
        return round(abs(x1-x2), 3)

    dist, _, _ = get_min_dist_and_list_of_paths(seg1, seg2, verbose=verbose)
    if dist is None:
        return None

    if seg2 in get_all_downstream_segs(seg1):  # seg2 is downstream of seg1
        dist -= x1 + (get_len_seg(seg2) - x2)
    else:
        dist -= x2 + (get_len_seg(seg1) - x1)
    return round(dist, 3)


def get_list_of_paths(seg1, seg2, verbose: bool = False):
    """ Return the list of paths between seg1 and seg2. """
    _, _, list_paths = get_min_dist_and_list_of_paths(seg1, seg2, verbose=verbose)
    return list_paths


def get_min_dist_and_list_of_paths(seg1, seg2, max_nb_paths: int = None, verbose: bool = False):
    """ Return the list of paths between seg1 and seg2. """
    if seg2 in get_all_downstream_segs(seg1):  # seg2 is downstream of seg1
        pass
    elif seg2 in get_all_upstream_segs(seg1):  # seg2 is upstream of seg1,
        # switch seg1 and seg2 to have seg2 downstream of seg1
        seg1, seg2 = seg2, seg1
    else:
        if verbose:
            print(f"No path found between {seg1} and {seg2}")
        return None, [], []
    dist, min_path, list_paths = get_downstream_path(seg1, seg2, max_nb_paths)
    return dist, min_path, list_paths


def get_downstream_path(start_seg, end_seg, max_nb_paths: int = None) -> (float, list[str], list[list[str]]):
    """ Look for the paths between start_seg and end_seg, if end_seg is downstream of start_seg.
    Return the smallest path alongside its length, and the list of paths. """
    list_paths = list()
    accessible_segs = get_all_upstream_segs(end_seg)

    def inner_recurs_next_seg(seg, path, downstream: bool = True):
        nonlocal list_paths
        if seg == end_seg:
            list_paths.append(path)
            return
        if seg not in accessible_segs:
            return
        if max_nb_paths is not None and len(list_paths) > max_nb_paths:
            return
        for next_seg in get_linked_segs(seg, downstream):
            if next_seg in path:  # for ring
                return
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                downstream = not downstream
            inner_recurs_next_seg(next_seg, path + [next_seg], downstream)

    inner_recurs_next_seg(start_seg, [start_seg])
    if not list_paths:
        return None, [], []
    if max_nb_paths is not None and len(list_paths) > max_nb_paths:
        return None, [], []
    min_len, min_path = get_smallest_path(list_paths)
    return min_len, min_path, list_paths


def get_smallest_path(list_paths: list[list[str]]) -> (float, list[str]):
    """ Return the smallest path along its length,
    if there are multiple smallest paths with the same length, compare the number of segments. """
    list_paths_dist = [get_path_len(path) for path in list_paths]
    min_len = min(list_paths_dist)
    list_min_paths = [path for path, path_len in zip(list_paths, list_paths_dist) if path_len == min_len]
    if len(list_min_paths) == 1:
        return min_len, list_min_paths[0]
    min_nb_seg = min(len(path) for path in list_min_paths)
    list_min_paths = [path for path in list_min_paths if len(path) == min_nb_seg]
    return min_len, list_min_paths[0]


def get_path_len(path: list[str]) -> float:
    """ Return the length of a path: the sum of the segments lengths. """
    return sum([get_len_seg(seg) for seg in path])
