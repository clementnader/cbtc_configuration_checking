#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


__all__ = ["get_control_tables_ivb_list", "get_control_tables_switch_list",
           "are_sw_names_matching", "are_signals_matching"]


def get_control_tables_ivb_list(ct_ivb_str: str) -> list[str]:
    if ct_ivb_str == "--":
        ct_ivb_list = []
    else:
        # ct_ivb_str = ct_ivb_str.removesuffix("*")
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
                  if (re.match(r"^.*[0-9]+C[NR]$", sw) is None)]
    # It can start by SC or I (see Milan ML4)
    ct_sw_list = [sw for sw in ct_sw_list
                  if (re.match(r"^SC[0-9]+[NR]$", sw) is None
                      and re.match(r"^I[0-9]+[NR]$", sw) is None)]

    # It can be a switch with 4 digits (plus N/R) (see KCR and TSK),
    # we test if there are switches with 4 digits and switches with length 2 digits (and optional D for depot)
    if (all((re.match(r"^1[0-9]{3}[NR]$", sw) is not None
                or re.match(r"^[0-9]{2}D*[NR]$", sw) is not None) for sw in ct_sw_list)
            and any((re.match(r"^1[0-9]{3}[NR]$", sw) is not None) for sw in ct_sw_list)
            and any((re.match(r"^[0-9]{2}D*[NR]$", sw) is not None) for sw in ct_sw_list)):
        ct_sw_list = [sw for sw in ct_sw_list if (re.match(r"^1[0-9]{3}[NR]$", sw) is None)]

    # It can be a switch with 2 digits or D plus 1 digit (plus N/R) (see CMRL),
    # we test if there are switches with 7 digits or more, and switches with length 2 digits
    if (all((re.match(r"^[A-Z]_PM[0-9]{4}[NR][1-9]*$", sw) is not None
                or re.match(r"^[0-9]{2}[NR]$", sw) is not None) for sw in ct_sw_list)
            and any((re.match(r"^[A-Z]_PM[0-9]{4}[NR][1-9]*$", sw) is not None) for sw in ct_sw_list)
            and any((re.match(r"^[0-9]{2}[NR]$", sw) is not None) for sw in ct_sw_list)):
        ct_sw_list = [sw for sw in ct_sw_list if (re.match(r"^[0-9]{2}[NR]$", sw) is None)]
    if (all((re.match(r"^[A-Z]_PM[0-9]{4}[NR][1-9]*$", sw) is not None
                or re.match(r"^D[0-9][NR]$", sw) is not None) for sw in ct_sw_list)
            and any((re.match(r"^[A-Z]_PM[0-9]{4}[NR][1-9]*$", sw) is not None) for sw in ct_sw_list)
            and any((re.match(r"^D[0-9][NR]$", sw) is not None) for sw in ct_sw_list)):
        ct_sw_list = [sw for sw in ct_sw_list if (re.match(r"^D[0-9][NR]$", sw) is None)]

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
