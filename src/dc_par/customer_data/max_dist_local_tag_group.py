#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...dc_sys import *


def max_dist_local_tag_group(in_cbtc: bool = False):
    if in_cbtc:
        tag_dict = get_tags_in_cbtc_ter()
        tag_gr_dict = get_tag_gr_in_cbtc_ter()
    else:
        tag_dict = load_sheet("tag")
        tag_gr_dict = load_sheet("tag_gr")
    nb_tag_gr = len(tag_gr_dict)
    tag_cols_name = get_cols_name("tag")

    dict_max_dist = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    for n, (tag_gr, tag_gr_values) in enumerate(tag_gr_dict.items()):
        print_log(f"\r{progress_bar(n, nb_tag_gr)} processing distances inside local tag group {tag_gr}...", end="")
        tags = [list(limits.values())[0] for limits in tag_gr_values["limits"]]
        for i, tag1 in enumerate(tags):
            seg1 = tag_dict[tag1][tag_cols_name['D']]
            x1 = float(tag_dict[tag1][tag_cols_name['E']])
            for tag2 in tags[i+1:]:
                seg2 = tag_dict[tag2][tag_cols_name['D']]
                x2 = float(tag_dict[tag2][tag_cols_name['E']])
                d = get_dist(seg1, x1, seg2, x2)
                if d is not None:
                    dict_max_dist[f"{tag_gr}::{tag1} to {tag2}"] = d
                else:
                    print_warning(f"Unable to compute interdistance of tag group {tag_gr},"
                                  f"\n no path between {tag1} and {tag2}.")
    print_log(f"\r{progress_bar(nb_tag_gr, nb_tag_gr, end=True)} processing distances between "
              f" inside local tag groups finished.\n")

    dict_max_dist = {x: dict_max_dist[x] for x in sorted(dict_max_dist, key=lambda x: dict_max_dist[x])}
    max_dist = max(tags_values for tags_values in dict_max_dist.values())
    print(f"The maximum distance between two tags inside local tag groups is, {print_in_cbtc(in_cbtc)}:"
          f"\n{max_dist=}"
          f"\n > for: {[tags for tags, tags_values in dict_max_dist.items() if tags_values == max_dist]}\n")
    return dict_max_dist
