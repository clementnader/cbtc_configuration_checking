#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from .config_ini import *
from ..utils import *
from ..dc_sys import *
from ..database_location import DATABASE_LOC


__all__ = ["init_log", "init", "get_log_file_sub_python"]


def init_log():
    args = _set_up_parser()
    log_file_name = args.log_file_name
    if log_file_name is None:
        log_file_name = f"tool_log_{get_timestamp()}.log"
        if os.path.exists(log_file_name):
            os.remove(log_file_name)
        print_log(f"\nTool logs will be stored in {Color.white}{os.path.realpath(log_file_name)}{Color.reset}")
    return log_file_name, args


def _set_up_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-s", action="store_true", dest="skip_regen", default=False)
    parser.add_argument("-l", action="store", dest="log_file_name", default=None)
    return parser.parse_args()


def init(args, main_file: str, log_file_instance: Any, log_file_name: str):
    if args.skip_regen:
        skip_init = False
        update_config_info()
    else:
        print_title(f"Tool Initialization")
        update_cctool_oo()
        skip_init = not DATABASE_LOC.cctool_oo_schema

    # Initialization Commands
    if skip_init:
        update_config_info()
        print_title(f"Working on {Color.cyan}{get_current_version()}{Color.reset}\n"
                    f"{Color.orange}skipping the reloading of CCTool-OO Schema{Color.reset}")
    else:
        current_cctool_oo_version = get_ga_version_text()
        if args.skip_regen:
            pass
        else:
            regen_cctool_oo_schema_wrapper_no_gui(main_file,
                                                  log_file_instance=log_file_instance,
                                                  log_file_name=log_file_name)
        print_title(f"Working on {Color.cyan}{get_current_version()}{Color.reset}\n"
                    f"with CCTool-OO Schema version: "
                    f"{Color.pale_green}{current_cctool_oo_version}{Color.reset}")


def get_log_file_sub_python():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-l", action="store", dest="log_file_name", default=None)
    parser.add_argument("-g", action="store", dest="gui_default_directory", default=None)

    args = parser.parse_args()
    log_file_name = args.log_file_name
    gui_default_directory = args.gui_default_directory
    set_gui_initial_directory(gui_default_directory)

    return log_file_name
