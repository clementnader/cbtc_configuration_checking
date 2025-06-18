#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from .train_utils import *


__all__ = ["get_train_front_position_at_osp",
           "is_accelerometer_calibration_authorized_at_osp_not_platform_related"]


def get_train_front_position_at_osp(train_type: str, osp_seg: str, osp_x: float, osp_direction: str, osp_type: str
                                    ) -> Optional[tuple[str, float]]:
    if osp_type == StoppingPointType.AVANT:
        return osp_seg, osp_x

    train_length = get_train_length(train_type)
    polarity = 1 if osp_direction == Direction.CROISSANT else -1

    if osp_type == StoppingPointType.CENTRE:
        train_front_seg, train_front_x = get_correct_seg_offset(osp_seg, osp_x + polarity * 0.5 * train_length)
        return train_front_seg, train_front_x

    if osp_type == StoppingPointType.ARRIERE:
        train_front_seg, train_front_x = get_correct_seg_offset(osp_seg, osp_x + polarity * train_length)
        return train_front_seg, train_front_x

    print_error(f"OSP Type {osp_type} is unknown, it should be in {get_class_values(StoppingPointType)}")


def is_accelerometer_calibration_authorized_at_osp_not_platform_related(osp_name: str) -> Optional[bool]:
    osp_dict = load_sheet(DCSYS.PtA)
    osp_value = osp_dict[osp_name]
    if "AllowAccelerometerCalibration" in get_class_attr_dict(DCSYS.PtA):
        return get_dc_sys_value(osp_value, DCSYS.PtA.AllowAccelerometerCalibration) == YesOrNo.O

    if "AllowAccelerometersCalibration" in get_class_attr_dict(DCSYS.PtA):
        return get_dc_sys_value(osp_value, DCSYS.PtA.AllowAccelerometersCalibration) == YesOrNo.O
