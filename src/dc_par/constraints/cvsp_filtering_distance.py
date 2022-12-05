#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys_pkg import *
from dc_sys_checking.src.dc_sys_pkg.seg_utils import *


def min_dist_between_platform_osp_and_end_of_next_platform():
    wb = load_wb()
    sh_plt = wb.sheet_by_name("Quai")
    plt_dict = get_dict(sh_plt, fixed_cols_ref=['I', 'J', 'Q', 'R', 'Y', 'AA', 'AB', 'AD', 'AI', 'AK', 'AL', 'AN',
                                                'AS', 'AU', 'AV', 'AX'])
    plt_cols_name = get_cols_name(sh_plt, cols_ref=['I', 'J', 'Q', 'R', 'Y', 'AA', 'AB', 'AD', 'AI', 'AK', 'AL', 'AN',
                                                    'AS', 'AU', 'AV', 'AX'])

    sh_seg = wb.sheet_by_name("Seg")
    seg_dict = get_dict(sh_seg, fixed_cols_ref=['G', 'H', 'I', 'J', 'K'])
    seg_cols_name = get_cols_name(sh_seg, cols_ref=['G', 'H', 'I', 'J', 'K'])

    dict_min_dist = dict()

    osp_name_cols = ['Y', 'AI', 'AS']
    osp_seg_cols = ['AA', 'AK', 'AU']
    osp_x_cols = ['AB', 'AL', 'AV']
    osp_direction_cols = ['AD', 'AN', 'AX']

    for plt in plt_dict:
        for name_col, seg_col, x_col, direction_col in zip(osp_name_cols, osp_seg_cols, osp_x_cols, osp_direction_cols):
            osp_name = plt_dict[plt][plt_cols_name[name_col]] if plt_cols_name[name_col] in plt_dict[plt] else ""
            if osp_name:  # if OSP exists
                osp_seg = plt_dict[plt][plt_cols_name[seg_col]]
                osp_x = plt_dict[plt][plt_cols_name[x_col]]
                osp_direction = plt_dict[plt][plt_cols_name[direction_col]]
                if osp_direction in ["DECROISSANT", "DOUBLE_SENS"]:
                    key, value = get_dist_osp_next_plt(osp_name, osp_seg, osp_x, osp_direction, plt,
                                                       plt_dict, plt_cols_name, seg_dict, seg_cols_name, upstream=True)
                    if key:
                        dict_min_dist[key] = value

                if osp_direction in ["CROISSANT", "DOUBLE_SENS"]:
                    key, value = get_dist_osp_next_plt(osp_name, osp_seg, osp_x, osp_direction, plt,
                                                       plt_dict, plt_cols_name, seg_dict, seg_cols_name, upstream=False)
                    if key:
                        dict_min_dist[key] = value

    min_dist = min([dict_min_dist[osp_n_dir]["d"] for osp_n_dir in dict_min_dist])
    res_list = [{osp_n_dir: dict_min_dist[osp_n_dir]} for osp_n_dir in dict_min_dist
                if dict_min_dist[osp_n_dir]['d'] == min_dist]
    print(f"min_dist is {min_dist}"
          f"\nfor: {res_list}")
    return plt_dict


def get_dist_osp_next_plt(osp_name, osp_seg, osp_x, osp_direction, osp_plt, plt_dict, plt_cols_name,
                          seg_dict, seg_cols_name, upstream: bool):

    closest_plt, linked_segs = get_next_platform(osp_seg, osp_x, osp_plt, plt_dict, plt_cols_name,
                                                 seg_dict, seg_cols_name, upstream=upstream)
    upstream_str = "upstream" if upstream else "downstream"

    if closest_plt == "End of Track":
        print(f"{osp_name}_{upstream_str} of {osp_plt} in {osp_direction=} is the last before End of Track")
        return None, None
    else:
        plt_seg = plt_dict[closest_plt][plt_cols_name['Q']]
        plt_x = plt_dict[closest_plt][plt_cols_name['R']]

        d = get_dist_with_path(osp_seg, osp_x, plt_seg, plt_x, linked_segs, seg_dict, seg_cols_name,
                               upstream=upstream)
        return f"{osp_name}_{upstream_str}", {"origin_plt": osp_plt, "osp_direction": osp_direction,
                                              "closest_plt": closest_plt, "d": d}


