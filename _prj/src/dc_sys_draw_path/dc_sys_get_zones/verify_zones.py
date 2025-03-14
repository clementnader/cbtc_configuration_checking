#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ...dc_sys import *
from .zones_utils import get_segments_within_zone


__all__ = ["check_dc_sys_zones_definition"]


def check_dc_sys_zones_definition():
    for sheet_name in get_all_sheet_names():
        sheet_dict = load_sheet(sheet_name)
        for obj_name in sheet_dict.keys():
            get_segments_within_zone(sheet_name, obj_name)
