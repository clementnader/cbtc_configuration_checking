#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_len_seg(seg: str, seg_dict: dict, seg_cols_name: dict[str, str]) -> float:
    return float(seg_dict[seg][seg_cols_name['G']])


def get_straight_linked_segs(seg: str, seg_dict: dict, seg_cols_name: dict[str, str], upstream: bool = True,
                             depth: int = 10) -> list[str]:

    ref_col = 'H' if upstream else 'J'
    linked_segs = list()
    linked_seg = seg_dict[seg][seg_cols_name[ref_col]] if seg_cols_name[ref_col] in seg_dict[seg] else ""
    cnt = 0
    while linked_seg and cnt < depth:
        cnt += 1
        linked_segs.append(linked_seg)
        linked_seg = seg_dict[linked_seg][seg_cols_name[ref_col]] if seg_cols_name[ref_col] in seg_dict[linked_seg] \
            else ""

    return linked_segs


def get_linked_segs(seg: str, seg_dict: dict, seg_cols_name: dict[str, str], upstream: bool = True) -> list[str]:
    ref_col_1 = 'H' if upstream else 'J'
    ref_col_2 = 'I' if upstream else 'K'
    linked_segs = list()

    linked_seg_1 = seg_dict[seg][seg_cols_name[ref_col_1]] if seg_cols_name[ref_col_1] in seg_dict[seg] else ""
    linked_seg_2 = seg_dict[seg][seg_cols_name[ref_col_2]] if seg_cols_name[ref_col_2] in seg_dict[seg] else ""
    if linked_seg_1:
        linked_segs.append(linked_seg_1)
    if linked_seg_2:
        linked_segs.append(linked_seg_2)

    return linked_segs


def get_path_unidir(seg1, seg2, seg_dict, seg_cols_name, upstream: bool = True, depth: int = 10,
                    recursive_cnt: int = 0):
    if seg2 == seg1:
        return [seg1]
    if recursive_cnt == depth:
        return []
    linked_segs = get_linked_segs(seg1, seg_dict, seg_cols_name, upstream)
    for linked_seg in linked_segs:
        path = get_path_unidir(linked_seg, seg2, seg_dict, seg_cols_name, upstream, depth, recursive_cnt+1)
        if path:
            return [seg1] + path
    return []


def get_straight_dist(seg1, x1, seg2, x2, seg_dict, seg_cols_name, depth: int = 10):
    x1 = float(x1)
    x2 = float(x2)
    seg1, x1 = get_correct_seg_offset(seg1, x1, seg_dict, seg_cols_name)
    seg2, x2 = get_correct_seg_offset(seg2, x2, seg_dict, seg_cols_name)

    if seg1 == seg2:
        return round(abs(x1-x2), 2)

    len_seg1 = get_len_seg(seg1, seg_dict, seg_cols_name)
    len_seg2 = get_len_seg(seg2, seg_dict, seg_cols_name)
    upstream_segs_1 = get_straight_linked_segs(seg1, seg_dict, seg_cols_name, upstream=True, depth=depth)
    downstream_segs_1 = get_straight_linked_segs(seg1, seg_dict, seg_cols_name, upstream=False, depth=depth)
    upstream = seg2 in upstream_segs_1
    downstream = seg2 in downstream_segs_1

    if not upstream and not downstream:
        print(f"cannot calculate distance between ({seg1}, {x1}) and ({seg2}, {x2}):"
              f"no path found between {seg1} and {seg2}")
        return 0.
    elif upstream:
        d = x1
        i = 0
        upstream_seg = upstream_segs_1[i]
        while seg2 != upstream_seg:
            d += get_len_seg(upstream_seg, seg_dict, seg_cols_name)
            i += 1
            upstream_seg = upstream_segs_1[i]
        d += len_seg2 - x2
    else:  # downstream
        d = len_seg1 - x1
        i = 0
        downstream_seg = downstream_segs_1[i]
        while seg2 != downstream_seg:
            d += get_len_seg(downstream_seg, seg_dict, seg_cols_name)
            i += 1
            downstream_seg = downstream_segs_1[i]
        d += x2
    return round(d, 2)


def get_dist(seg1, x1, seg2, x2, seg_dict, seg_cols_name):
    x1 = float(x1)
    x2 = float(x2)
    seg1, x1 = get_correct_seg_offset(seg1, x1, seg_dict, seg_cols_name)
    seg2, x2 = get_correct_seg_offset(seg2, x2, seg_dict, seg_cols_name)

    if seg1 == seg2:
        return round(abs(x1-x2), 2)

    len_seg1 = get_len_seg(seg1, seg_dict, seg_cols_name)
    len_seg2 = get_len_seg(seg2, seg_dict, seg_cols_name)
    upstream_segs = get_path_unidir(seg1, seg2, seg_dict, seg_cols_name, upstream=True)
    downstream_segs = get_path_unidir(seg1, seg2, seg_dict, seg_cols_name, upstream=False)

    if not upstream_segs and not downstream_segs:
        print(f"cannot calculate distance between ({seg1}, {x1}) and ({seg2}, {x2}): "
              f"no path found between {seg1} and {seg2}")
        return 0.
    elif upstream_segs:
        d = x1
        for i, upstream_seg in enumerate(upstream_segs[1:-1]):
            d += get_len_seg(upstream_seg, seg_dict, seg_cols_name)
        d += len_seg2 - x2
    else:  # downstream
        d = len_seg1 - x1
        for i, downstream_seg in enumerate(downstream_segs[1:-1]):
            d += get_len_seg(downstream_seg, seg_dict, seg_cols_name)
        d += x2
    return round(d, 2)


def get_correct_seg_offset(seg, x, seg_dict, seg_cols_name):
    len_seg = get_len_seg(seg, seg_dict, seg_cols_name)
    upstream_segs = get_straight_linked_segs(seg, seg_dict, seg_cols_name, upstream=True)
    downstream_segs = get_straight_linked_segs(seg, seg_dict, seg_cols_name, upstream=False)

    while x > len_seg:
        x -= len_seg
        seg = downstream_segs.pop(0)
        len_seg = get_len_seg(seg, seg_dict, seg_cols_name)

    while x < 0:
        seg = upstream_segs.pop(0)
        len_seg = get_len_seg(seg, seg_dict, seg_cols_name)
        x += len_seg

    return seg, x


def get_sig_dist(sig1, sig2, sig_dict, sig_cols_name, seg_dict, seg_cols_name, depth: int = 10):
    seg1 = sig_dict[sig1][sig_cols_name['C']]
    x1 = float(sig_dict[sig1][sig_cols_name['D']])
    seg2 = sig_dict[sig2][sig_cols_name['C']]
    x2 = float(sig_dict[sig2][sig_cols_name['D']])
    return get_straight_dist(seg1, x1, seg2, x2, seg_dict, seg_cols_name, depth)


def get_tag_dist(tag1, tag2, tag_dict, tag_cols_name, seg_dict, seg_cols_name, depth: int = 10):
    seg1 = tag_dict[tag1][tag_cols_name['D']]
    x1 = float(tag_dict[tag1][tag_cols_name['E']])
    seg2 = tag_dict[tag2][tag_cols_name['D']]
    x2 = float(tag_dict[tag2][tag_cols_name['E']])
    return get_straight_dist(seg1, x1, seg2, x2, seg_dict, seg_cols_name, depth)
