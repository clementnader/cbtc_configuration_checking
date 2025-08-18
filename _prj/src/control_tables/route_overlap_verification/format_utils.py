#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


__all__ = ["get_control_tables_ivb_list", "get_control_tables_switch_list",
           "are_sw_names_matching", "are_signals_matching"]


def get_control_tables_ivb_list(ct_ivb_str: str) -> list[str]:
    if ct_ivb_str == "--":
        ct_ivb_list = []
    else:
        ct_ivb_list = [sw.strip() for sw in ct_ivb_str.split(",") if sw.strip()]
        ct_ivb_list[0] = ct_ivb_list[0].removeprefix("[").removesuffix("]")

    return ct_ivb_list


def get_control_tables_switch_list(ct_sw_str: str) -> list[str]:
    if ct_sw_str == "--":
        ct_sw_list = []
    else:
        ct_sw_list = [sw.strip() for sw in ct_sw_str.split(",") if sw.strip()]
        ct_sw_list = _remove_intersection_diamond_switch(ct_sw_list)

    return ct_sw_list


def _remove_intersection_diamond_switch(ct_sw_list: list[str]) -> list[str]:
    # Remove Central switch (Normal or Reverse)

    # It can end by CN or CR (see Chennai CMRL)
    ct_sw_list = [sw for sw in ct_sw_list
                  if not (re.match(r"^.*[0-9]+C[NR]$", sw) is not None)]
    # It can start by SC or I (see Milan ML4)
    ct_sw_list = [sw for sw in ct_sw_list
                  if not (re.match(r"^SC[0-9]+[NR]$", sw) is not None
                          or re.match(r"^I[0-9]+[NR]$", sw) is not None)]

    # if PROJECT_NAME == Projects.Copenhagen_KCR or PROJECT_NAME == Projects.Thessaloniki_TSK:
    #     ct_sw_list = [sw for sw in ovl_sw_list if len(sw) < 5]  # In Control Table, when on diamond crossing,
    #     # an extra switch appears with 4 digits (and the letter R or N at the end)
    # elif PROJECT_NAME == Projects.Milan_ML4:
    #     ct_sw_list = [sw for sw in ovl_sw_list if not sw.startswith("I") and not sw.startswith("SC")]
    #     # In Control Table, when on diamond crossing, an extra switch appears starting by an 'I' or 'SC'
    # elif PROJECT_NAME == Projects.Riyadh_RL3:
    #     ct_sw_list = [sw.replace("-", "") for sw in ovl_sw_list]  # In Control Table, there is a hyphen
    #     # in the switches name that does not appear in the DC_SYS

    return ct_sw_list


def are_sw_names_matching(ct_sw: str, dc_sys_sw: str) -> bool:
    ct_sw = ct_sw.strip()
    dc_sys_sw = dc_sys_sw.strip()
    if dc_sys_sw.endswith(ct_sw):
        return True

    # Remove leading zeros
    ct_sw = _remove_leading_zeros(ct_sw)
    dc_sys_sw = _remove_leading_zeros(dc_sys_sw)
    if dc_sys_sw.endswith(ct_sw):
        return True

    # Remove hyphens - for Riyadh project
    ct_sw = _remove_hyphens(ct_sw)
    dc_sys_sw = _remove_leading_zeros(dc_sys_sw)
    if dc_sys_sw.endswith(ct_sw):
        return True

    return False


def _remove_leading_zeros(name: str) -> str:
    return re.sub(r"([^1-9]*)0+([1-9])", r"\1\2", name)


def _remove_hyphens(name: str) -> str:
    return re.sub(r"(S[AM])-([0-9])", r"\1\2", name)


def are_signals_matching(ct_sig: str, dc_sys_sig: str) -> bool:
    ct_sig = ct_sig.upper()
    dc_sys_sig = dc_sys_sig.upper()
    if dc_sys_sig.endswith(ct_sig):
        return True
    # Remove leading S in the signal name, sometimes it's only the number that is used on one side
    if dc_sys_sig.replace("_S", "_").endswith(ct_sig.removeprefix("S")):
        return True
    # Remove leading zeros in the signal name
    if dc_sys_sig.replace("_0", "_").endswith(ct_sig.removeprefix("0")):
        return True
    return False
