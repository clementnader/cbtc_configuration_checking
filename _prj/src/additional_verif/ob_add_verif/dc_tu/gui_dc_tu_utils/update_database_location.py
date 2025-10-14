#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from .....utils import *
from .....database_location import *


__all__ = ["update_database_loc"]


def update_database_loc(c11_d470_directory: tkinter.StringVar):
    c11_d470_directory = c11_d470_directory.get().replace("/", os.path.sep)
    print_log(f"C11_D470 directory is {Color.default}\"{c11_d470_directory}\"{Color.reset}.")
    DATABASE_LOCATION.kit_c11_dir = c11_d470_directory
