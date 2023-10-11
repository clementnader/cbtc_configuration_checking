#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_common_utils import *
from ..dc_sys_get_zones import *
from .line_section_utils import *
from .maz_utils import *


__all__ = ["get_all_zc", "is_point_in_zc", "get_zc_of_point", "get_zc_of_extremities", "get_zc_of_obj",
           "get_zc_managing_obj", "get_ls_managed_by_zc", "get_zc_managing_ls"]


def get_all_zc():
    zc_dict = load_sheet(DCSYS.PAS)
    return list(zc_dict.keys())


def is_point_in_zc(zc_name: str, seg: str, x: float, direction: str = None) -> Optional[bool]:
    return is_point_in_zone(DCSYS.PAS, zc_name, seg, x, direction)


def get_zc_of_point(seg: str, x: float, direction: str = None) -> list[str]:
    return get_zones_on_point(DCSYS.PAS, seg, x, direction)


def get_zc_of_extremities(limits: list[tuple[str, float]]) -> list[str]:
    return get_zones_of_extremities(DCSYS.PAS, limits)


def _get_zc_of_traffic_stop(obj_name: str) -> list[str]:
    obj_dict = load_sheet(DCSYS.Traffic_Stop)
    obj_val = obj_dict[obj_name]
    list_zc = list()
    for plt_name in get_dc_sys_value(obj_val, DCSYS.Traffic_Stop.PlatformList.Name):
        list_zc.extend([zc for zc in get_zc_of_obj(DCSYS.Quai, plt_name) if zc not in list_zc])
    return list_zc


def get_zc_of_obj(obj_type, obj_name: str) -> Optional[list[str]]:
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Traffic_Stop):  # a dedicated function for traffic stops
        return _get_zc_of_traffic_stop(obj_name)
    position = get_obj_position(obj_type, obj_name)
    if isinstance(position, tuple):
        return get_zc_of_point(*position)
    if isinstance(position, list):
        return get_zc_of_extremities(position)
    return None


def get_ls_managed_by_zc(zc_name: str) -> list[str]:
    zc_dict = load_sheet(DCSYS.PAS)
    list_ls = get_dc_sys_value(zc_dict[zc_name], DCSYS.PAS.TronconsGeresParLePas.Troncon)
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


def _get_zc_managing_signal(sig_name: str) -> tuple[str, str]:
    # sig_dict = load_sheet(DCSYS.Sig)
    # sig_value = sig_dict[sig_name]
    # sig_seg, sig_x = get_dc_sys_values(sig_value, DCSYS.Sig.Seg, DCSYS.Sig.X)
    # sig_direction = get_dc_sys_value(sig_value, DCSYS.Sig.Sens)
    # at a limit between two IVB, the signal is considered to belong to the IVB in rear

    # ivb_on_sig = get_zones_on_point(DCSYS.IVB, sig_seg, sig_x, direction=get_reverse_direction(sig_direction))
    # if not ivb_on_sig:
    #     print_error(f"Signal {sig_name} is on no IVB.")
    #     sys.exit(1)
    # if len(ivb_on_sig) > 1:
    #     print_error(f"Signal {sig_name} is on multiple IVBs: {ivb_on_sig}.")
    #     sys.exit(1)
    # ivb = ivb_on_sig[0]
    # zc = _get_zc_managing_ivb(ivb)

    ls = get_line_section_of_obj(DCSYS.Sig, sig_name)[0]
    zc = get_zc_managing_ls(ls)
    return zc, ls


def _get_zc_managing_ivb(ivb_name: str) -> str:
    ivb_dict = load_sheet(DCSYS.IVB)
    dedicated_zc = get_dc_sys_value(ivb_dict[ivb_name], DCSYS.IVB.ZcName)
    list_of_zc_covering_ivb = get_zc_of_obj(DCSYS.IVB, ivb_name)
    if dedicated_zc not in list_of_zc_covering_ivb:
        print_error(f"The dedicated ZC of {ivb_name} given in IVB sheet ({dedicated_zc}) does not cover the IVB.\n"
                    f"({list_of_zc_covering_ivb = })")
    return dedicated_zc


def _get_zc_managing_block(block_name: str) -> tuple[str, str]:
    ls = get_line_section_of_obj(DCSYS.CDV, block_name)[0]
    zc = get_zc_managing_ls(ls)
    return zc, ls


def _get_zc_managing_maz(maz_name: str) -> tuple[str, str]:
    ls = get_line_section_of_obj(DCSYS.Zaum, maz_name)[0]
    zc = get_zc_managing_ls(ls)
    return zc, ls


def _get_zc_managing_protection_zone(obj_type, obj_name: str) -> tuple[list[str], list[str]]:
    """ Function that shall work for both GES and Protection Zones. """
    pz_limits = get_obj_position(obj_type, obj_name)
    maz_list = get_maz_of_extremities(pz_limits)
    ls_list = list()
    zc_list = list()
    for maz in maz_list:
        zc, ls = _get_zc_managing_maz(maz)
        if ls not in ls_list:
            ls_list.append(ls)
        if zc not in zc_list:
            zc_list.append(zc)
    return zc_list, ls_list


def get_zc_managing_obj(obj_type, obj_name: str) -> tuple[Optional[list[str]], Optional[list[str]]]:
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Sig):
        zc, related_obj = _get_zc_managing_signal(obj_name)
        return [zc], [related_obj]

    if get_sh_name(obj_type) == get_sh_name(DCSYS.IVB):
        zc = _get_zc_managing_ivb(obj_name)
        return [zc], None

    if get_sh_name(obj_type) == get_sh_name(DCSYS.CDV):
        zc, related_obj = _get_zc_managing_block(obj_name)
        return [zc], [related_obj]

    if get_sh_name(obj_type) == get_sh_name(DCSYS.Zaum):
        zc, related_obj = _get_zc_managing_maz(obj_name)
        return [zc], [related_obj]

    if get_sh_name(obj_type) == get_sh_name(DCSYS.Protection_Zone):
        return _get_zc_managing_protection_zone(obj_type, obj_name)

    list_zc = get_zc_of_obj(obj_type, obj_name)
    return list_zc, None
