#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ...utils import *
from .get_cctool_oo_schema_info import *
from .create_cctool_oo_enum_lists_info_file import *
from .get_ga_version import *


__all__ = ["regenerate_cctool_oo_schema_info", "regen_cctool_oo_schema_wrapper", "regen_cctool_oo_schema_wrapper_no_gui"]


def regenerate_cctool_oo_schema_info():
    cctool_oo_file = get_corresponding_cctool_oo_schema()
    if cctool_oo_file is None:
        return
    print_log(f"Regenerating the CCTool-OO Schema information files\n"
              f"\tfrom {Color.default}\"{cctool_oo_file}\"{Color.reset}.")
    revision, comments = get_cctool_oo_version_info(cctool_oo_file)
    print(f"{Color.yellow}{'Revision: ' + revision}{Color.reset}\n"
          f"{Color.yellow}{'Comments: ' + comments}{Color.reset}\n")

    # Regenerate the CCTool-OO Schema Info class files to match the current version
    create_cctool_oo_schema_info_file()
    create_cctool_oo_enum_lists_info_file()


def regen_cctool_oo_schema_wrapper(file_to_launch_full_address: str,
                                   log_file_instance: Any = None, log_file_name: str = None):
    print_title(f"CCTool-OO Schema Information", color=Color.mint_green)
    print(f"{Color.light_green}Select the \"CCTool-OO Schema\" file compatible with your DC_SYS.{Color.reset}\n")
    cctool_oo_schema_window()
    gui_default_directory = get_gui_initial_directory()
    regenerate_cctool_oo_schema_info()

    # We relaunch the tool with a new python instance to take into account the regenerated CCTool-OO Schema files.
    python_exe = sys.executable
    if log_file_instance:
        log_file_instance.close()

    # we relaunch the new instance
    if log_file_name:
        launch_cmd(f"{python_exe} \"{file_to_launch_full_address}\" -l \"{log_file_name}\" "
                   f"-g \"{gui_default_directory}\"")
    else:
        launch_cmd(f"{python_exe} \"{file_to_launch_full_address}\" -g \"{gui_default_directory}\"")


def regen_cctool_oo_schema_wrapper_no_gui(file_to_launch: str,
                                          log_file_instance: Any = None, log_file_name: str = None):
    print()
    regenerate_cctool_oo_schema_info()

    # We relaunch the tool with a new python instance to take into account the regenerated CCTool-OO Schema files.
    print_log(f"Launch another Python instance to take into account the CCTool-OO Schema.")
    python_exe = sys.executable
    if log_file_instance:
        log_file_instance.close()

    # we relaunch the new instance
    if log_file_name:
        launch_cmd(f"\"{python_exe}\" \"{file_to_launch}\" -s -l \"{log_file_name}\"",
                   do_print=False)
    else:
        launch_cmd(f"\"{python_exe}\" \"{file_to_launch}\" -s",
                   do_print=False)
    # we exit the current instance
    exit(0)
