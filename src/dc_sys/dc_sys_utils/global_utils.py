#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .switch_utils import give_sw_pos

__all__ = ["get_obj_position"]


def get_obj_position(obj_type, obj_name: str) -> Union[tuple[str, float], list[tuple[str, float]], None]:
    """
    Returns the position of an object:
        - if it is a point, returns a tuple (segment, offset)
        - if it is a zone, returns a list of these extremities (segment, offset)
    :param obj_type: type of the object, using DCSYS class attributes
    :param obj_name: name of the object
    :return: tuple[str, float] for point object, list[tuple[str, float]] for zone object,
     None if it was unable to find the position
    """
    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = get_sheet_attributes_columns_dict(obj_sh).keys()

    if get_sh_name(obj_type) == get_sh_name(DCSYS.Aig):  # a dedicated function for switches
        return give_sw_pos(obj_val)
    elif get_sh_name(obj_type) == get_sh_name(DCSYS.IXL_Overlap):  # a dedicated function for overlaps
        return _get_ovl_pos(obj_val)
    elif get_sh_name(obj_type) == get_sh_name(DCSYS.Quai):  # a dedicated function for platforms
        return _get_plt_pos(obj_val)
    elif get_sh_name(obj_type) == get_sh_name(DCSYS.Calib):  # a dedicated function for calibration bases
        return _get_calib_pos(obj_val)
    elif "Seg" in sh_attrs and "X" in sh_attrs:
        seg, x = get_dc_sys_values(obj_val, obj_sh.Seg, obj_sh.X)
        return seg, x
    elif "Limit" in sh_attrs:
        limits = list(get_dc_sys_zip_values(obj_val, obj_sh.Limit.Seg, obj_sh.Limit.X))
        return limits
    elif "Extremite" in sh_attrs:
        limits = list(get_dc_sys_zip_values(obj_val, obj_sh.Extremite.Seg, obj_sh.Extremite.X))
        return limits
    elif "From" in sh_attrs and "To" in sh_attrs:
        lim1 = get_dc_sys_values(obj_val, obj_sh.From.Seg, obj_sh.To.X)
        lim2 = get_dc_sys_values(obj_val, obj_sh.To.Seg, obj_sh.To.X)
        return [lim1, lim2]
    elif "De" in sh_attrs and "A" in sh_attrs:
        lim1 = get_dc_sys_values(obj_val, obj_sh.De.Seg, obj_sh.De.X)
        lim2 = get_dc_sys_values(obj_val, obj_sh.A.Seg, obj_sh.A.X)
        return [lim1, lim2]
    return None


def _get_ovl_pos(obj_val: dict[str]) -> list[tuple[str, float]]:
    rp_seg, rp_x = list(get_dc_sys_zip_values(obj_val, DCSYS.IXL_Overlap.ReleasePoint.Seg,
                                              DCSYS.IXL_Overlap.ReleasePoint.X))[0]
    vsp_seg, vsp_x = list(get_dc_sys_zip_values(obj_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Seg,
                                                DCSYS.IXL_Overlap.VitalStoppingPoint.X))[0]
    return [(rp_seg, rp_x), (vsp_seg, vsp_x)]


def _get_plt_pos(obj_val: dict[str]) -> list[tuple[str, float]]:
    limits = get_dc_sys_zip_values(obj_val, DCSYS.Quai.ExtremiteDuQuai.Seg, DCSYS.Quai.ExtremiteDuQuai.X)
    return limits


def _get_calib_pos(obj_val: dict[str]) -> list[tuple[str, float]]:
    start_tag, end_tag = get_dc_sys_values(obj_val, DCSYS.Calib.BaliseDeb, DCSYS.Calib.BaliseFin)
    return [get_obj_position(DCSYS.Bal, start_tag), get_obj_position(DCSYS.Bal, end_tag)]
