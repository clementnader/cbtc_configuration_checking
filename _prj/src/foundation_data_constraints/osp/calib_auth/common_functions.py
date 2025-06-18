#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_sys_sheet_utils.osp_utils import *
from ....dc_sys_sheet_utils.train_utils import *
from ....dc_sys_sheet_utils.slope_utils import *
from ....dc_sys_draw_path.dc_sys_get_zones import get_objects_in_zone_limits


__all__ = ["check_if_constant_slope_under_car_with_accel"]


def check_if_constant_slope_under_car_with_accel(osp_seg: str, osp_x: float, osp_direction: str,
                                                 osp_type: str, tolerance_around_osp: float):
    osp_position_and_type = [add_track_kp_to_position((osp_seg, osp_x, osp_direction)), osp_type]
    res_dict = dict()
    res_dict["osp_position_and_type"] = osp_position_and_type
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

                # We check that the slope is constant under, before and after the car
                slope_change_under_car = (get_objects_in_zone_limits(DCSYS.Profil, zone_limits) is not None)
                min_slope, max_slope = get_min_and_max_slopes_in_zone_limits(zone_limits)

                # Write results in dict
                accel_car_str = f"accelerometer_car = {accel_car}"
                if train_type_name not in res_dict:
                    res_dict[train_type_name] = dict()
                    res_dict[train_type_name]["train_front_position_at_osp"] = add_track_kp_to_position(
                        train_front_position_at_osp)
                if accel_car_str not in res_dict[train_type_name]:
                    if list_train_units != "all":
                        res_dict[train_type_name][accel_car_str] = {"list_train_units": list_train_units}
                    else:
                        # Normally all train units of the same type have the same accelerometer car, so no need to
                        # display it in that case.
                        res_dict[train_type_name][accel_car_str] = dict()

                res_dict[train_type_name][accel_car_str][f"train_polarity = {train_polarity}"] = {
                    "accelerometer_car_position_with_tolerance_at_osp": add_track_kp_to_zone_limits(zone_limits),
                    "slope_change_under_car": slope_change_under_car,
                    "min_slope": min_slope, "max_slope": max_slope, "constant_slope": (min_slope != max_slope)
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
