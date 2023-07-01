#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import DCSYS
from ..load_database import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


def get_tags_in_cbtc_ter():
    tag_dict = load_sheet(DCSYS.Bal)

    within_cbtc_tag_dict = dict()
    for tag_name, tag_value in tag_dict.items():
        seg = get_dc_sys_value(tag_value, DCSYS.Bal.Seg)
        x = float(get_dc_sys_value(tag_value, DCSYS.Bal.X))
        if is_point_in_cbtc_ter(seg, x) is not False:
            within_cbtc_tag_dict[tag_name] = tag_value
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Tag {tag_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
    return within_cbtc_tag_dict


def get_tag_gr_in_cbtc_ter():
    within_cbtc_tag_dict = get_tags_in_cbtc_ter()
    tag_gr_dict = load_sheet(DCSYS.StaticTag_Group)
    within_cbtc_tag_gr_dict = dict()
    for tag_gr_name, tag_gr_value in tag_gr_dict.items():
        tags = [tag for tag in get_dc_sys_value(tag_gr_value, DCSYS.StaticTag_Group.TagList.Tag) if tag is not None]
        if all(tag in within_cbtc_tag_dict for tag in tags):
            within_cbtc_tag_gr_dict[tag_gr_name] = tag_gr_value
        elif any(tag in within_cbtc_tag_dict for tag in tags):
            print_warning(f"Tag group {tag_gr_name} possesses tags within and without CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_tag_gr_dict[tag_gr_name] = tag_gr_value
    return within_cbtc_tag_gr_dict
