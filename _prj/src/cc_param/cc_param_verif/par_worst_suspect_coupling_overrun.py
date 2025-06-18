#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_path_and_distances import *
from ..load_ccparameters import *


__all__ = ["get_par_worst_suspect_coupling_overrun_additionnal_dist"]


def get_par_worst_suspect_coupling_overrun_additionnal_dist():
    par_max_couplable_train_units = get_cc_param_values("PAR_max_couplable_train_units")[0]
    par_gravity = get_cc_param_values("PAR_gravity")[0]
    par_train_unit_length_array = get_cc_param_values("PAR_train_unit_length_ARRAY__1")[0]
    par_train_worst_gamma_eb = get_cc_param_values("PAR_train_worst_gamma_eb")[0]
    print_log(f"PAR_max_couplable_train_units = {par_max_couplable_train_units}")
    print_log(f"PAR_gravity = {par_gravity}")
    print_log(f"PAR_train_unit_length_ARRAY__1 = {par_train_unit_length_array}")
    print_log(f"PAR_train_worst_gamma_eb = {par_train_worst_gamma_eb}")

    max_in_downstream = _get_max_in_direction(par_max_couplable_train_units, par_gravity,
                                              par_train_unit_length_array, par_train_worst_gamma_eb,
                                              downstream=True)
    print_success(f"{max_in_downstream = }")
    max_in_upstream = _get_max_in_direction(par_max_couplable_train_units, par_gravity,
                                            par_train_unit_length_array, par_train_worst_gamma_eb,
                                            downstream=False)
    print_success(f"{max_in_upstream = }")

    par_worst_suspect_coupling_overrun_additionnal_dist = max(max_in_upstream, max_in_downstream)
    print_success(f"{par_worst_suspect_coupling_overrun_additionnal_dist = }")
    return par_worst_suspect_coupling_overrun_additionnal_dist


def _get_max_in_direction(par_max_couplable_train_units: int, par_gravity: float,
                          par_train_unit_length_array: int, par_train_worst_gamma_eb: float,
                          downstream: bool) -> float:
    _n = par_max_couplable_train_units
    _g = par_gravity
    _l = par_train_unit_length_array
    gamma_fu = -par_train_worst_gamma_eb

    max_param = 0

    slope_dict = load_sheet(DCSYS.Profil)
    nb_slopes = len(slope_dict)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (alpha1_name, alpha1_obj) in enumerate(slope_dict.items()):
        print_log_progress_bar(i, nb_slopes, f"processing distances between {alpha1_name} and other slopes")
        alpha1 = (1 if downstream else -1) * get_dc_sys_value(alpha1_obj, DCSYS.Profil.Pente)
        alpha1_seg, alpha1_x = get_dc_sys_values(alpha1_obj, DCSYS.Profil.Seg, DCSYS.Profil.X)
        for alpha2_obj in slope_dict.values():
            if alpha2_obj == alpha1_obj:
                continue
            alpha2 = (1 if downstream else -1) * get_dc_sys_value(alpha2_obj, DCSYS.Profil.Pente)
            alpha2_seg, alpha2_x = get_dc_sys_values(alpha2_obj, DCSYS.Profil.Seg, DCSYS.Profil.X)
            if not is_seg_downstream(start_seg=alpha1_seg, end_seg=alpha2_seg, start_x=alpha1_x, end_x=alpha2_x,
                                     downstream=downstream):
                continue
            if alpha1 < alpha2:  # case of a basin
                dist = get_dist_downstream(alpha1_seg, alpha1_x, alpha2_seg, alpha2_x, downstream=downstream)
                if dist is None:
                    continue

                if dist < _n*_l:
                    alpha21 = alpha1
                else:
                    radius = abs(dist / (alpha2 - alpha1))
                    alpha21 = alpha1 + (dist - _n * _l) / (2 * radius)

                parameter = (abs(((_n - 1) * _g * _l * (alpha1 - alpha2)) / (2 * (gamma_fu - _g * alpha21)))
                             - abs(((_n - 1) * _g * _l * (alpha1 - alpha2)) / (2 * (gamma_fu - _g * alpha2))))
                if parameter > max_param:
                    max_param = parameter
                    # print("\n\n-------------------------------------------------------------------------------------------------")
                    # print("PAR_worst_suspect_coupling_overrun_additionnal_dist", max_param)
                    # print("    slope1_extremities : " + str([alpha1_seg, alpha1_x]))
                    # print("    slope2_extremities : " + str([alpha2_seg, alpha2_x]))
                    # print("    direction: " + ("INCREASE" if downstream == Direction.CROISSANT else "DECREASE"))
                    # print("    D", dist)
                    # print("    Dp", 0)
                    # print("    n", _n)
                    # print("    L", _l)
                    # print("    alpha1", alpha1)
                    # print("    alpha2", alpha2)
                    # print("    alpha21", alpha21)
                    # print("    gammaFu", gamma_fu)
                    # print("    minAlpha", min(alpha1, alpha2))
                    # print("-------------------------------------------------------------------------------------------------\n\n")
    print_log_progress_bar(nb_slopes, nb_slopes, "processing distances between slopes finished", end=True)

    return max_param
