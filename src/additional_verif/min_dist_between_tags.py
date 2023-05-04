#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys import *


def min_dist_between_tags(in_cbtc: bool = False):
    if in_cbtc:
        tag_dict = get_tags_in_cbtc_ter()
    else:
        tag_dict = load_sheet("tag")
    tag_cols_name = get_cols_name("tag")
    tag_list = list(tag_dict.keys())
    nb_tags = len(tag_list)

    tags_dist_dict = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, tag1 in enumerate(tag_list):
        print_log(f"\r{progress_bar(i, nb_tags)} processing distances between {tag1} and other tags...", end="")
        seg1 = tag_dict[tag1][tag_cols_name['D']]
        x1 = float(tag_dict[tag1][tag_cols_name['E']])
        for tag2 in tag_list[i+1:]:
            seg2 = tag_dict[tag2][tag_cols_name['D']]
            x2 = float(tag_dict[tag2][tag_cols_name['E']])
            d = get_dist(seg1, x1, seg2, x2)
            if d is not None:
                tags_dist_dict[f"{tag1} and {tag2}"] = d
    print_log(f"\r{progress_bar(nb_tags, nb_tags, end=True)} processing distances between tags finished.\n")

    tags_dist_dict = {x: tags_dist_dict[x] for x in sorted(tags_dist_dict, key=lambda x: tags_dist_dict[x])[:30]}
    min_dist = min(tags_values for tags_values in tags_dist_dict.values())
    print(f"The minimal distance between two tags is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_dist=}"
          f"\n > for {[tags for tags, tags_values in tags_dist_dict.items() if tags_values == min_dist]}\n")
    return tags_dist_dict
