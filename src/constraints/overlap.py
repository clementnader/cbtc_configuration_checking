#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys import *
from ..control_tables import *

DESTINATION_POINT_CONTROL_TABLE = "[1]"
OVL_PATH_CONTROL_TABLE = "[5]"
OVL_SW_CONTROL_TABLE = "[8]"


def check_overlap_control_tables(use_csv_file: bool = False):
    ovl_dict = get_overlap()
    ovl_control_tables = parse_control_tables(CONTROL_TABLE_TYPE.overlap, use_csv_file)

    list_missing_ovl = list()
    result = True
    for ovl, ovl_val in ovl_dict.items():
        mid_result, missing_ovl = _check_ovl(ovl, ovl_val, ovl_control_tables)
        if mid_result is False:
            result = False
        if missing_ovl:
            list_missing_ovl.append(missing_ovl)
    list_missing_ovl_in_dc_sys = _check_ovl_exist_in_dc_sys(ovl_dict, ovl_control_tables)
    if list_missing_ovl_in_dc_sys:
        result = False

    print(f"\n\n{Color.beige}Final result of Overlap verification:{Color.reset}\n")
    if result is True and not (list_missing_ovl or list_missing_ovl_in_dc_sys):
        print_success("Overlaps in DC_SYS correspond to the Control Tables.")
        return True

    if list_missing_ovl:
        print_warning(f"The following {len(list_missing_ovl)} overlaps are missing in the Control Tables:\n"
                      f"\t{Color.yellow}" + "\n\t".join(list_missing_ovl) + f"{Color.reset}")
    if list_missing_ovl_in_dc_sys:
        print_warning(f"The following {len(list_missing_ovl_in_dc_sys)} overlaps are missing in the DC_SYS:\n"
                      f"\t{Color.yellow}" + "\n\t".join(list_missing_ovl_in_dc_sys) + f"{Color.reset}")
    print_error("Overlaps in DC_SYS do not correspond to the Control Tables.")
    return False


def _check_ovl(ovl: str, ovl_val: dict[str, str], ovl_control_tables: dict[str, dict]):
    ovl_control_table, table_name = _find_ovl_control_table(ovl, ovl_control_tables)
    if not ovl_control_table:
        return None, ovl
    destination_point = [ovl_control_table[key] for key in ovl_control_table.keys()
                         if key.startswith(DESTINATION_POINT_CONTROL_TABLE)][0]
    ovl_sw = [ovl_control_table[key] for key in ovl_control_table.keys()
              if key.startswith(OVL_SW_CONTROL_TABLE)][0]
    ovl_path = [ovl_control_table[key] for key in ovl_control_table.keys()
                if key.startswith(OVL_PATH_CONTROL_TABLE)][0]

    result = True
    if _check_ovl_destination_point(ovl, ovl_val, destination_point, table_name) is False:
        result = False
    if _check_ovl_sw(ovl, ovl_val, ovl_sw, table_name) is False:
        result = False
    return result, None


def _find_ovl_control_table(ovl: str, ovl_control_tables: dict[str, dict[str, str]]):
    ovl = "_".join([sig.removeprefix("0") for sig in ovl.split("_")])
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        ovl_control_table = "_".join([sig.removeprefix("0") for sig in ovl_control_table.split("-")])
        if ovl.endswith(ovl_control_table):
            return ovl_val, ovl_control_table
    return {}, ""


def _check_ovl_destination_point(ovl: str, ovl_val: dict[str], destination_point: str, table_name: str):
    ovl_cols_name = get_cols_name("overlap")
    dc_sys_destination_signal: str = ovl_val[ovl_cols_name['B']]
    if dc_sys_destination_signal.endswith(destination_point.removeprefix("0")):
        return True
    print_error(f"For Overlap {Color.turquoise}{ovl}{Color.reset}, the Destination Signal {dc_sys_destination_signal} "
                f"does not correspond to the Control Table {table_name} where the Destination Point is "
                f"{destination_point}.")
    return False


def _check_ovl_sw(ovl: str, ovl_val: dict[str], ovl_sw: str, table_name: str):
    dc_sys_ovl_sw: list[str] = ovl_val["Overlap Path Switch"]
    if ovl_sw == "--":
        ovl_sw_list = []
    else:
        ovl_sw_list = ovl_sw.split(",")
        ovl_sw_list = [sw.strip().removeprefix("0") for sw in ovl_sw_list]
        ovl_sw_list = [sw for sw in ovl_sw_list if len(sw) < 5]  # In Control Table, when on diamond crossing,
        # an extra switch appears with 4 digits (and the letter R or N at the end)

    result = True

    if len(ovl_sw_list) != len(dc_sys_ovl_sw):
        print_error(f"For ovl {Color.turquoise}{ovl}{Color.reset}, DC_SYS ovl Switch does not have the same "
                    f"number of switches ({len(ovl_sw_list)}) as in the Control Table {table_name} "
                    f"({len(dc_sys_ovl_sw)}).\n"
                    f"DC_SYS ovl Switch: {Color.white}{dc_sys_ovl_sw}{Color.reset}\n"
                    f"Switch ovl Path: {Color.white}{ovl_sw}{Color.reset}")
        result = False

    for dc_sys_sw, control_table_sw in zip(dc_sys_ovl_sw, ovl_sw_list):
        if not dc_sys_sw.endswith(control_table_sw):
            if any(sw.endswith(control_table_sw) for sw in dc_sys_ovl_sw):
                print_warning(f"For ovl {Color.turquoise}{ovl}{Color.reset}, the order of the switches does not "
                              f"correspond to the Control Table {table_name}:\n"
                              f"{dc_sys_sw=} does not correspond to {control_table_sw=}.\n"
                              f"DC_SYS ovl Switch: {Color.white}{dc_sys_ovl_sw}{Color.reset}\n"
                              f"Switch ovl Path: {Color.white}{ovl_sw}{Color.reset}")
            else:
                print_error(f"For ovl {Color.turquoise}{ovl}{Color.reset}, switch {dc_sys_sw=} does not "
                            f"correspond to switch {control_table_sw=} in the Control Table {table_name}.\n"
                            f"DC_SYS ovl Switch: {Color.white}{dc_sys_ovl_sw}{Color.reset}\n"
                            f"Switch ovl Path: {Color.white}{ovl_sw}{Color.reset}")
            result = False

    return result


def _check_ovl_exist_in_dc_sys(ovl_dict: dict[str], ovl_control_tables: dict[str]):
    missing_ovl_in_dc_sys = list()

    for ovl_name in ovl_control_tables.keys():
        if _is_ovl_in_dc_sys(ovl_name, ovl_dict) is False:
            missing_ovl_in_dc_sys.append(ovl_name)

    return missing_ovl_in_dc_sys


def _is_ovl_in_dc_sys(ovl_name: str, ovl_dict: dict[str]):
    ovl_name = "_".join([sig.removeprefix("0") for sig in ovl_name.split("-")])
    for ovl in ovl_dict.keys():
        ovl = "_".join([sig.removeprefix("0") for sig in ovl.split("_")])
        if ovl.endswith(ovl_name):
            return True
    return False
