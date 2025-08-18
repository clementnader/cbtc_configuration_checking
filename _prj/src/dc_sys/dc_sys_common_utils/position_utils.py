#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .common_utils import *
from .switch_utils import *
from .segments_utils import get_correct_seg_offset
from .plt_osp_utils import *


__all__ = ["get_object_position", "get_obj_zone_limits",
           "remove_common_limits_of_oriented_limits"]


def get_object_position(obj_type, obj_name: str) -> Union[tuple[str, float],
                                                          tuple[str, float, str],
                                                          list[tuple[str, float]],
                                                          list[tuple[str, float, str]], None]:
    """
    Returns the position of an object:
        - if it is a point, returns a tuple (segment, offset) and if this point is oriented, returns its oriented
        position (segment, offset, direction)
        - if it is a zone, returns a list of its extremities (segment, offset) and if these extremities are oriented,
        returns a list of its oriented extremities (segment, offset, direction)
    :param obj_type: type of the object, using DCSYS class attributes
    :param obj_name: name of the object
    :return: tuple[str, float] for point object, list[tuple[str, float]] for non-oriented zone object,
     list[tuple[str, float, str]] for oriented zone object, None if it was unable to find the position
    """
    obj_type = get_sh_name(obj_type)

    # Objects with no direct corresponding DC_SYS sheet
    if ("Sig" in get_class_attr_dict(DCSYS) and "DistPap" in get_class_attr_dict(DCSYS.Sig)
            and obj_type == get_sh_name(DCSYS.Sig.DistPap)):
        # a dedicated function for signal VSP
        return _get_vsp_position(obj_name)

    if ("IXL_Overlap" in get_class_attr_dict(DCSYS) and "VitalStoppingPoint" in get_class_attr_dict(DCSYS.IXL_Overlap)
            and obj_type == get_sh_name(DCSYS.IXL_Overlap.VitalStoppingPoint)):
        # a dedicated function for IXL Overlap VSP
        return _get_ixl_ovl_vsp_position(obj_name)

    if ("IXL_Overlap" in get_class_attr_dict(DCSYS) and "ReleasePoint" in get_class_attr_dict(DCSYS.IXL_Overlap)
            and obj_type == get_sh_name(DCSYS.IXL_Overlap.ReleasePoint)):
        # a dedicated function for IXL Overlap Release Point
        return _get_ixl_ovl_release_point_position(obj_name)

    if ("Quai" in get_class_attr_dict(DCSYS) and "PointDArret" in get_class_attr_dict(DCSYS.Quai)
            and obj_type == get_sh_name(DCSYS.Quai.PointDArret)):
        # a dedicated function for platform OSP
        return _get_plt_osp_position(obj_name)

    limits = get_obj_zone_limits(obj_type, obj_name)  # zone object, we put it first to manage the zone subsets objects
    if limits is not None:
        return limits

    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = get_class_attr_dict(obj_sh).keys()

    if "Aig" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.Aig):
        # a dedicated function for switches
        return get_switch_position(obj_val)

    if "Seg" in sh_attrs and "X" in sh_attrs:  # one point object
        seg, x = get_dc_sys_values(obj_val, obj_sh.Seg, obj_sh.X)
        direction = _get_direction_of_point(obj_type, obj_name)
        if direction is not None:
            return seg, x, direction
        return seg, x

    return None


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
    """ Return the list of limits (seg, offset) or (seg, offset, direction) if the object is a zone
     else it returns None. """
    obj_type = get_sh_name(obj_type)

    # Zones with subsets
    if "PAS" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.PAS):
        # a dedicated function for ZC
        limits = _get_zc_oriented_limits(obj_name)
        return limits
    if "DCS_Elementary_Zones" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.DCS_Elementary_Zones):
        # a dedicated function for DCS Elementary Zones
        limits = _get_dcs_ez_oriented_limits(obj_name)
        return limits

    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = get_class_attr_dict(obj_sh).keys()

    if "Quai" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.Quai):
        # a dedicated function for platforms
        limits = _get_platform_oriented_limits(obj_val)
        return limits
    if "Seg" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.Seg):
        # a dedicated function for segments
        limits = _get_segment_oriented_limits(obj_val)
        return limits
    if "IXL_Overlap" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.IXL_Overlap):
        # a dedicated function for overlaps
        return _get_overlap_oriented_limits(obj_val)
    if "Calib" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.Calib):
        # a dedicated function for calibration bases
        return _get_calibration_base_oriented_limits(obj_val)

    if "Limit" in sh_attrs:
        limits = _get_obj_limits(obj_val, obj_sh.Limit)
        return limits
    if "Extremite" in sh_attrs:
        limits = _get_obj_limits(obj_val, obj_sh.Extremite)
        return limits
    if "ExtZsm" in sh_attrs:
        limits = _get_obj_limits(obj_val, obj_sh.ExtZsm)
        return limits
    if "OdometricZone" in sh_attrs:
        limits = _get_obj_limits(obj_val, obj_sh.OdometricZone)
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


