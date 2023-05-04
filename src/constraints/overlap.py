#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys import *
from ..control_tables import *
from ..database_loc import PROJECT_NAME, Projects

DESTINATION_POINT_CONTROL_TABLE = "[1]"
OVL_PATH_CONTROL_TABLE = "[5]"
OVL_SW_CONTROL_TABLE = "[8]"


def check_overlap_control_tables(use_csv_file: bool = False):
    ovl_dict = get_overlap()
    ovl_control_tables = parse_control_tables(CONTROL_TABLE_TYPE.overlap, use_csv_file)
    ovl_control_tables = {ovl.strip(): {key.strip(): val.strip() for key, val in ovl_val.items()}
                          for ovl, ovl_val in ovl_control_tables.items()}
    ovl_control_tables = _update_ovl_control_tables(ovl_control_tables)

    print_section_title("Overlap verification...\n")
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

    print_bar()
    print(f"Total number of Overlaps in DC_SYS: {Color.yellow}{len(ovl_dict)}{Color.reset}\n"
          f"Total number of Overlaps in Control Tables: {Color.yellow}{len(ovl_control_tables)}{Color.reset}\n")
    print_bar()
    if result is True and not (list_missing_ovl or list_missing_ovl_in_dc_sys):
        print_section_title("Result of Overlap verification:")
        print_success("Overlaps in DC_SYS correspond to the Control Tables.")
        return True
    if list_missing_ovl:
        print_section_title("Missing information for Overlap:")
        print_warning(f"The following {Color.yellow}{len(list_missing_ovl)}{Color.reset} overlaps "
                      f"in the DC_SYS are missing in the Control Tables:\n"
                      f"\t{Color.yellow}" + "\n\t".join(list_missing_ovl) + f"{Color.reset}")
    if list_missing_ovl_in_dc_sys:
        print_section_title("Exhaustiveness of Overlap:")
        print_warning(f"The following {Color.yellow}{len(list_missing_ovl_in_dc_sys)}{Color.reset} overlaps "
                      f"in the Control Tables are missing in the DC_SYS:\n"
                      f"\t{Color.yellow}" + "\n\t".join(list_missing_ovl_in_dc_sys) + f"{Color.reset}")
    print_section_title("\nResult of Overlap verification:")
    print_error("Overlaps in DC_SYS do not correspond to the Control Tables.")
    return False


def _check_ovl(ovl: str, ovl_val: dict[str, str], ovl_control_tables: dict[str, dict]):
    ovl_control_table, table_name = _find_ovl_control_table(ovl, ovl_control_tables)
    if not ovl_control_table:
        return None, ovl
    destination_point = [ovl_control_table[key].upper() for key in ovl_control_table.keys()
                         if key.startswith(DESTINATION_POINT_CONTROL_TABLE)][0]
    ovl_sw = [ovl_control_table[key].upper() for key in ovl_control_table.keys()
              if key.startswith(OVL_SW_CONTROL_TABLE)][0]
    ovl_path = [ovl_control_table[key].upper() for key in ovl_control_table.keys()
                if key.startswith(OVL_PATH_CONTROL_TABLE)][0]  # TODO use it to determine DC_SYS VSP

    result = True
    if _check_ovl_destination_point(ovl, ovl_val, destination_point, table_name) is False:
        result = False
    if _check_ovl_sw(ovl, ovl_val, ovl_sw, table_name) is False:
        result = False
    return result, None


def _find_ovl_control_table(ovl_dc_sys: str, ovl_control_tables: dict[str, dict[str, str]]):
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys):
            return ovl_val, ovl_control_table
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys,
                                                    test_with_ovl_pos=True, ovl_val=ovl_val):
            return ovl_val, ovl_control_table
    return {}, ""


def _correspondence_ovl_control_table_dc_sys(ovl_control_table: str, ovl_dc_sys: str,
                                             test_with_ovl_pos: bool = False, ovl_val: dict[str] = None):
    split_text = [sig.removeprefix("0") for sig in ovl_dc_sys.split("_")]
    end = split_text[-1]
    if len(end) > 2:
        ovl_dc_sys = end
    else:
        ovl_dc_sys = split_text[-2] + end
    split_text = ovl_control_table.split("-", 1)
    sig = split_text[0]
    if test_with_ovl_pos and PROJECT_NAME == Projects.Glasgow:
        end = split_text[1].removeprefix(sig).removeprefix("o").removesuffix("o")
        sig = "S" + sig
    elif test_with_ovl_pos and ovl_val["nb_occurrences"] == 1:
        sig = sig.removesuffix("N").removesuffix("R")
        end = ""
    elif test_with_ovl_pos and "ovl_pos" in ovl_val:
        end = ovl_val["ovl_pos"]
    else:
        end = split_text[1].removeprefix(sig).removeprefix("o").removesuffix("o")
    ovl_control_table = sig.removeprefix("0") + (end if end else "")
    return ovl_dc_sys == ovl_control_table


def _update_ovl_control_tables(ovl_control_tables: dict[str, dict[str]]):
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        ovl_sw = [ovl_val[key].upper() for key in ovl_val.keys() if key.startswith(OVL_SW_CONTROL_TABLE)][0]
        sig = ovl_control_table.split("-", 1)[0]
        list_occurrences = [key for key in ovl_control_tables if key.split("-", 1)[0] == sig]
        ovl_control_tables[ovl_control_table]["nb_occurrences"] = len(list_occurrences)
        if len(list_occurrences) == 2:
            if ovl_sw.endswith("N"):
                ovl_control_tables[ovl_control_table]["ovl_pos"] = "N"
            elif ovl_sw.endswith("R"):
                ovl_control_tables[ovl_control_table]["ovl_pos"] = "R"
    return ovl_control_tables


