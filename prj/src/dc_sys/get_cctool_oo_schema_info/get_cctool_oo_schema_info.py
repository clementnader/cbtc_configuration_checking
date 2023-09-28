#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...database_location import *
from .get_version import *
from .load_cctool_oo_schema import *
from .load_cctool_oo_schema.load_xl import *


__all__ = ["get_corresponding_cctool_oo_schema", "load_cctool_oo_schema_info", "load_cctool_oo_enum_lists_info",
           "get_cctool_oo_version_info"]


CCTOOL_OO_SCHEMA_DIR = r"C:\Users\naderc\Documents\Documents GA\CCTool-OO Schema"

REVISION_SHEET = "Revision"


def load_cctool_oo_schema_info():
    cctool_oo_file = get_corresponding_cctool_oo_schema()
    if cctool_oo_file is None:
        return dict()
    info_dict = load_cctool_oo_schema(cctool_oo_file)
    return info_dict


def load_cctool_oo_enum_lists_info():
    cctool_oo_file = get_corresponding_cctool_oo_schema()
    if cctool_oo_file is None:
        return dict()
    info_dict = load_cctool_oo_enum_lists(cctool_oo_file)
    return info_dict


def get_corresponding_cctool_oo_schema():
    if DATABASE_LOC.cctool_oo_schema != "":
        return DATABASE_LOC.cctool_oo_schema

    version = get_cctool_oo_version()
    for file in os.listdir(CCTOOL_OO_SCHEMA_DIR):
        full_path = os.path.join(CCTOOL_OO_SCHEMA_DIR, file)
        file, ext = os.path.splitext(file)
        if os.path.isfile(full_path) and ext == ".xls":
            if file.endswith(version):
                return full_path
    print_error(f"Unable to find the CCTool-OO Schema file for version {version} in directory {CCTOOL_OO_SCHEMA_DIR}")
    return None


def get_cctool_oo_version_info(cctool_oo_file):
    wb = load_cctool_oo_schema_wb(cctool_oo_file)
    revision_sh = wb.sheet_by_name(REVISION_SHEET)
    for line in range(get_xl_ws_number_of_rows(revision_sh) + 1, 0, -1):
        cell_value = get_xl_cell_value(revision_sh, row=line, column=4)
        if cell_value is not None:
            return cell_value
    return ""