def _get_obj_limits(obj_val: dict[str, Any], obj_limit_attr
                   ) -> Union[None, list[tuple[str, float]], list[tuple[str, float, str]]]:
    limits = _get_obj_oriented_limits(obj_val, obj_limit_attr)
    if limits is None:  # non-oriented limits
        limits = list(get_dc_sys_zip_values(obj_val, obj_limit_attr.Seg, obj_limit_attr.X))
    if not limits:
        return None
    return limits


def _get_obj_oriented_limits(obj_val: dict[str, Any], obj_limit_attr) -> Union[None, list[tuple[str, float, str]]]:
    limit_sub_attrs = get_class_attr_dict(obj_limit_attr).keys()
    if "Direction" in limit_sub_attrs:
        limits = list(get_dc_sys_zip_values(obj_val, obj_limit_attr.Seg, obj_limit_attr.X, obj_limit_attr.Direction))
    elif "Sens" in limit_sub_attrs:
        limits = list(get_dc_sys_zip_values(obj_val, obj_limit_attr.Seg, obj_limit_attr.X, obj_limit_attr.Sens))
    else:
        limits = None
    if not limits:
        return None
    return limits


def _get_platform_oriented_limits(plt_val) -> list[tuple[str, float, str]]:
    limits = list()
    for seg, x, direction in get_dc_sys_zip_values(plt_val, DCSYS.Quai.ExtremiteDuQuai.Seg,
                                                   DCSYS.Quai.ExtremiteDuQuai.X, DCSYS.Quai.ExtremiteDuQuai.SensExt):
        if direction == LineRelatedDirection.SENS_LIGNE:  # the downstream platform end, so the zone is upstream
            direction = Direction.DECROISSANT
        elif direction == LineRelatedDirection.SENS_OPPOSE:  # the upstream platform end, so the zone is downstream
            direction = Direction.CROISSANT
        limits.append((seg, x, direction))
    return limits


def _get_segment_oriented_limits(seg_val) -> list[tuple[str, float, str]]:
    seg_name = get_dc_sys_value(seg_val, DCSYS.Seg.Nom)
    seg_length = get_dc_sys_value(seg_val, DCSYS.Seg.Longueur)
    begin_limit = (seg_name, 0., Direction.CROISSANT)
    end_limit = (seg_name, seg_length, Direction.DECROISSANT)
    return [begin_limit, end_limit]


def _get_overlap_oriented_limits(obj_val: dict[str, Any]) -> list[tuple[str, float, str]]:
    vsp_direction = get_dc_sys_value(obj_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Sens)
    # The zone of the overlap is upstream the VSP and downstream the release point
    rp_seg, rp_x = get_dc_sys_values(obj_val, DCSYS.IXL_Overlap.ReleasePoint.Seg,
                                     DCSYS.IXL_Overlap.ReleasePoint.X)
    vsp_seg, vsp_x = get_dc_sys_values(obj_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Seg,
                                       DCSYS.IXL_Overlap.VitalStoppingPoint.X)
    return [(rp_seg, rp_x, get_reverse_direction(vsp_direction)), (vsp_seg, vsp_x, vsp_direction)]


def _get_calibration_base_oriented_limits(obj_val: dict[str, Any]) -> list[tuple[str, float]]:
    start_tag, end_tag = get_dc_sys_values(obj_val, DCSYS.Calib.BaliseDeb, DCSYS.Calib.BaliseFin)
    calib_direction = get_dc_sys_value(obj_val, DCSYS.Calib.SensCalib)
    return [(*get_object_position(DCSYS.Bal, start_tag), calib_direction),
            (*get_object_position(DCSYS.Bal, end_tag), get_reverse_direction(calib_direction))]


