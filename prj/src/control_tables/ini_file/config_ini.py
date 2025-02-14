#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import configparser
from ...utils import *


__all__ = ["get_control_tables_template_info"]


CONFIG_INI_FILE_NAME = "control_tables_configuration.ini"
CONFIG_INI_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", CONFIG_INI_FILE_NAME))

ROUTE_INFORMATION = dict()
OVERLAP_INFORMATION = dict()


def get_control_tables_template_info() -> tuple[dict[str, dict[str, Union[str, bool]]],
                                            dict[str, dict[str, Union[str, bool]]]]:
    global ROUTE_INFORMATION, OVERLAP_INFORMATION

    if not ROUTE_INFORMATION or not OVERLAP_INFORMATION:
        _read_control_tables_ini_info()

    return ROUTE_INFORMATION, OVERLAP_INFORMATION


def _read_control_tables_ini_info():
    global ROUTE_INFORMATION, OVERLAP_INFORMATION

    print_section_title(f"Read {CONFIG_INI_FILE} file to get the Control Tables PDF format.")
    config = configparser.ConfigParser()
    config.read(CONFIG_INI_FILE, encoding="utf-8")

    print_log(f"Get the ROUTE Control Tables info.")
    route_control_table_config = config["route_control_table_config"]
    # route_name
    name, right = _split_ini_info(route_control_table_config, "route_name")
    ROUTE_INFORMATION["route_name"] = {"name": name, "right": right}
    # start_signal
    name, right = _split_ini_info(route_control_table_config, "start_signal")
    ROUTE_INFORMATION["start_signal"] = {"name": name, "right": right}
    # route_ivb_path
    name, right = _split_ini_info(route_control_table_config, "route_ivb_path")
    ROUTE_INFORMATION["route_ivb_path"] = {"name": name, "right": right}
    # route_switch_path
    name, right = _split_ini_info(route_control_table_config, "route_switch_path")
    ROUTE_INFORMATION["route_switch_path"] = {"name": name, "right": right}

    print_log(f"Get the OVERLAP Control Tables info.")
    overlap_control_table_config = config["overlap_control_table_config"]
    # overlap_name
    name, right = _split_ini_info(overlap_control_table_config, "overlap_name")
    OVERLAP_INFORMATION["overlap_name"] = {"name": name, "right": right}
    # associated_signal
    name, right = _split_ini_info(overlap_control_table_config, "associated_signal")
    OVERLAP_INFORMATION["associated_signal"] = {"name": name, "right": right}
    # ovl_ivb_path
    name, right = _split_ini_info(overlap_control_table_config, "ovl_ivb_path")
    OVERLAP_INFORMATION["ovl_ivb_path"] = {"name": name, "right": right}
    # ovl_switch_path
    name, right = _split_ini_info(overlap_control_table_config, "ovl_switch_path")
    OVERLAP_INFORMATION["ovl_switch_path"] = {"name": name, "right": right}


def _split_ini_info(control_table_config: configparser.SectionProxy, option: str) -> tuple[str, bool]:
    ini_info = control_table_config.get(option, "").strip()
    if not ini_info:
        print_error(f"No information given for {option}.")
        sys.exit(1)

    if not ":" in ini_info:
        print_error(f"No semicolon \":\" found inside {option}.")
        sys.exit(1)

    info_split = ini_info.split(":")
    name = info_split[0].strip()
    relative_location = info_split[1].strip().lower()
    if relative_location == "right":
        right = True
    elif relative_location == "down":
        right = False
    else:
        print_error(f"The relative position after the semicolon \":\" does not correspond "
                    f"to either \"right\" or \"down\".")
        sys.exit(1)

    print_log(f"\tEntry title for {option} is {name} and its relative position is {'right' if right else 'down'}.")
    return name, right