def _check_ovl_destination_point(ovl: str, ovl_val: dict[str], destination_point: str, table_name: str):
    ovl_cols_name = get_cols_name("overlap")
    dc_sys_destination_signal: str = ovl_val[ovl_cols_name['B']]
    if dc_sys_destination_signal.endswith(destination_point.removeprefix("0")):
        return True
    print_error(f"For Overlap {Color.green}{ovl}{Color.reset}, DC_SYS Destination Signal {Color.yellow}"
                f"{dc_sys_destination_signal}{Color.reset} does not correspond to the Control Table {Color.green}"
                f"{table_name}{Color.reset} where Destination Point is {Color.yellow}{destination_point}{Color.reset}.")
    return False


def _check_ovl_sw(ovl: str, ovl_val: dict[str], ovl_sw: str, table_name: str):
    dc_sys_ovl_sw: list[str] = ovl_val["Overlap Path Switch"]
    if ovl_sw == "--":
        ovl_sw_list = []
    else:
        ovl_sw_list = ovl_sw.split(",")
        ovl_sw_list = [sw.strip().removeprefix("0") for sw in ovl_sw_list]
        if PROJECT_NAME == Projects.Copenhagen or PROJECT_NAME == Projects.Thessaloniki:
            ovl_sw_list = [sw for sw in ovl_sw_list if len(sw) < 5]  # In Control Table, when on diamond crossing,
            # an extra switch appears with 4 digits (and the letter R or N at the end)
        elif PROJECT_NAME == Projects.Milan:
            ovl_sw_list = [sw for sw in ovl_sw_list if not sw.startswith('I') and not sw.startswith("SC")]
            # In Control Table, when on diamond crossing, an extra switch appears starting by an 'I' or 'SC'
        elif PROJECT_NAME == Projects.Riyadh:
            ovl_sw_list = [sw.replace("-", "") for sw in ovl_sw_list]  # In Control Table, there is a hyphen
            # in the switches name that does not appear in the DC_SYS

    result = True

    if len(ovl_sw_list) != len(dc_sys_ovl_sw):
        print_error(f"For Overlap {Color.green}{ovl}{Color.reset}, DC_SYS Overlap Switch does not have the same "
                    f"number of switches {Color.yellow}({len(dc_sys_ovl_sw)}){Color.reset} as in the Control Table "
                    f"{Color.green}{table_name}{Color.reset} {Color.yellow}({len(ovl_sw_list)}){Color.reset}.\n"
                    f"DC_SYS Overlap Switch: {Color.white}{', '.join(dc_sys_ovl_sw)}{Color.reset}\n"
                    f"Control Table Switch Overlap Path: {Color.white}{ovl_sw}{Color.reset}")
        result = False

    for dc_sys_sw, control_table_sw in zip(dc_sys_ovl_sw, ovl_sw_list):
        if not dc_sys_sw.endswith(control_table_sw):
            dc_sys_ovl_sw_str = f"{bg_color(Color.yellow)}{Color.black}{dc_sys_sw}{Color.reset}{Color.white}".join(
                ', '.join(dc_sys_ovl_sw).split(dc_sys_sw))
            ovl_sw_str = f"{bg_color(Color.yellow)}{Color.black}{control_table_sw}{Color.reset}{Color.white}".join(
                ovl_sw.split(control_table_sw))
            if any(sw.endswith(control_table_sw) for sw in dc_sys_ovl_sw):
                print_warning(f"For Overlap {Color.green}{ovl}{Color.reset}, the order of the switches does not "
                              f"correspond to the Control Table {Color.green}{table_name}{Color.reset}:\n"
                              f"{Color.blue}{dc_sys_sw=}{Color.reset} does not correspond to "
                              f"{Color.blue}{control_table_sw=}{Color.reset}.\n"
                              f"DC_SYS Overlap Switch: {Color.white}{dc_sys_ovl_sw_str}{Color.reset}\n"
                              f"Control Table Switch Overlap Path: {Color.white}{ovl_sw_str}{Color.reset}")
            else:
                print_error(f"For Overlap {Color.green}{ovl}{Color.reset}, switch {Color.blue}{dc_sys_sw=}"
                            f"{Color.reset} does not correspond to switch {Color.blue}{control_table_sw=}"
                            f"{Color.reset} in the Control Table {Color.green}{table_name}{Color.reset}.\n"
                            f"DC_SYS Overlap Switch: {Color.white}{dc_sys_ovl_sw_str}{Color.reset}\n"
                            f"Control Table Switch Overlap Path: {Color.white}{ovl_sw_str}{Color.reset}")
            result = False

    return result


def _check_ovl_exist_in_dc_sys(ovl_dict: dict[str], ovl_control_tables: dict[str]):
    missing_ovl_in_dc_sys = list()
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if not _is_ovl_in_dc_sys(ovl_control_table, ovl_val, ovl_dict):
            missing_ovl_in_dc_sys.append(ovl_control_table)
    return missing_ovl_in_dc_sys


def _is_ovl_in_dc_sys(ovl_control_table: str, ovl_val: dict[str], ovl_dict: dict[str]):
    for ovl_dc_sys in ovl_dict.keys():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys):
            return True
    for ovl_dc_sys in ovl_dict.keys():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys,
                                                    test_with_ovl_pos=True, ovl_val=ovl_val):
            return True
    return False
