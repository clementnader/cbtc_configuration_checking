#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_sys import *


def min_dist_between_tags():
    tag_dict = load_sheet("tag")
    tag_cols_name = get_cols_name("tag")
    tag_list = list(tag_dict.keys())

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    tags_dist_dict = dict()
    for i, tag1 in enumerate(tag_list):
        seg1 = tag_dict[tag1][tag_cols_name['D']]
        x1 = tag_dict[tag1][tag_cols_name['E']]
        for tag2 in tag_list[i+1:]:
            seg2 = tag_dict[tag2][tag_cols_name['D']]
            x2 = tag_dict[tag2][tag_cols_name['E']]
            d = get_dist(seg1, x1, seg2, x2, seg_dict, seg_cols_name, verbose=False)
            if d:
                tags_dist_dict[f"{tag1} and {tag2}"] = d

    min_dist = min(tags_dist_dict[tags] for tags in tags_dist_dict)
    print(f"{min_dist=}"
          f"\nfor {[tags for tags in tags_dist_dict if tags_dist_dict[tags] == min_dist]}")
    return tags_dist_dict
