#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point, get_zones_intersecting_zone, is_point_in_zone
from .line_section_utils import *
from .maz_utils import *


__all__ = ["is_point_in_zc", "get_zc_of_point", "get_zc_of_obj",
           "get_zc_managing_obj", "get_ls_managed_by_zc", "get_zc_managing_ls"]


def is_point_in_zc(zc_name: str, seg: str, x: float, direction: str = None) -> Optional[bool]:
    return is_point_in_zone(DCSYS.PAS, zc_name, seg, x, direction)


def get_zc_of_point(seg: str, x: float, direction: str = None) -> list[str]:
    return get_zones_on_point(DCSYS.PAS, seg, x, direction)


def _get_zc_of_traffic_stop(obj_name: str) -> list[str]:
    obj_dict = load_sheet(DCSYS.Traffic_Stop)
    obj_val = obj_dict[obj_name]
    list_zc = list()
    for plt_name in get_dc_sys_value(obj_val, DCSYS.Traffic_Stop.PlatformList.Name):
        list_zc.extend([zc_name for zc_name in get_zc_of_obj(DCSYS.Quai, plt_name) if zc_name not in list_zc])
    return list_zc


def _get_zc_of_overlap(obj_name: str) -> list[str]:
    # For a ZC to manage an overlap, it has to contain both RP and VSP
    position = get_obj_position(DCSYS.IXL_Overlap, obj_name)
    dict_zc_on_limits = dict()
    for seg, x, direction in position:
        zc_list = get_zc_of_point(seg, x, direction)
        if zc_list is None:
            print_error(f"Point {(seg, x, direction)} for overlap {obj_name} is on no ZC.")
            zc_list = []
        dict_zc_on_limits[(seg, x)] = zc_list

    list_zc = list()
    for zc_name in get_all_zc():
        if all(zc_name in zc_on_limit for zc_on_limit in dict_zc_on_limits.values()):
            list_zc.append(zc_name)
    return list_zc


def get_zc_of_obj(obj_type, obj_name: str) -> list[str]:
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Traffic_Stop):  # a dedicated function for traffic stops
        return _get_zc_of_traffic_stop(obj_name)
    if get_sh_name(obj_type) == get_sh_name(DCSYS.IXL_Overlap):  # a dedicated function for overlaps
        return _get_zc_of_overlap(obj_name)
    position = get_obj_position(obj_type, obj_name)
    if isinstance(position, tuple):
        list_zc = get_zc_of_point(*position)
        return list_zc if list_zc is not None else []
    if isinstance(position, list):
        list_zc = get_zones_intersecting_zone(DCSYS.PAS, obj_type, obj_name)
        return list_zc if list_zc is not None else []
    return []


def get_ls_managed_by_zc(zc_name: str) -> list[str]:
    zc_value = get_zc_value(zc_name)
    list_ls = get_dc_sys_value(zc_value, DCSYS.PAS.TronconsGeresParLePas.Troncon)
    return list_ls


def get_zc_managing_ls(ls_name: str) -> str:
    list_zc = list()
    for zc_name in get_all_zc():
        if ls_name in get_ls_managed_by_zc(zc_name):
            list_zc.append(zc_name)
    if not list_zc:
        print_error(f"Line Section {ls_name} is managed by no ZC.")
        sys.exit(1)
    if len(list_zc) > 1:
        print_error(f"Line Section {ls_name} is managed by multiple ZCs: {list_zc}.")
        sys.exit(1)
    return list_zc[0]


def _get_zc_managing_platform(plt_name: str) -> Optional[str]:
    plt_dict = load_sheet(DCSYS.Quai)
    ws_eqpt_dict = load_sheet(DCSYS.Wayside_Eqpt)
    related_ws_eqpt = get_dc_sys_value(plt_dict[plt_name], DCSYS.Quai.RelatedWaysideEquip)
    related_ws_eqpt_is_a_zc = (related_ws_eqpt is not None
                               and get_dc_sys_value(ws_eqpt_dict[related_ws_eqpt],
                                                    DCSYS.Wayside_Eqpt.Function.Zc) == YesOrNo.O)
    zc_name = related_ws_eqpt if related_ws_eqpt_is_a_zc else None
    return zc_name


def _get_zc_managing_signal(sig_name: str, sig_upstream_ivb: bool) -> Optional[str]:
    sig_dict = load_sheet(DCSYS.Sig)
    sig_value = sig_dict[sig_name]
    upstream_ivb = get_dc_sys_value(sig_value, DCSYS.Sig.IvbJoint.UpstreamIvb)
    downstream_ivb = get_dc_sys_value(sig_value, DCSYS.Sig.IvbJoint.DownstreamIvb)

    if sig_upstream_ivb:
        zc_name = _get_zc_managing_ivb(upstream_ivb)
    else:
        zc_name = _get_zc_managing_ivb(downstream_ivb)
    return zc_name


