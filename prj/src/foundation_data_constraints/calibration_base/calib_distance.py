#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_path_and_distances import get_dist_downstream


__all__ = ["verif_calib_distance"]


def verif_calib_distance():
    print_title(f"Verification of Calibration Base Distance", color=Color.mint_green)
    calib_dict = load_sheet(DCSYS.Calib)
    for calib_val in calib_dict.values():
        start_tag, end_tag = get_dc_sys_values(calib_val, DCSYS.Calib.BaliseDeb, DCSYS.Calib.BaliseFin)
        dist_calib = get_dc_sys_value(calib_val, DCSYS.Calib.DistanceCalib)
        direction_calib = get_dc_sys_value(calib_val, DCSYS.Calib.SensCalib)
        loc_start_tag = get_obj_position(DCSYS.Bal, start_tag)
        loc_end_tag = get_obj_position(DCSYS.Bal, end_tag)
        dist_test = get_dist_downstream(*loc_start_tag, *loc_end_tag, downstream=direction_calib == Direction.CROISSANT)
        if dist_calib != dist_test:
            print_error(f"For Calibration Base {Color.beige}({start_tag = }; {end_tag = }){Color.reset},\n"
                        f"Calibration Distance has been wrongly set to {Color.orange}{dist_calib}{Color.reset}, "
                        f"instead of the real distance between the two tags of "
                        f"{Color.mint_green}{dist_test}{Color.reset}.")
