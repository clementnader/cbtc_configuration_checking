#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import DCSYS
from ...utils import *
from ...dc_sys import *


def max_dist_local_tag_group(in_cbtc: bool = False):
    if in_cbtc:
        tag_gr_dict = get_tag_gr_in_cbtc_ter()
    else:
        tag_gr_dict = load_sheet(DCSYS.StaticTag_Group)
    tag_dict = load_sheet(DCSYS.Bal)
    nb_tag_gr = len(tag_gr_dict)

    if nb_tag_gr == 0:
        max_dist = 0
        print(f"The maximum distance between two tags inside local tag groups is, {print_in_cbtc(in_cbtc)}:"
              f"\n{max_dist = }"
              f"\n > There is no tag group.\n")
        return {}
    dict_max_dist = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    for n, (tag_gr, tag_gr_value) in enumerate(tag_gr_dict.items()):
        print_log(f"\r{progress_bar(n, nb_tag_gr)} processing distances inside local tag group {tag_gr}...", end="")
        tags = get_dc_sys_value(tag_gr_value, DCSYS.StaticTag_Group.TagList.Tag)
        for i, tag1 in enumerate(tags):
            seg1 = get_dc_sys_value(tag_dict[tag1], DCSYS.Bal.Seg)
            x1 = float(get_dc_sys_value(tag_dict[tag1], DCSYS.Bal.X))
            for tag2 in tags[i+1:]:
                seg2 = get_dc_sys_value(tag_dict[tag2], DCSYS.Bal.Seg)
                x2 = float(get_dc_sys_value(tag_dict[tag2], DCSYS.Bal.X))
                d = get_dist(seg1, x1, seg2, x2)
                if d is not None:
                    dict_max_dist[f"{tag_gr}::{tag1} to {tag2}"] = d
                else:
                    print_warning(f"Unable to compute interdistance of tag group {tag_gr},"
                                  f"\n no path between {tag1} and {tag2}.")
    print_log(f"\r{progress_bar(nb_tag_gr, nb_tag_gr, end=True)} processing distances between "
              f" inside local tag groups finished.\n")

    dict_max_dist = {x: dict_max_dist[x] for x in sorted(dict_max_dist, key=lambda x: dict_max_dist[x])}
    max_dist = max(tags_value for tags_value in dict_max_dist.values())
    print(f"The maximum distance between two tags inside local tag groups is, {print_in_cbtc(in_cbtc)}:"
          f"\n{max_dist = }"
          f"\n > for: {[tags for tags, tags_value in dict_max_dist.items() if tags_value == max_dist]}\n")
    return dict_max_dist
