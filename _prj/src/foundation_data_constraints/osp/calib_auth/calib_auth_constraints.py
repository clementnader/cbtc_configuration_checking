#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_sys_get_cbtc_territory import *
from ....dc_sys_sheet_utils.platform_utils import *
from ....dc_sys_sheet_utils.osp_utils import *
from ....dc_par import *
from .common_functions import *
from .write_file import *


__all__ = ["cc_quai_6", "r_point_arret_ato_10"]


def cc_quai_6(in_cbtc: bool = False):
    print_title("Verification of CC_QUAI_6", color=Color.mint_green)
    stopping_point_station_without_psd_dist = get_parameter_value("stopping_point_station_without_psd_dist")
    stopping_point_station_with_psd_dist = get_parameter_value("stopping_point_station_with_psd_dist")

    res_dict = dict()

    if in_cbtc:
        plt_dict = get_objects_in_cbtc_ter(DCSYS.Quai)
    else:
        plt_dict = load_sheet(DCSYS.Quai)
    nb_plt = len(plt_dict)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (plt_name, plt_value) in enumerate(plt_dict.items()):
        print_log_progress_bar(i, nb_plt, f"slope under train at OSP of {plt_name}")

        calib_auth = is_accelerometer_calibration_authorized_at_platform(plt_name)

        with_psd = get_dc_sys_value(plt_value, DCSYS.Quai.AvecFq)
        if with_psd == YesOrNo.O:
            tolerance_around_osp = stopping_point_station_with_psd_dist
        else:
            tolerance_around_osp = stopping_point_station_without_psd_dist

        for osp_name, osp_seg, osp_x, osp_direction, osp_type in get_dc_sys_zip_values(
                plt_value, DCSYS.Quai.PointDArret.Name, DCSYS.Quai.PointDArret.Seg, DCSYS.Quai.PointDArret.X,
                DCSYS.Quai.PointDArret.SensAssocie, DCSYS.Quai.PointDArret.TypePtArretQuai):
            sub_dict = check_if_constant_slope_under_car_with_accel(osp_seg, osp_x, osp_direction,
                                                                    osp_type, tolerance_around_osp)
            sub_dict["Allow Accelerometers Calibration"] = calib_auth
            res_dict[osp_name] = sub_dict

    print_log_progress_bar(nb_plt, nb_plt, f"computation of slope under train at platform OSPs done", end=True)

    res_file_path = create_verif_file(res_dict, "CC_QUAI_6", in_cbtc)
    open_excel_file(res_file_path)


def r_point_arret_ato_10(in_cbtc: bool = False):
    print_title("Verification of R_POINT_ARRET_ATO_10", color=Color.mint_green)
    stopping_point_out_station_calibration_dist = get_parameter_value("stopping_point_out_station_calibration_dist")

    res_dict = dict()

    if in_cbtc:
        osp_dict = get_objects_in_cbtc_ter(DCSYS.PtA)
    else:
        osp_dict = load_sheet(DCSYS.PtA)
    nb_osp = len(osp_dict)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (osp_name, osp_value) in enumerate(osp_dict.items()):
        print_log_progress_bar(i, nb_osp, f"slope under train at {osp_name}")

        calib_auth = is_accelerometer_calibration_authorized_at_osp_not_platform_related(osp_name)

        osp_seg, osp_x, osp_direction, osp_type = get_dc_sys_values(
            osp_value, DCSYS.PtA.Seg, DCSYS.PtA.X, DCSYS.PtA.SensAssocie, DCSYS.PtA.TypePtAto)
        sub_dict = check_if_constant_slope_under_car_with_accel(osp_seg, osp_x, osp_direction,
                                                                osp_type, stopping_point_out_station_calibration_dist)
        sub_dict["Allow Accelerometers Calibration"] = calib_auth
        res_dict[osp_name] = sub_dict

    print_log_progress_bar(nb_osp, nb_osp, f"computation of slope under train at OSPs out of platform done",
                           end=True)

    res_file_path = create_verif_file(res_dict, "R_POINT_ARRET_ATO_10", in_cbtc)
    open_excel_file(res_file_path)
