#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.platform_utils import *
from ...dc_sys_sheet_utils.osp_utils import *
from ...dc_sys_sheet_utils.train_utils import *
from ...dc_sys_draw_path.dc_sys_get_zones import *
from ...dc_par import *


__all__ = ["cc_quai_6"]


def cc_quai_6():
    stopping_point_station_without_psd_dist = get_param_value("stopping_point_station_without_psd_dist")
    stopping_point_station_with_psd_dist = get_param_value("stopping_point_station_with_psd_dist")
    stopping_point_out_station_calibration_dist = get_param_value("stopping_point_out_station_calibration_dist")

    res_dict = dict()

    plt_dict = load_sheet(DCSYS.Quai)
    nb_plt = len(plt_dict)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (plt_name, plt_value) in enumerate(plt_dict.items()):
        print_log_progress_bar(i, nb_plt, f"processing slope under train at OSP of platform {plt_name}")

        calib_auth = is_accelerometer_calibration_authorized_at_platform(plt_name)
        with_psd = get_dc_sys_value(plt_value, DCSYS.Quai.AvecFq)
        if with_psd == YesOrNo.O:
            tolerance_around_osp = stopping_point_station_with_psd_dist
            tolerance_around_osp_str = "stopping_point_station_with_psd_dist"
        else:
            tolerance_around_osp = stopping_point_station_without_psd_dist
            tolerance_around_osp_str = "stopping_point_station_without_psd_dist"

        for osp_name, osp_seg, osp_x, osp_direction, osp_type in get_dc_sys_zip_values(
                plt_value, DCSYS.Quai.PointDArret.Name, DCSYS.Quai.PointDArret.Seg, DCSYS.Quai.PointDArret.X,
                DCSYS.Quai.PointDArret.SensAssocie, DCSYS.Quai.PointDArret.TypePtArretQuai):

            # # TODO to delete
            # if osp_name not in ["PT_ARRET_AUM_771Q1", "PT_ARRET_ERS_764Q2", "PT_ARRET_VEE_769Q2"]:
            #     continue

            sub_dict = _check_if_constant_slope_under_car_with_accel(osp_name, osp_seg, osp_x, osp_direction,
                                                                     osp_type, tolerance_around_osp)
            res_dict[osp_name] = sub_dict

            if ("ko" not in sub_dict) == calib_auth:  # if calibration is authorized when slope is constant,
                # and if calibration is not authorized when slope is not constant -> configuration OK
                # print(f"OK")
                # pretty_print_dict(sub_dict)
                continue
            # else either calibration is authorized when there is a slope change -> KO
            if "ko" in sub_dict:
                print_error(f"[Allow Accelerometers Calibration] should not be authorized for {Color.beige}{osp_name}"
                            f"{Color.reset} as there is a slope change under the car containing the accelerometer when "
                            f"the train is stopped at the OSP +/- {tolerance_around_osp_str}:")
                pretty_print_dict(sub_dict)
            # or calibration is not authorized when slope is constant -> we write a comment to say that it could be set
            if calib_auth == YesOrNo.N:
                print(f"[Allow Accelerometers Calibration] could be authorized for {Color.beige}{osp_name}"
                      f"{Color.reset} as there is no slope change under the car containing the accelerometer when "
                      f"the train is stopped at the OSP +/- {tolerance_around_osp_str}.")
                pretty_print_dict(sub_dict)

    print_log_progress_bar(nb_plt, nb_plt, f"computation of slope under train at platform OSPs done", end=True)
    return res_dict


def _check_if_constant_slope_under_car_with_accel(osp_name: str, osp_seg: str, osp_x: float, osp_direction: str,
                                                  osp_type: str, tolerance_around_osp: float):
    osp_position_and_type = [add_track_kp_to_position(get_object_position(DCSYS.Quai.PointDArret, osp_name)),
                             get_osp_type(osp_name)]
    res_dict = dict()
    train_types_dict = load_sheet(DCSYS.Train_Types)
    for train_type_name in train_types_dict.keys():  # for each train type

        # We get train front position according to the OSP position, direction and type (front, rear, middle)
        train_front_position_at_osp = get_train_front_position_at_osp(train_type_name, osp_seg, osp_x, osp_direction,
                                                                      osp_type)

        dict_accel_car = _get_accel_car(train_type_name)
        for accel_car, list_train_units in dict_accel_car.items():  # in case the accelerometer is not set
            # in the same car for each train unit of this train type
            for train_polarity in [True, False]:  # considering both directions the train can have
                # (the accelerometer is in the same car but the car can be at different locations from the train front)

                # We get the tail and front position of the car when train is at OSP
                (car_front_seg, car_front_x), (car_tail_seg, car_tail_x) = _get_car_position_at_osp(
                    train_type_name, accel_car, train_polarity, train_front_position_at_osp, osp_direction)

                # We need to check that there is no slope change under the car with the accelerometer,
                # enlarged by the tolerance under the OSP.
                (front_seg, front_x), (tail_seg, tail_x) = _enlarged_position_by_osp_tolerance(
                    car_front_seg, car_front_x, car_tail_seg, car_tail_x, osp_direction, tolerance_around_osp)

                zone_limits = [(front_seg, front_x, get_reverse_direction(osp_direction)),
                               (tail_seg, tail_x, osp_direction)]

                slopes_under_car = get_objects_in_zone_limits(DCSYS.Profil, zone_limits)
                if slopes_under_car is not None:
                    slopes_under_car = [(name, add_track_kp_to_position(get_object_position(DCSYS.Profil, name)))
                                        for name in slopes_under_car]
                    res_dict["ko"] = True

                accel_car_str = f"accelerometer_car = {accel_car}"
                if train_type_name not in res_dict:
                    res_dict[train_type_name] = dict()
                if accel_car_str not in res_dict[train_type_name]:
                    if list_train_units != "all":
                        res_dict[train_type_name][accel_car_str] = {"list_train_units": list_train_units}
                    else:  # Normally all train units of the same type have the same accelerometer car, so no need to
                        # display it.
                        res_dict[train_type_name][accel_car_str] = dict()

                    res_dict[train_type_name][accel_car_str]["osp_position_and_type"] = osp_position_and_type
                    res_dict[train_type_name][accel_car_str]["train_front_position_at_osp"] = add_track_kp_to_position(
                        train_front_position_at_osp)

                res_dict[train_type_name][accel_car_str][f"train_polarity = {train_polarity}"] = {
                    "accelerometer_car_position_with_tolerance_at_osp": add_track_kp_to_zone_limits(zone_limits),
                    "slope_changes_under_accelerometer_car": slopes_under_car
                }
    return res_dict