def _get_zc_managing_ivb(ivb_name: str) -> Optional[str]:
    ivb_dict = load_sheet(DCSYS.IVB)
    dedicated_zc = get_dc_sys_value(ivb_dict[ivb_name], DCSYS.IVB.ZcName)
    list_of_zc_covering_ivb = get_zc_of_obj(DCSYS.IVB, ivb_name)
    if dedicated_zc is None:  # some IVB are not sent to the IXL and thus don't have a dedicated ZC sending it
        if len(list_of_zc_covering_ivb) == 1:
            return list_of_zc_covering_ivb[0]
        print_warning(f"IVB {ivb_name} is not managed by a ZC and it is in overlay: {list_of_zc_covering_ivb}.")
        return None

    if dedicated_zc not in list_of_zc_covering_ivb:
        print_error(f"The dedicated ZC of {ivb_name} given in IVB sheet ({dedicated_zc}) does not cover the IVB.\n"
                    f"({list_of_zc_covering_ivb = })")
    return dedicated_zc


def _get_zc_managing_maz(maz_name: str) -> tuple[Optional[str], Optional[str]]:
    if not maz_name:
        return None, None
    ls = get_line_section_of_obj(DCSYS.Zaum, maz_name)[0]
    zc_name = get_zc_managing_ls(ls)
    info = f"{maz_name} -> {ls} -> {zc_name}"
    return zc_name, info


def _get_zc_managing_sw(sw_name: str) -> tuple[Optional[str], str]:
    ivb_on_switch = get_zones_on_point(DCSYS.IVB, *get_obj_position(DCSYS.Aig, sw_name))[0]
    zc_name = _get_zc_managing_ivb(ivb_on_switch)
    info = f"{sw_name} -> {ivb_on_switch} -> {zc_name}"
    return zc_name, info


def _get_zc_managing_platform_end(plt_name: str, plt_end: str) -> tuple[str, str]:
    ls = get_line_section_of_obj(DCSYS.Quai, plt_name, plt_end=plt_end)[0]
    zc_name = get_zc_managing_ls(ls)
    info = f"{plt_name}::{plt_end.upper()} -> {ls} -> {zc_name}"
    return zc_name, info


def _get_zc_managing_maz_on_zone(obj_type, obj_name: str) -> tuple[list[str], str]:
    """ Function that shall work for both GES, CBTC Protection Zones, Protection Zones and Traction Power Zones. """
    zone_limits = get_obj_position(obj_type, obj_name)
    maz_list = get_maz_of_extremities(zone_limits)
    zc_list = list()
    info_list = list()
    for maz in maz_list:
        zc_name, info = _get_zc_managing_maz(maz)
        if info is not None:
            info_list.append(info)

        if zc_name is not None and zc_name not in zc_list:
            zc_list.append(zc_name)
    return zc_list, "\n\t".join(info_list)


def get_zc_managing_obj(obj_type, obj_name: str, sig_upstream_ivb: bool = None, plt_end: str = None
                        ) -> tuple[list[str], Optional[str]]:
    # Platform End
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Quai) and plt_end in ["normal", "reverse"]:
        zc_name, info = _get_zc_managing_platform_end(obj_name, plt_end)
        return [zc_name], info
    # Platform
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Quai):
        zc_name = _get_zc_managing_platform(obj_name)
        return [zc_name], None
    # Signal
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Sig):
        zc_name = _get_zc_managing_signal(obj_name, sig_upstream_ivb)
        return [zc_name], None
    # Switch
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Aig):
        zc_name, info = _get_zc_managing_sw(obj_name)
        return [zc_name], info
    # IVB
    if get_sh_name(obj_type) == get_sh_name(DCSYS.IVB):
        zc_name = _get_zc_managing_ivb(obj_name)
        return [zc_name], None
    # MAZ
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Zaum):
        zc_name, info = _get_zc_managing_maz(obj_name)
        return [zc_name], info
    # GES, CBTC_Protection_Zone, Protection Zone and Traction Power Zone
    if (("GES" in get_class_attr_dict(DCSYS)
         and get_sh_name(obj_type) == get_sh_name(DCSYS.GES))
        or ("CBTC_Protection_Zone" in get_class_attr_dict(DCSYS)
            and get_sh_name(obj_type) == get_sh_name(DCSYS.CBTC_Protection_Zone))
        or ("Protection_Zone" in get_class_attr_dict(DCSYS)
            and get_sh_name(obj_type) == get_sh_name(DCSYS.Protection_Zone))
        or ("SS" in get_class_attr_dict(DCSYS)
            and get_sh_name(obj_type) == get_sh_name(DCSYS.SS))):
        # we need at least that the ZC managing the MAZ intersecting the zone is receiving the message
        return _get_zc_managing_maz_on_zone(obj_type, obj_name)

    list_zc = get_zc_of_obj(obj_type, obj_name)
    return list_zc, None
