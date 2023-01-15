#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *
from ...colors_pkg import *


def max_dist_local_tag_group(in_cbtc: bool = True):
    if in_cbtc:
        tag_dict = get_tags_in_cbtc_ter()
        tag_gr_dict = get_tag_gr_in_cbtc_ter()
    else:
        tag_dict = load_sheet("tag")
        tag_gr_dict = load_sheet("tag_gr")
    tag_cols_name = get_cols_name("tag")

    dict_max_dist = dict()
    for n, (tag_gr, tag_gr_values) in enumerate(tag_gr_dict.items()):
        tags = [list(limits.values())[0] for limits in tag_gr_values["limits"]]
        for i, tag1 in enumerate(tags):
            seg1 = tag_dict[tag1][tag_cols_name['D']]
            x1 = float(tag_dict[tag1][tag_cols_name['E']])
            for tag2 in tags[i+1:]:
                seg2 = tag_dict[tag2][tag_cols_name['D']]
                x2 = float(tag_dict[tag2][tag_cols_name['E']])
                d = get_dist(seg1, x1, seg2, x2)
                if d is not None:
                    dict_max_dist[f"{tag_gr}::{tag1} to {tag2}"] = {"d": d}
                else:
                    print_warning(f"Unable to compute interdistance of tag group {tag_gr},"
                                  f"\n no path between {tag1} and {tag2}.")

    max_dist = max(tags_values['d'] for tags_values in dict_max_dist.values())
    print(f"The maximum interdistance between local tag groups is, {print_in_cbtc(in_cbtc)}:"
          f"\n{max_dist=}"
          f"\n > for: {[tags for tags, tags_values in dict_max_dist.items() if tags_values['d'] == max_dist]}")
    return dict_max_dist
