#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_train_length", "get_car_length", "get_car_names"]


def get_train_length(train_name: str) -> Optional[float]:
    pv_consist_dict = load_sheet(DCSYS.Train_Consist)
    av_consist_dict = load_sheet(DCSYS.AV_Consist)

    if train_name in pv_consist_dict:
        train_length = sum(_get_unit_length(unit_name) if unit_name is not None else 0
                           for unit_name in get_dc_sys_values(pv_consist_dict[train_name],
                                                              DCSYS.Train_Consist.TrainType1,
                                                              DCSYS.Train_Consist.TrainType2,
                                                              DCSYS.Train_Consist.TrainType3,
                                                              DCSYS.Train_Consist.TrainType4))
    elif train_name in av_consist_dict:
        train_length = sum(_get_unit_length(unit_name) if unit_name is not None else 0
                           for unit_name in get_dc_sys_values(av_consist_dict[train_name],
                                                              DCSYS.AV_Consist.VehicleType1,
                                                              DCSYS.AV_Consist.VehicleType2,
                                                              DCSYS.AV_Consist.VehicleType3,
                                                              DCSYS.AV_Consist.VehicleType4,
                                                              DCSYS.AV_Consist.VehicleType5))
    else:
        train_length = _get_unit_length(train_name)
        if train_length is None:
            print_error(f"{Color.blue}{train_name}{Color.reset} is not a train name defined in DC_SYS.")
    return train_length


def _get_unit_length(unit_name: str) -> Optional[float]:
    pv_dict = load_sheet(DCSYS.Train_Types)
    av_dict = load_sheet(DCSYS.AV_Types)
    flatbed_dict = load_sheet(DCSYS.Flatbed_Types)

    if unit_name in pv_dict:
        unit_info = pv_dict[unit_name]
        return get_dc_sys_value(unit_info, DCSYS.Train_Types.Length)
    elif unit_name in av_dict:
        unit_info = av_dict[unit_name]
        return get_dc_sys_value(unit_info, DCSYS.AV_Types.Length)
    elif unit_name in flatbed_dict:
        unit_info = flatbed_dict[unit_name]
        return get_dc_sys_value(unit_info, DCSYS.Flatbed_Types.Length)
    else:
        return None


def get_car_length(car_name: str) -> float:
    car_dict = load_sheet(DCSYS.Car)
    car_value = car_dict[car_name]
    return get_dc_sys_value(car_value, DCSYS.Car.Length)


def get_car_names(train_type: str) -> dict[int, Optional[str]]:
    train_types_dict = load_sheet(DCSYS.Train_Types)
    dict_of_cars = dict()
    for car_number, car_name in enumerate(get_dc_sys_values(
            train_types_dict[train_type],
            DCSYS.Train_Types.Car1, DCSYS.Train_Types.Car2, DCSYS.Train_Types.Car3, DCSYS.Train_Types.Car4,
            DCSYS.Train_Types.Car5, DCSYS.Train_Types.Car6, DCSYS.Train_Types.Car7, DCSYS.Train_Types.Car8,
            DCSYS.Train_Types.Car9, DCSYS.Train_Types.Car10), start=1):

        dict_of_cars[car_number] = car_name
    return dict_of_cars
