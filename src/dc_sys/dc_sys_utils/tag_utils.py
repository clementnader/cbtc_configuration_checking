#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database.load_sheets import load_sheet, get_cols_name
from .cbtc_territory_utils import is_point_in_cbtc_ter


def get_tags_in_cbtc_ter():
    tag_dict = load_sheet("tag", generic_name=True)
    tag_cols_name = get_cols_name("tag")

    within_cbtc_tag_dict = dict()
    for tag_values in tag_dict.values():
        tag_name = tag_values[tag_cols_name['B']]
        seg = tag_values[tag_cols_name['D']]
        x = float(tag_values[tag_cols_name['E']])
        if is_point_in_cbtc_ter(seg, x) is not False:
            within_cbtc_tag_dict[tag_name] = tag_values
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Tag {tag_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
    return within_cbtc_tag_dict


def get_tag_gr_in_cbtc_ter():
    within_cbtc_tag_dict = get_tags_in_cbtc_ter()
    tag_gr_dict = load_sheet("tag_gr")
    within_cbtc_tag_gr_dict = dict()
    for tag_gr_name, tag_gr_values in tag_gr_dict.items():
        tags = [list(limits.values())[0] for limits in tag_gr_values["limits"]]
        if all(tag in within_cbtc_tag_dict for tag in tags):
            within_cbtc_tag_gr_dict[tag_gr_name] = tag_gr_values
        elif any(tag in within_cbtc_tag_dict for tag in tags):
            print_warning(f"Tag group {tag_gr_name} possesses tags within and without CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_tag_gr_dict[tag_gr_name] = tag_gr_values
    return within_cbtc_tag_gr_dict
