#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys_pkg import *


def max_dist_local_tag_group():
    tag_dict = load_sheet("tag")
    tag_cols_name = get_cols_name("tag")

    tag_gr_dict = load_sheet("tag_gr")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    dict_max_dist = dict()

    for tag_gr in tag_gr_dict:
        tag_list = [list(limits.values())[0] for limits in tag_gr_dict[tag_gr]["limits"]]
        for i, tag1 in enumerate(tag_list):
            seg1 = tag_dict[tag1][tag_cols_name['D']]
            x1 = float(tag_dict[tag1][tag_cols_name['E']])
            for tag2 in tag_list[i+1:]:
                seg2 = tag_dict[tag2][tag_cols_name['D']]
                x2 = float(tag_dict[tag2][tag_cols_name['E']])
                d = get_dist(seg1, x1, seg2, x2, seg_dict, seg_cols_name)
                if d:
                    dict_max_dist[f"{tag_gr}::{tag1} to {tag2}"] = {"d": d}

    max_dist = max([dict_max_dist[tags]['d'] for tags in dict_max_dist])
    print(f"max_dist is {max_dist}"
          f"\nfor: {[tags for tags in dict_max_dist if dict_max_dist[tags]['d'] == max_dist]}")

    return dict_max_dist
