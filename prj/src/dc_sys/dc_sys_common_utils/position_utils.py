#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .common_utils import *
from .switch_utils import *


__all__ = ["get_obj_position", "get_obj_zone_limits", "get_obj_oriented_zone_limits"]


def get_obj_position(obj_type, obj_name: str) -> Union[tuple[str, float], tuple[str, float, str],
                                                       list[tuple[str, float]],
                                                       list[tuple[str, float, str]], None]:
    """
    Returns the position of an object:
        - if it is a point, returns a tuple (segment, offset)
        - if it is a zone, returns a list of its extremities (segment, offset) and if these extremities are oriented,
        returns a list of its oriented extremities (segment, offset, direction)
    :param obj_type: type of the object, using DCSYS class attributes
    :param obj_name: name of the object
    :return: tuple[str, float] for point object, list[tuple[str, float]] for non-oriented zone object,
     list[tuple[str, float, str]] for oriented zone object, None if it was unable to find the position
    """
    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = get_class_attr_dict(obj_sh).keys()

    if get_sh_name(obj_type) == get_sh_name(DCSYS.Aig):
        # a dedicated function for switches
        return give_sw_pos(obj_val)
    if "IXL_Overlap" in get_class_attr_dict(DCSYS) and get_sh_name(obj_type) == get_sh_name(DCSYS.IXL_Overlap):
        # a dedicated function for overlaps
        return _get_ovl_pos(obj_val)
    if "Calib" in get_class_attr_dict(DCSYS) and get_sh_name(obj_type) == get_sh_name(DCSYS.Calib):
        # a dedicated function for calibration bases
        return _get_calib_pos(obj_val)

    if "Seg" in sh_attrs and "X" in sh_attrs:
        seg, x = get_dc_sys_values(obj_val, obj_sh.Seg, obj_sh.X)
        direction = _get_direction_of_point(obj_type, obj_name)
        if direction is not None:
            return seg, x, direction
        return seg, x

    limits = get_obj_zone_limits(obj_type, obj_name)
    if limits is not None:
        return limits

    return None


def _get_ovl_pos(obj_val: dict[str]) -> list[tuple[str, float, str]]:
    vsp_direction = get_dc_sys_value(obj_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Sens)
    # The zone of the overlap is upstream the VSP and downstream the release point
    rp_seg, rp_x = get_dc_sys_values(obj_val, DCSYS.IXL_Overlap.ReleasePoint.Seg,
                                     DCSYS.IXL_Overlap.ReleasePoint.X)
    vsp_seg, vsp_x = get_dc_sys_values(obj_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Seg,
                                       DCSYS.IXL_Overlap.VitalStoppingPoint.X)
    return [(rp_seg, rp_x, get_reverse_direction(vsp_direction)), (vsp_seg, vsp_x, vsp_direction)]


def _get_calib_pos(obj_val: dict[str]) -> list[tuple[str, float]]:
    start_tag, end_tag = get_dc_sys_values(obj_val, DCSYS.Calib.BaliseDeb, DCSYS.Calib.BaliseFin)
    return [get_obj_position(DCSYS.Bal, start_tag), get_obj_position(DCSYS.Bal, end_tag)]


def _get_direction_of_point(obj_type, obj_name: str) -> Optional[str]:
    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = get_class_attr_dict(obj_sh).keys()
    if "Direction" in sh_attrs:
        direction = get_dc_sys_value(obj_val, obj_sh.Direction)
    elif "Sens" in sh_attrs:
        direction = get_dc_sys_value(obj_val, obj_sh.Sens)
    elif "SensAssocie" in sh_attrs:
        direction = get_dc_sys_value(obj_val, obj_sh.SensAssocie)
    else:
        direction = None
    return direction


