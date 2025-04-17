#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["get_current_version", "get_line_name_and_version"]


DC_SYS_VERSION_CELL = "B6"


def _get_dc_sys_version() -> str:
    ws = open_menu_sheet()
    version = get_xl_cell_value(ws, cell=DC_SYS_VERSION_CELL)
    return version


def get_line_name_and_version() -> str:
    line_dict = load_sheet(DCSYS.Ligne)
    line_value = list(line_dict.values())[0]
    line_name = get_dc_sys_value(line_value, DCSYS.Ligne.Nom)
    line_version = get_dc_sys_value(line_value, DCSYS.Ligne.Version)
    if line_version is None:
        return line_name
    if isinstance(line_version, float):
        if int(line_version) == line_version:
            line_version = int(line_version)
    return f"{line_name}__{line_version}"


def get_current_version() -> str:
    c_d470 = get_c_d470_version()
    if c_d470:
        return c_d470

    if get_dc_sys_folder():
        dc_sys_version = _get_dc_sys_version()
        if dc_sys_version and "_C_D470_" in dc_sys_version.upper():
            return dc_sys_version
        return get_line_name_and_version()

    c11_d470 = get_c11_d470_version()
    if c11_d470:
        return c11_d470

    c121_d470 = get_c121_d470_version()
    if c121_d470:
        return c121_d470

    return "PRJ"
