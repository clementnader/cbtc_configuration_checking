#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..database_location import *


__all__ = ["get_c_d470_version", "get_c11_d470_version", "get_c121_d470_version"]


def get_c_d470_version():
    return os.path.split(os.path.split(DATABASE_LOC.dc_sys_addr)[0])[-1]


def get_c11_d470_version():
    return os.path.split(DATABASE_LOC.kit_c11_dir)[-1]


def get_c121_d470_version():
    return os.path.split(DATABASE_LOC.kit_c121_d470_dir)[-1]