def get_obj_zone_limits(obj_type, obj_name: str) -> Union[None, list[tuple[str, float]], list[tuple[str, float, str]]]:
    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = get_class_attr_dict(obj_sh).keys()

    if "ExtremiteDuQuai" in sh_attrs:
        limits = get_platform_oriented_limits(obj_val)
        return limits
    if "Limit" in sh_attrs:
        limits = get_obj_limits(obj_val, obj_sh.Limit)
        return limits
    if "Extremite" in sh_attrs:
        limits = get_obj_limits(obj_val, obj_sh.Extremite)
        return limits
    if "ExtremiteSuivi" in sh_attrs:
        limits = get_obj_limits(obj_val, obj_sh.ExtremiteSuivi)
        return limits
    if "ExtZsm" in sh_attrs:
        limits = get_obj_limits(obj_val, obj_sh.ExtZsm)
        return limits
    if "OdometricZone" in sh_attrs:
        limits = get_obj_limits(obj_val, obj_sh.OdometricZone)
        return limits
    if "From" in sh_attrs and "To" in sh_attrs:
        seg1, x1 = get_dc_sys_values(obj_val, obj_sh.From.Seg, obj_sh.From.X)
        seg2, x2 = get_dc_sys_values(obj_val, obj_sh.To.Seg, obj_sh.To.X)
        return [(seg1, x1), (seg2, x2)]
    if "De" in sh_attrs and "A" in sh_attrs:
        seg1, x1 = get_dc_sys_values(obj_val, obj_sh.De.Seg, obj_sh.De.X)
        seg2, x2 = get_dc_sys_values(obj_val, obj_sh.A.Seg, obj_sh.A.X)
        return [(seg1, x1), (seg2, x2)]
    return None


def get_obj_oriented_zone_limits(obj_type, obj_name: str) -> Union[None, list[tuple[str, float, str]]]:
    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = get_class_attr_dict(obj_sh).keys()

    if "ExtremiteDuQuai" in sh_attrs:
        limits = get_platform_oriented_limits(obj_val)
        return limits
    if "Limit" in sh_attrs:
        limits = get_obj_oriented_limits(obj_val, obj_sh.Limit)
        return limits
    if "Extremite" in sh_attrs:
        limits = get_obj_oriented_limits(obj_val, obj_sh.Extremite)
        return limits
    if "ExtremiteSuivi" in sh_attrs:
        limits = get_obj_oriented_limits(obj_val, obj_sh.ExtremiteSuivi)
        return limits
    return None


def get_obj_limits(obj_val: dict[str], obj_limit_attr) -> Union[list[tuple[str, float]], list[tuple[str, float, str]]]:
    limits = get_obj_oriented_limits(obj_val, obj_limit_attr)
    if limits is None:  # non-oriented limits
        limits = list(get_dc_sys_zip_values(obj_val, obj_limit_attr.Seg, obj_limit_attr.X))
    return limits


def get_obj_oriented_limits(obj_val: dict[str], obj_limit_attr) -> Union[None, list[tuple[str, float, str]]]:
    limit_sub_attrs = get_class_attr_dict(obj_limit_attr).keys()
    if "Direction" in limit_sub_attrs:
        limits = list(get_dc_sys_zip_values(obj_val, obj_limit_attr.Seg, obj_limit_attr.X, obj_limit_attr.Direction))
    elif "Sens" in limit_sub_attrs:
        limits = list(get_dc_sys_zip_values(obj_val, obj_limit_attr.Seg, obj_limit_attr.X, obj_limit_attr.Sens))
    else:
        limits = None
    return limits


def get_platform_oriented_limits(obj_val) -> list[tuple[str, float, str]]:
    limits = list()
    for seg, x, direction in get_dc_sys_zip_values(obj_val, DCSYS.Quai.ExtremiteDuQuai.Seg,
                                                   DCSYS.Quai.ExtremiteDuQuai.X, DCSYS.Quai.ExtremiteDuQuai.SensExt):
        if direction == LineRelatedDirection.SENS_LIGNE:  # the downstream platform end, so the zone is upstream
            direction = Direction.DECROISSANT
        elif direction == LineRelatedDirection.SENS_OPPOSE:  # the upstream platform end, so the zone is downstream
            direction = Direction.CROISSANT
        limits.append((seg, x, direction))
    return limits
