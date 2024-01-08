#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ...utils import *
from .get_cctool_oo_schema_info import *
from .create_cctool_oo_schema_info_file import *
from .create_cctool_oo_enum_lists_info_file import *


__all__ = ["regen_cctool_oo_schema_wrapper", "regenerate_cctool_oo_schema_info"]


def regen_cctool_oo_schema_wrapper(file_to_launch_full_address: str):
    print_title(f"CCTool-OO Schema Information", color=Color.mint_green)
    print(f"{Color.light_green}Select the CCTool-OO Schema compatible with your version.{Color.reset}\n")
    cctool_schema_window()
    regenerate_cctool_oo_schema_info()
    python_exe = sys.executable
    launch_cmd(f"{python_exe} \"{file_to_launch_full_address}\"")


def regenerate_cctool_oo_schema_info():
    cctool_oo_file = get_corresponding_cctool_oo_schema()
    if cctool_oo_file is None:
        return
    print_log("Regenerating the CCTool-OO Schema information files.")
    revision, comments = get_cctool_oo_version_info(cctool_oo_file)
    print(f"{Color.yellow}{'Revision: ' + revision}{Color.reset}\n"
          f"{Color.yellow}{'Comments: ' + comments}{Color.reset}\n")

    # Regenerate the CCTool-OO Schema Info class files to match the current version
    create_cctool_oo_schema_info_file()
    create_cctool_oo_enum_lists_info_file()
