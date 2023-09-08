#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


def min_dist_between_tags(in_cbtc: bool = False):
    if in_cbtc:
        tag_dict = get_tags_in_cbtc_ter()
    else:
        tag_dict = load_sheet(DCSYS.Bal)
    tag_list = list(tag_dict.keys())
    nb_tags = len(tag_list)

    tags_dist_dict = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, tag1 in enumerate(tag_list):
        print_log(f"\r{progress_bar(i, nb_tags)} processing distances between {tag1} and other tags...", end="")
        seg1 = get_dc_sys_value(tag_dict[tag1], DCSYS.Bal.Seg)
        x1 = float(get_dc_sys_value(tag_dict[tag1], DCSYS.Bal.X))
        for tag2 in tag_list[i+1:]:
            seg2 = get_dc_sys_value(tag_dict[tag2], DCSYS.Bal.Seg)
            x2 = float(get_dc_sys_value(tag_dict[tag2], DCSYS.Bal.X))
            d = get_dist(seg1, x1, seg2, x2)
            if d is not None:
                tags_dist_dict[f"{tag1} and {tag2}"] = d
    print_log(f"\r{progress_bar(nb_tags, nb_tags, end=True)} processing distances between tags finished.\n")

    tags_dist_dict = {x: tags_dist_dict[x] for x in sorted(tags_dist_dict, key=lambda x: tags_dist_dict[x])}
    min_dist = min(tags_value for tags_value in tags_dist_dict.values())
    print(f"The minimal distance between two tags is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_dist = }"
          f"\n > for {[tags for tags, tags_value in tags_dist_dict.items() if tags_value == min_dist]}\n")
    return tags_dist_dict
