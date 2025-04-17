#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_path_and_distances import get_dist_downstream, get_list_of_paths


__all__ = ["verif_calib_distance", "cf_calib_4"]


def verif_calib_distance():
    print_title(f"Verification of Calibration Base Distance", color=Color.mint_green)
    calib_dict = load_sheet(DCSYS.Calib)
    for calib_val in calib_dict.values():
        start_tag, end_tag = get_dc_sys_values(calib_val, DCSYS.Calib.BaliseDeb, DCSYS.Calib.BaliseFin)
        dist_calib = get_dc_sys_value(calib_val, DCSYS.Calib.DistanceCalib)
        direction_calib = get_dc_sys_value(calib_val, DCSYS.Calib.SensCalib)
        loc_start_tag = get_object_position(DCSYS.Bal, start_tag)
        loc_end_tag = get_object_position(DCSYS.Bal, end_tag)
        dist_test = get_dist_downstream(*loc_start_tag, *loc_end_tag, downstream=direction_calib == Direction.CROISSANT)
        if dist_calib != dist_test:
            print_error(f"For Calibration Base {Color.beige}({start_tag = }; {end_tag = }){Color.reset},\n"
                        f"Calibration Distance has been wrongly set to {Color.orange}{dist_calib}{Color.reset}, "
                        f"instead of the real distance between the two tags of "
                        f"{Color.mint_green}{dist_test}{Color.reset}.")


def cf_calib_4():
    calib_dict = load_sheet(DCSYS.Calib)
    for calib_name, calib_value in calib_dict.items():
        bal1, bal2 = get_dc_sys_values(calib_value, DCSYS.Calib.BaliseDeb, DCSYS.Calib.BaliseFin)
        seg1, _ = get_object_position(DCSYS.Bal, bal1)
        seg2, _ = get_object_position(DCSYS.Bal, bal2)
        list_of_paths = get_list_of_paths(seg1, seg2, verbose=True)
        if not list_of_paths:
            print_error(f"For {calib_name} (between {bal1} and {bal2}), "
                        f"no path found between {seg1} and {seg2}.")
            continue
        if len(list_of_paths) > 1:
            print_error(f"For {calib_name} (between {bal1} and {bal2}), "
                        f"multiple paths found between {seg1} and {seg2}:")
            print(list_of_paths)
            continue
        if len(list_of_paths) == 1:
            upstream, path = list_of_paths[0]
            calib_direction = get_dc_sys_value(calib_value, DCSYS.Calib.SensCalib)
            if (calib_direction == Direction.CROISSANT) != upstream:
                print_error(f"For {calib_name} (between {bal1} and {bal2}), path found between {seg1} and {seg2} is "
                            f"found in the opposite direction:")
                print(calib_direction, upstream)
                print(list_of_paths)
            continue
