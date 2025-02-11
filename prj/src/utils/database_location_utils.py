#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..database_location import *


__all__ = ["get_dc_sys_folder", "get_c_d470_version", "get_c11_d470_version", "get_c121_d470_version"]


def get_dc_sys_folder():
    return os.path.split(DATABASE_LOC.dc_sys_addr)[0]


def get_dc_par_folder():
    return os.path.split(DATABASE_LOC.dc_par_addr)[0]


def get_c_d470_version():
    dc_sys_folder = get_dc_sys_folder()
    if dc_sys_folder:
        return os.path.split(dc_sys_folder)[-1]
    dc_par_folder = get_dc_par_folder()
    if dc_par_folder:
        return os.path.split(dc_par_folder)[-1]
    return ""


def get_c11_d470_version():
    kit_c11_dir = DATABASE_LOC.kit_c11_dir
    if kit_c11_dir:
        return os.path.split(kit_c11_dir)[-1]


def get_c121_d470_version():
    kit_c121_dir = DATABASE_LOC.kit_c121_d470_dir
    if kit_c121_dir:
        return os.path.split(kit_c121_dir)[-1]
