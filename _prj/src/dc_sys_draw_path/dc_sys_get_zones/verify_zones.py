#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from .zones_utils import get_segments_within_zone


__all__ = ["check_dc_sys_zones_definition"]



def check_dc_sys_zones_definition():
    check_dc_sys_global_definition()
    print_title(f"Verification of the good definition of all the zone objects in the DC_SYS")
    # Trace every zone of every sheet
    for sheet_name in get_all_sheet_names():
        sheet_dict = load_sheet(sheet_name)
        for obj_name in sheet_dict:
            get_segments_within_zone(sheet_name, obj_name)