def _get_accel_car(train_type_name: str) -> dict[int, list[tuple[str, str]]]:
    train_dict = load_sheet(DCSYS.Train)
    cc_dict = load_sheet(DCSYS.Carborne_Controllers)
    dict_accel_car = dict()
    for train_value in train_dict.values():
        if get_dc_sys_value(train_value, DCSYS.Train.Type) != train_type_name:
            continue
        train_unit_id = int(get_dc_sys_value(train_value, DCSYS.Train.CbtcTrainUnitId))
        for cab_cc_name in get_dc_sys_values(train_value, DCSYS.Train.Cab1CcName, DCSYS.Train.Cab2CcName):
            if cab_cc_name is None:
                continue
            cab_cc_value = cc_dict[cab_cc_name]
            accel_car = int(get_dc_sys_value(cab_cc_value, DCSYS.Carborne_Controllers.Acceleros.AccelerosCar))
            if accel_car not in dict_accel_car:
                dict_accel_car[accel_car] = list()
            dict_accel_car[accel_car].append((train_unit_id, cab_cc_name))
    for accel_car, info in dict_accel_car.items():
        if len(info) == len([train_units for train_units, train_value in train_dict.items()
                             if get_dc_sys_value(train_value, DCSYS.Train.Type) == train_type_name]):
            dict_accel_car[accel_car] = "all"
    return dict_accel_car


def _enlarged_position_by_osp_tolerance(front_seg: str, front_x: float, tail_seg: str, tail_x: float, direction: str,
                                        tolerance_around_osp: float) -> tuple[tuple[str, float], tuple[str, float]]:
    polarity = 1 if direction == Direction.CROISSANT else -1

    front_seg, front_x = get_correct_seg_offset(  # front is moved further downstream
        front_seg, front_x + polarity * tolerance_around_osp)
    tail_seg, tail_x = get_correct_seg_offset(  # tail is moved further upstream
        tail_seg, tail_x - polarity * tolerance_around_osp)

    return (front_seg, front_x), (tail_seg, tail_x)


def _get_car_position_at_osp(train_type: str, car_number: int, cars_order: bool,
                             train_front_position_at_osp: tuple[str, float], osp_direction: str
                             ) -> tuple[tuple[str, float], tuple[str, float]]:
    train_front_seg, train_front_x = train_front_position_at_osp

    # We get the length between the train front and the tail and front of the car
    length_until_car_front, length_until_car_tail = _get_car_position_from_train_front(train_type, car_number,
                                                                                       cars_order)

    polarity = 1 if osp_direction == Direction.CROISSANT else -1
    car_front_seg, car_front_x = get_correct_seg_offset(
        train_front_seg, train_front_x - polarity * length_until_car_front)
    car_tail_seg, car_tail_x = get_correct_seg_offset(
        train_front_seg, train_front_x - polarity * length_until_car_tail)

    return (car_front_seg, car_front_x), (car_tail_seg, car_tail_x)


def _get_car_position_from_train_front(train_type: str, car_number: int, cars_order: bool) -> tuple[float, float]:
    car_names = get_car_names(train_type)

    current_length = 0.
    list_of_car_numbers = list(car_names.keys()) if cars_order else reversed(list(car_names.keys()))
    # the front car can be the first one or the last one
    for current_car_number in list_of_car_numbers:
        if current_car_number == car_number:
            break
        current_car_name = car_names[current_car_number]
        if current_car_name is None:
            continue
        car_length = get_car_length(current_car_name)
        current_length += car_length

    length_until_car_front = current_length
    length_until_car_tail = current_length + get_car_length(car_names[car_number])

    return length_until_car_front, length_until_car_tail
