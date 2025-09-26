#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import configparser
from ...database_location import *
from ..control_tables_utils import *
from ...utils import *


__all__ = ["get_control_tables_template_info"]


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

    config_ini_file_name = DATABASE_LOC.control_tables_config_ini_file
    config_ini_file = os.path.join(ROOT_DIRECTORY, "control_tables_configuration", config_ini_file_name)

    print_section_title(f"Read \"{config_ini_file_name}\" file to get the Control Tables PDF format:")
    print("", config_ini_file)
    config = configparser.ConfigParser()
    config.read(config_ini_file, encoding="utf-8")

    print_log(f"Get the ROUTE Control Tables information:")
    route_control_table_config = config["route_control_table_config"]
    # route_name
    name, right = _split_ini_info(route_control_table_config, "route_name")
    ROUTE_INFORMATION["name"] = {"name": name, "right": right, "csv_name": ROUTE_NAME_KEY}
    # start_signal
    name, right = _split_ini_info(route_control_table_config, "start_signal")
    ROUTE_INFORMATION["start_signal"] = {"name": name, "right": right, "csv_name": ROUTE_ORIGIN_SIGNAL_KEY}
    # route_ivb_path
    name, right = _split_ini_info(route_control_table_config, "route_ivb_path")
    ROUTE_INFORMATION["route_ivb_path"] = {"name": name, "right": right, "csv_name": ROUTE_IVB_LIST_KEY}
    # route_switch_path
    name, right = _split_ini_info(route_control_table_config, "route_switch_path")
    ROUTE_INFORMATION["route_switch_path"] = {"name": name, "right": right, "csv_name": ROUTE_SWITCHES_LIST_KEY}

    print_log(f"Get the OVERLAP Control Tables information:")
    overlap_control_table_config = config["overlap_control_table_config"]
    # overlap_name
    name, right = _split_ini_info(overlap_control_table_config, "overlap_name")
    OVERLAP_INFORMATION["name"] = {"name": name, "right": right, "csv_name": OVERLAP_NAME_KEY}
    # associated_signal
    name, right = _split_ini_info(overlap_control_table_config, "associated_signal")
    OVERLAP_INFORMATION["associated_signal"] = {"name": name, "right": right, "csv_name": OVERLAP_SIGNAL_NAME_KEY}
    # overlap_ivb_path
    name, right = _split_ini_info(overlap_control_table_config, "overlap_ivb_path")
    OVERLAP_INFORMATION["overlap_ivb_path"] = {"name": name, "right": right, "csv_name": OVERLAP_IVB_LIST_KEY}
    # overlap_switch_path
    name, right = _split_ini_info(overlap_control_table_config, "overlap_switch_path")
    OVERLAP_INFORMATION["overlap_switch_path"] = {"name": name, "right": right, "csv_name": OVERLAP_SWITCHES_LIST_KEY}

    print()


def _split_ini_info(control_table_config: configparser.SectionProxy, option: str) -> tuple[str, bool]:
    ini_info = control_table_config.get(option, "").strip()
    if not ini_info:
        print_error(f"No information given for {option}.")
        exit(1)

    if not ":" in ini_info:
        print_error(f"No colon \":\" found inside {option}.")
        exit(1)

    info_split = ini_info.split(":")
    name = info_split[0].strip()
    relative_location = info_split[1].strip().lower()
    if relative_location == "right":
        right = True
    elif relative_location == "down":
        right = False
    else:
        print_error(f"The relative position after the colon \":\" does not correspond "
                    f"to either \"right\" or \"down\".")
        exit(1)

    print_log(f"\tAttribute name for {option} is {Color.default}\"{name}\"{Color.reset} "
              f"and its relative position is {Color.default}\"{'right' if right else 'down'}\"{Color.reset}.")
    return name, right