def get_next_platform(osp_seg, osp_x, osp_plt, plt_dict, plt_cols_name, seg_dict: dict, seg_cols_name: dict[str, str],
                      upstream: bool = True):

    ref_col = 'H' if upstream else 'J'  # TODO: change to use both linked segments
    linked_segs = list()
    linked_seg = osp_seg
    closest_plt = None
    while linked_seg and not closest_plt:
        linked_segs.append(linked_seg)
        closest_plt = get_closest_platform_on_same_seg(linked_seg, osp_seg, osp_x, osp_plt,
                                                       plt_dict, plt_cols_name, upstream=upstream)
        if not closest_plt:
            linked_seg = seg_dict[linked_seg][seg_cols_name[ref_col]] \
                if seg_cols_name[ref_col] in seg_dict[linked_seg] else ""

    if not closest_plt:  # no more linked_seg
        return "End of Track", None

    return closest_plt, linked_segs


def get_closest_platform_on_same_seg(seg, osp_seg, osp_x, osp_plt, plt_dict, plt_cols_name, upstream: bool = True):
    close_plt_dict = dict()
    for plt in plt_dict:
        if plt != osp_plt:
            if upstream:
                plt_seg = plt_dict[plt][plt_cols_name['Q']]  # closest end will be limit 2
                plt_x = plt_dict[plt][plt_cols_name['R']]
            else:
                plt_seg = plt_dict[plt][plt_cols_name['I']]  # closest end will be limit 1
                plt_x = plt_dict[plt][plt_cols_name['J']]
            if seg == plt_seg:
                close_plt_dict[plt] = {"seg": plt_seg, "x": plt_x}
    if not close_plt_dict:
        return None
    if seg == osp_seg:
        correct_plt_dict = dict()
        for plt in close_plt_dict:
            if upstream and float(close_plt_dict[plt]["x"]) > float(osp_x):  # the OSP is in the platform
                pass
            elif not upstream and float(close_plt_dict[plt]["x"]) < float(osp_x):  # the OSP is in the platform
                pass
            else:
                correct_plt_dict[plt] = close_plt_dict[plt]
        close_plt_dict = correct_plt_dict
        if not close_plt_dict:
            return None
    if len(close_plt_dict) > 1:
        print(f"Multiple platforms are on the same segment {close_plt_dict=}")
        close_plt_dict = sort_x_dict(close_plt_dict, reverse=upstream)
    return list(close_plt_dict.keys())[0]


def sort_x_dict(in_dict, reverse: bool = False):
    sorted_list = sorted(in_dict, key=lambda a: float(in_dict[a]["x"]), reverse=reverse)
    return {key: {"x": in_dict[key]["x"]} for key in sorted_list}


def get_platform_segs(plt_seg1, plt_seg2, seg_dict: dict, seg_cols_name: dict[str, str]):
    if plt_seg1 == plt_seg2:
        return [plt_seg1]
    upstream_seg = seg_dict[plt_seg1][seg_cols_name['H']] if seg_cols_name['H'] in seg_dict[plt_seg1] else ""
    downstream_seg = seg_dict[plt_seg1][seg_cols_name['J']] if seg_cols_name['J'] in seg_dict[plt_seg1] else ""
    list_upstream_segs = [upstream_seg]
    list_downstream_segs = [downstream_seg]
    while plt_seg2 not in [upstream_seg, downstream_seg]:
        if upstream_seg:
            upstream_seg = seg_dict[upstream_seg][seg_cols_name['H']] \
                if seg_cols_name['H'] in seg_dict[upstream_seg] else ""
        if downstream_seg:
            downstream_seg = seg_dict[downstream_seg][seg_cols_name['J']] \
                if seg_cols_name['J'] in seg_dict[downstream_seg] else ""
        if not upstream_seg and not downstream_seg:
            print(f"No path found to rejoin both ends of the platform"
                  f"\n{plt_seg1=}, {plt_seg2=}")
            return []
        list_upstream_segs.append(upstream_seg)
        list_downstream_segs.append(downstream_seg)
    if plt_seg2 == upstream_seg:
        return list_upstream_segs[::-1] + [plt_seg1]
    elif plt_seg2 == downstream_seg:
        return [plt_seg1] + list_downstream_segs


def get_dist_with_path(seg1, x1, seg2, x2, linked_segs, seg_dict, seg_cols_name, upstream: bool):
    x1 = float(x1)
    x2 = float(x2)

    if seg1 == seg2:
        return round(abs(x1-x2), 2)

    len_seg1 = get_len_seg(seg1, seg_dict, seg_cols_name)
    len_seg2 = get_len_seg(seg2, seg_dict, seg_cols_name)

    if upstream:
        d = x1
        for upstream_seg in linked_segs[1:-1]:
            d += get_len_seg(upstream_seg, seg_dict, seg_cols_name)
        d += len_seg2 - x2
    else:  # downstream
        d = len_seg1 - x1
        for downstream_seg in linked_segs[1:-1]:
            d += get_len_seg(downstream_seg, seg_dict, seg_cols_name)
        d += x2
    return round(d, 2)
