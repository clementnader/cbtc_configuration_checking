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
    progress_bar(1, 1, end=True)  # reset progress_bar
    list_sheets = get_all_sheet_names()
    nb_sheets = len(list_sheets)
    for i, sheet_name in enumerate(list_sheets):
        print_log_progress_bar(i, nb_sheets, f"zones in {sheet_name}")
        sheet_dict = load_sheet(sheet_name)
        for object_name in sheet_dict:
            get_segments_within_zone(sheet_name, object_name)
    print_log_progress_bar(nb_sheets, nb_sheets, "verification of the good definition of the zone objects in "
                                                 "the DC_SYS sheets finished", end=True)
