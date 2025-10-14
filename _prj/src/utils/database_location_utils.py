#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..database_location import *


__all__ = ["get_dc_sys_folder", "get_c_d470_version", "get_c11_d470_version", "get_c121_d470_version"]


def get_dc_sys_folder():
    dc_sys_addr = DATABASE_LOCATION.dc_sys_addr
    if dc_sys_addr:
        return os.path.split(dc_sys_addr)[0]
    return ""


def get_dc_par_folder():
    dc_par_addr = DATABASE_LOCATION.dc_par_addr
    if dc_par_addr:
        return os.path.split(dc_par_addr)[0]
    return ""


def get_c_d470_version():
    dc_sys_folder = get_dc_sys_folder()
    dc_sys_version = _get_version_in_full_path(dc_sys_folder, "C_D470")
    if dc_sys_version:
        return dc_sys_version

    dc_par_folder = get_dc_par_folder()
    dc_par_version = _get_version_in_full_path(dc_par_folder, "C_D470")
    if dc_par_version:
        return dc_par_version

    return ""


def get_c11_d470_version():
    kit_c11_dir = DATABASE_LOCATION.kit_c11_dir
    return _get_version_in_full_path(kit_c11_dir, "C11_D470")


def get_c121_d470_version():
    kit_c121_d470_dir = DATABASE_LOCATION.kit_c121_d470_dir
    return _get_version_in_full_path(kit_c121_d470_dir, "C121_D470")


def _get_version_in_full_path(full_path: str, kit_name: str):
    if not full_path:
        return ""

    for directory in reversed(full_path.split(os.sep)):  # check at any upper levels in the path
        if f"_{kit_name}_" in directory.upper():
            return directory
    return ""
