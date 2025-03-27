#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database import open_menu_sheet


__all__ = ["get_cctool_oo_name"]


CCTOOL_OO_VERSION_CELL = "A4"


def get_cctool_oo_name() -> str:
    ws = open_menu_sheet()
    version = get_xl_cell_value(ws, cell=CCTOOL_OO_VERSION_CELL)
    return version
