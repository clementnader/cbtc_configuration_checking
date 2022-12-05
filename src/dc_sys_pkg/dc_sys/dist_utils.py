#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .seg_utils import get_len_seg, get_linked_segs


def get_dist(seg1, x1, seg2, x2, seg_dict: dict, seg_cols_name: dict[str, str]):
    """ Return the distance between (seg1, x1) and (seg2, x2). """
    x1 = float(x1)
    x2 = float(x2)
    if seg1 == seg2:
        return abs(x1-x2)
    dist, _, list_paths = get_downstream_path(seg1, seg2, seg_dict, seg_cols_name)
    if list_paths:
        downstream = True
    else:
        dist, _, list_paths = get_downstream_path(seg2, seg1, seg_dict, seg_cols_name)
        if list_paths:
            downstream = False
        else:
            print(f"No path found between {seg1} and {seg2}")
            return 0
    if downstream:  # 1 -> 2
        dist -= x1 + (get_len_seg(seg2, seg_dict, seg_cols_name) - x2)
    else:  # 2 -> 1
        dist -= x2 + (get_len_seg(seg1, seg_dict, seg_cols_name) - x1)
    return dist


def get_list_of_paths(seg1, seg2, seg_dict: dict, seg_cols_name: dict[str, str]):
    """ Return the list of paths between seg1 and seg2. """
    _, _, list_paths = get_downstream_path(seg1, seg2, seg_dict, seg_cols_name)
    if not list_paths:
        _, _, list_paths = get_downstream_path(seg2, seg1, seg_dict, seg_cols_name)
        if not list_paths:
            print(f"No path found between {seg1} and {seg2}")
            return []
    return list_paths


def get_downstream_path(start_seg, end_seg, seg_dict: dict, seg_cols_name: dict[str, str])\
        -> (float, list[str], list[list[str]]):
    """ Look for the paths between start_seg and end_seg, if end_seg is downstream of start_seg.
    Return the smallest path alongside its length, and the list of paths. """
    list_paths = list()

    def inner_recurs_next_seg(seg, path):
        nonlocal list_paths
        if seg == end_seg:
            list_paths.append(path)
            return
        for next_seg in get_linked_segs(seg, seg_dict=seg_dict, seg_cols_name=seg_cols_name):
            if next_seg:
                inner_recurs_next_seg(next_seg, path + [next_seg])

    inner_recurs_next_seg(start_seg, [start_seg])
    if not list_paths:
        return 0, [], []
    min_len, min_path = get_smallest_path(list_paths, seg_dict, seg_cols_name)
    return min_len, min_path, list_paths


def get_smallest_path(list_paths: list[list[str]], seg_dict: dict, seg_cols_name: dict[str, str]) \
        -> (float, list[str]):
    """ Return the smallest path along its length,
    if there are multiple smallest paths with the same length, compare the number of segments. """
    list_paths_dist = list()
    for path in list_paths:
        list_paths_dist.append(get_path_len(path, seg_dict, seg_cols_name))
    min_len = min(list_paths_dist)
    list_min_paths = [path for i, path in enumerate(list_paths) if list_paths_dist[i] == min_len]
    if len(list_min_paths) == 1:
        return min_len, list_min_paths[0]
    min_nb_seg = min([len(path) for path in list_min_paths])
    list_min_paths = [path for path in list_min_paths if len(path) == min_nb_seg]
    return min_len, list_min_paths[0]


def get_path_len(path: list[str], seg_dict: dict, seg_cols_name: dict[str, str]) -> float:
    """ Return the length of a path: the sum of the segments lengths. """
    path_len = 0
    for seg in path:
        path_len += get_len_seg(seg, seg_dict, seg_cols_name)
    return path_len


def test():
    start = 3
    end = 31
    print(f"Computing smallest path between {start} and {end}:")
    print(get_dist(end, 10, start, 0, segs_dict, segs_cols_name))


segs_cols_name = {'G': "len", 'J': "n1", 'K': "n2"}

segs_dict = {
    1: {"len": 10, "n1": 3},
    2: {"len": 10, "n1": 3},
    3: {"len": 10, "n1": 4, "n2": 5},
    4: {"len": 10, "n1": 6},
    5: {"len": 10, "n1": 18, "n2": 32},
    6: {"len": 10, "n1": 7},
    7: {"len": 10, "n1": 8, "n2": 21},
    8: {"len": 10, "n1": 9},
    9: {"len": 10, "n1": 10},
    10: {"len": 10, "n1": 11},
    11: {"len": 10, "n1": 12},
    12: {"len": 10, "n1": 13},
    13: {"len": 10, "n1": 14, "n2": 16},
    14: {"len": 10, "n1": 15},
    15: {"len": 10, },
    16: {"len": 10, "n1": 17},
    17: {"len": 10, },
    18: {"len": 5, "n1": 118},
    118: {"len": 5, "n1": 19},
    19: {"len": 10, "n1": 20},
    20: {"len": 10, "n1": 22},
    21: {"len": 10, "n1": 22},
    22: {"len": 10, "n1": 23},
    23: {"len": 10, "n1": 24},
    24: {"len": 10, "n1": 25, "n2": 26},
    25: {"len": 10, "n1": 12},
    26: {"len": 10, "n1": 27},
    27: {"len": 10, "n1": 28, "n2": 30},
    28: {"len": 10, "n1": 29},
    29: {"len": 10, },
    30: {"len": 10, "n1": 31},
    31: {"len": 10, },
    32: {"len": 10, "n1": 33},
    33: {"len": 10, "n1": 34},
    34: {"len": 10, "n1": 20},
}
