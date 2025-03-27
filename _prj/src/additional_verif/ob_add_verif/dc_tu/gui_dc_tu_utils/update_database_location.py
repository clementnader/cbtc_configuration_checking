#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .....utils import *
from .....database_location import *


__all__ = ["update_database_loc"]


def update_database_loc(c11_d470_directory: tkinter.StringVar):
    DATABASE_LOC.kit_c11_dir = c11_d470_directory.get()
