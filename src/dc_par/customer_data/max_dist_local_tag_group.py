#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys_pkg import *
from dc_sys_checking.src.dc_sys_pkg.seg_utils import *


def max_dist_local_tag_group():
    wb = load_wb()
    sh_tag = wb.sheet_by_name("Bal")
    tag_dict = get_dict(sh_tag, fixed_cols_ref=['D', 'E'])
    tag_cols_name = get_cols_name(sh_tag, cols_ref=['D', 'E'])

    sh_tag_gr = wb.sheet_by_name("StaticTag_Group")
    tag_gr_dict = get_limits_dict(sh_tag_gr, line_ref=3, col_ref='C', nb_max_limits=10, delta_between_limits=1)

    sh_seg = wb.sheet_by_name("Seg")
    seg_dict = get_dict(sh_seg, fixed_cols_ref=['G', 'H', 'I', 'J', 'K'])
    seg_cols_name = get_cols_name(sh_seg, cols_ref=['G', 'H', 'I', 'J', 'K'])

    dict_max_dist = dict()

    for tag_gr in tag_gr_dict:
        tag_list = [tag for tag in tag_gr_dict[tag_gr]]
        for tag1 in tag_list:
            for tag2 in tag_list:
                d = get_tag_dist(tag1, tag2, tag_dict, tag_cols_name, seg_dict, seg_cols_name)
                if d:
                    dict_max_dist[f"{tag_gr}::{tag1} to {tag2}"] = {"d": d}

    max_dist = max([dict_max_dist[tags]['d'] for tags in dict_max_dist])
    print(f"max_dist is {max_dist}"
          f"\nfor: {[tags for tags in dict_max_dist if dict_max_dist[tags]['d'] == max_dist]}")

    return dict_max_dist