def _get_zc_oriented_limits(zc_name):
    zc_dict = load_sheet(DCSYS.PAS)
    # A ZC can be split between multiple ZC subsets for a matter of maximal number of limits.
    zc_subset_value_list = [zc for zc in zc_dict.values()
                            if get_dc_sys_value(zc, DCSYS.PAS.Nom) == zc_name]
    limits = list()
    for zc_subset_value in zc_subset_value_list:
        zc_subset_limit = _get_obj_oriented_limits(zc_subset_value, DCSYS.PAS.ExtremiteSuivi)
        limits.extend(zc_subset_limit)
    return remove_common_limits_of_oriented_limits(limits)


def _get_dcs_ez_oriented_limits(dcs_ez_name):
    dcs_ez_dict = load_sheet(DCSYS.DCS_Elementary_Zones)
    # A DCS Elementary Zone can be split between multiple DCS EZ subsets for a matter of maximal number of limits.
    dcs_ez_subset_value_list = [dcs_ez for dcs_ez in dcs_ez_dict.values()
                                if get_dc_sys_value(dcs_ez, DCSYS.DCS_Elementary_Zones.Name) == dcs_ez_name]
    limits = list()
    for dcs_ez_subset_value in dcs_ez_subset_value_list:
        dcs_ez_subset_limit = _get_obj_oriented_limits(dcs_ez_subset_value, DCSYS.DCS_Elementary_Zones.Limit)
        limits.extend(dcs_ez_subset_limit)
    return remove_common_limits_of_oriented_limits(limits)


def remove_common_limits_of_oriented_limits(limits: list[tuple[str, float, str]]) -> list[tuple[str, float, str]]:
    common_limits = list()

    for i, (seg1, x1, lim_dir1) in enumerate(limits):
        if (seg1, x1, get_reverse_direction(lim_dir1)) in limits[i+1:]:
            common_limits.append((seg1, x1))

    if not common_limits:
        return limits

    return [(seg, x, lim_dir) for (seg, x, lim_dir) in limits if (seg, x) not in common_limits]


def _get_vsp_position(sig_name: str) -> tuple[str, float, str]:
    sig_seg, sig_x, sig_direction = get_object_position(DCSYS.Sig, sig_name)
    sig_dict = load_sheet(DCSYS.Sig)
    vsp_dist = get_dc_sys_value(sig_dict[sig_name], DCSYS.Sig.DistPap)
    if vsp_dist is None:
        vsp_dist = 0
    vsp_dist = vsp_dist if sig_direction == Direction.CROISSANT else -vsp_dist
    vsp_seg, vsp_x = get_correct_seg_offset(sig_seg, sig_x + vsp_dist)
    return vsp_seg, vsp_x, sig_direction


def _get_ixl_ovl_vsp_position(ixl_ovl_name: str) -> tuple[str, float, str]:
    vsp_seg, vsp_x, vsp_direction = get_dc_sys_values(
        ixl_ovl_name, DCSYS.IXL_Overlap.VitalStoppingPoint.Seg, DCSYS.IXL_Overlap.VitalStoppingPoint.X,
        DCSYS.IXL_Overlap.VitalStoppingPoint.Sens)
    return vsp_seg, vsp_x, vsp_direction


def _get_ixl_ovl_release_point_position(ixl_ovl_name: str) -> tuple[str, float, str]:
    rp_seg, rp_x, rp_direction = get_dc_sys_values(
        ixl_ovl_name, DCSYS.IXL_Overlap.ReleasePoint.Seg, DCSYS.IXL_Overlap.ReleasePoint.X,
        DCSYS.IXL_Overlap.ReleasePoint.Sens)
    return rp_seg, rp_x, rp_direction


def _get_plt_osp_position(osp_name: str) -> tuple[str, float, str]:
    plt_value = get_plt_osp_value(osp_name)
    osp_value = [(seg, x, direction) for (name, seg, x, direction) in get_dc_sys_zip_values(
        plt_value, DCSYS.Quai.PointDArret.Name, DCSYS.Quai.PointDArret.Seg, DCSYS.Quai.PointDArret.X,
        DCSYS.Quai.PointDArret.SensAssocie) if name == osp_name][0]
    osp_seg, osp_x, osp_direction = osp_value
    return osp_seg, osp_x, osp_direction
