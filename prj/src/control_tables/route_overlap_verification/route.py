#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.route_utils import get_routes
from ...database_location import *
from ..load_control_tables import *
from ..control_tables_utils import *
from .common_utils import *


__all__ = ["check_route_control_tables"]


def check_route_control_tables(use_csv_file: bool = False):
    route_dict = get_routes()
    route_control_tables = load_control_tables(CONTROL_TABLE_TYPE.route, use_csv_file)

    print_title("Route verification...", color=Color.mint_green)
    missing_routes = list()
    result = True
    for route, route_val in route_dict.items():
        mid_result, missing_route = _check_route(route, route_val, route_control_tables)
        if mid_result is False:
            result = False
        if missing_route:
            missing_routes.append(missing_route)
    missing_routes_in_dc_sys = _check_routes_exist_in_dc_sys(route_dict, route_control_tables)
    if missing_routes_in_dc_sys:
        result = False

    result = print_route_overlap_results("route", result, len(route_dict), len(route_control_tables),
                                         missing_routes, missing_routes_in_dc_sys)
    return result


def _check_route(route: str, route_val: dict[str, str], route_control_tables: dict[str, dict]):
    route_control_table, table_name = _find_route_control_table(route, route_control_tables)
    if not route_control_table:
        return None, route
    control_sig = [route_control_table[key].upper().strip() for key in route_control_table.keys()
                   if any(key.startswith(key_id) for key_id in ROUTE_CONTROL_SIG_CONTROL_TABLE)][0]
    route_sw = [route_control_table[key].upper().strip() for key in route_control_table.keys()
                if key.startswith(ROUTE_SW_CONTROL_TABLE)][0]
    route_path = [route_control_table[key].upper().strip() for key in route_control_table.keys()
                  if key.startswith(ROUTE_PATH_CONTROL_TABLE)][0]

    result = True
    if _check_controlled_sig(route, route_val, control_sig, table_name) is False:
        result = False
    if _check_route_sw(route, route_val, route_sw, table_name) is False:
        result = False
    if _check_route_path(route, route_val, route_path, table_name) is False:
        result = False
    return result, None


def _find_route_control_table(route_dc_sys: str, route_control_tables: dict[str, dict[str, str]]):
    for route_control_table, route_val in route_control_tables.items():
        if _correspondence_route_control_table_dc_sys(route_control_table, route_dc_sys):
            return route_val, route_control_table
    for route_control_table, route_val in route_control_tables.items():
        if _correspondence_route_control_table_dc_sys(route_control_table, route_dc_sys, remove_zero=True):
            return route_val, route_control_table
    return {}, ""


def _correspondence_route_control_table_dc_sys(route_control_table, route_dc_sys, remove_zero: bool = False):
    if remove_zero is True:
        # try removing leading 0 in sig names
        route_dc_sys = "_".join([sig.removeprefix("0") for sig in route_dc_sys.split("_")])
        route_control_table = "_".join([sig.removeprefix("0") for sig in route_control_table.split("-")])

    route_dc_sys = "_".join([sig.upper() for sig in route_dc_sys.split("_")][-2:])
    route_control_table = "_".join([sig.upper() for sig in route_control_table.split("-")]).replace(" ", "")
    if route_dc_sys == route_control_table:
        return True
    # in some projects, the route in DC_SYS is named with 'S' in front of signals name
    test_route_control_table = "_".join(['S' + sig for sig in route_control_table.split("_")])
    if route_dc_sys == test_route_control_table:
        return True
    # in some projects, the route in DC_SYS is named with 'f' or 'F' in at the end of route name
    route_dc_sys = "_".join([sig.removesuffix("F") for sig in route_dc_sys.split("_")])
    if route_dc_sys == route_control_table or route_dc_sys == test_route_control_table:
        return True

    return False


def _check_controlled_sig(route: str, route_val: dict[str, Any], control_sig: str, table_name: str):
    dc_sys_origin_signal: str = get_dc_sys_value(route_val, DCSYS.Iti.SignalOrig)
    control_sig = control_sig.upper()
    sig_nb = dc_sys_origin_signal.split("_")[-1].upper()
    if sig_nb == control_sig:
        return True
    if sig_nb.removeprefix("S") == control_sig.removeprefix("S"):
        return True
    if sig_nb.removeprefix("0") == control_sig.removeprefix("0"):
        return True
    print_error(f"For Route {Color.green}{route}{Color.reset}, DC_SYS Origin Signal {Color.yellow}"
                f"{dc_sys_origin_signal}{Color.reset} does not correspond to the Control Table {Color.green}"
                f"{table_name}{Color.reset} where Controlled Signal is {Color.yellow}{control_sig}{Color.reset}.")
    return False


def _check_route_sw(route: str, route_val: dict[str, Any], route_sw: str, table_name: str):
    dc_sys_route_sw: list[str] = route_val['Route Switch']
    dc_sys_route_ivb: list[str] = [ivb.upper() for ivb in route_val["Route IVB"]]
    if route_sw == "--":
        route_sw_list = []
    else:
        route_sw_list = route_sw.split(",")
        route_sw_list = [sw.strip().removeprefix("0") for sw in route_sw_list]
        if PROJECT_NAME == Projects.Copenhagen or PROJECT_NAME == Projects.Thessaloniki:
            route_sw_list = [sw for sw in route_sw_list if len(sw) < 5]  # In Control Table, when on diamond crossing,
            # an extra switch appears with 4 digits (and the letter R or N at the end)
        elif PROJECT_NAME == Projects.Milan:
            route_sw_list = [sw for sw in route_sw_list if not sw.startswith("I") and not sw.startswith("SC")]
            # In Control Table, when on diamond crossing, an extra switch appears starting by an 'I' or 'SC'
        elif PROJECT_NAME == Projects.Riyadh:
            route_sw_list = [sw.replace("-", "") for sw in route_sw_list]  # In Control Table, there is a hyphen
            # in the switches name that does not appear in the DC_SYS

    result = True

    if len(route_sw_list) != len(dc_sys_route_sw):
        print_error(f"For Route {Color.green}{route}{Color.reset}, DC_SYS Route Switch does not have the same "
                    f"number of switches {Color.yellow}({len(dc_sys_route_sw)}){Color.reset} as in the Control Table "
                    f"{Color.green}{table_name}{Color.reset} {Color.yellow}({len(route_sw_list)}){Color.reset}.\n"
                    f"DC_SYS Route Switch: {Color.white}{', '.join(dc_sys_route_sw)}{Color.reset}\n"
                    f"Control Table Switch Route Path: {Color.beige}{route_sw}{Color.reset}\n"
                    f"{Color.default}DC_SYS Route IVB: {', '.join(dc_sys_route_ivb)}{Color.reset}")
        result = False
        return result

    for dc_sys_sw, control_table_sw in zip(dc_sys_route_sw, route_sw_list):
        if not dc_sys_sw.endswith(control_table_sw):
            dc_sys_route_sw_str = (f"{csi_bg_color(Color.yellow)}{Color.black}{dc_sys_sw}{Color.reset}"
                                   f"{Color.white}").join(", ".join(dc_sys_route_sw).split(dc_sys_sw))
            route_sw_str = (f"{csi_bg_color(Color.yellow)}{Color.black}{control_table_sw}{Color.reset}"
                            f"{Color.beige}").join(route_sw.split(control_table_sw))
            if any(sw.endswith(control_table_sw) for sw in dc_sys_route_sw):
                corresponding_sw = [sw for sw in dc_sys_route_sw if sw.endswith(control_table_sw)][0]
                dc_sys_route_sw_str = (f"{csi_bg_color(Color.light_red)}{Color.black}{corresponding_sw}"
                                       f"{Color.reset}{Color.white}").join(dc_sys_route_sw_str.split(corresponding_sw))
                print_warning(f"For Route {Color.green}{route}{Color.reset}, the order of the switches does not "
                              f"correspond to the Control Table {Color.green}{table_name}{Color.reset}:\n"
                              f"{Color.blue}{dc_sys_sw = }{Color.reset} does not correspond to "
                              f"{Color.blue}{control_table_sw = }{Color.reset}.\n"
                              f"DC_SYS Route Switch: {Color.white}{dc_sys_route_sw_str}{Color.reset}\n"
                              f"Control Table Switch Route Path: {Color.beige}{route_sw_str}{Color.reset}\n"
                              f"{Color.default}DC_SYS Route IVB: {', '.join(dc_sys_route_ivb)}{Color.reset}")
            else:
                print_error(f"For Route {Color.green}{route}{Color.reset}, switch {Color.blue}{dc_sys_sw = }"
                            f"{Color.reset} does not correspond to switch {Color.blue}{control_table_sw = }"
                            f"{Color.reset} in the Control Table {Color.green}{table_name}{Color.reset}.\n"
                            f"DC_SYS Route Switch: {Color.white}{dc_sys_route_sw_str}{Color.reset}\n"
                            f"Control Table Switch Route Path: {Color.beige}{route_sw_str}{Color.reset}\n"
                            f"{Color.default}DC_SYS Route IVB: {', '.join(dc_sys_route_ivb)}{Color.reset}")
            result = False

    return result


def _check_route_path(route: str, route_val: dict[str, Any], route_path: str, table_name: str):
    dc_sys_route_sw: list[str] = route_val["Route Switch"]
    dc_sys_route_ivb: list[str] = [ivb.upper() for ivb in route_val["Route IVB"]]
    if route_path == "--":
        route_path_list = []
    else:
        route_path_list = route_path.split(",")
        route_path_list = [ivb.strip().removeprefix("0") for ivb in route_path_list]
        route_path_list[0] = route_path_list[0].removeprefix("[").removesuffix("]")

    result = True

    if len(dc_sys_route_ivb) != len(route_path_list):
        print_error(f"For Route {Color.green}{route}{Color.reset}, DC_SYS Route IVB does not have the same "
                    f"number of IVBs {Color.yellow}({len(dc_sys_route_ivb)}){Color.reset} as in the Control Table "
                    f"{Color.green}{table_name}{Color.reset} {Color.yellow}({len(route_path_list)}){Color.reset}.\n"
                    f"DC_SYS Route IVB: {Color.white}{', '.join(dc_sys_route_ivb)}{Color.reset}\n"
                    f"Control Table Route Path: {Color.beige}{route_path}{Color.reset}\n"
                    f"{Color.default}DC_SYS Route Switch: {', '.join(dc_sys_route_sw)}{Color.reset}")
        result = False

    for dc_sys_ivb, control_table_ivb in zip(dc_sys_route_ivb, route_path_list):
        if not dc_sys_ivb.endswith(control_table_ivb):
            dc_sys_route_ivb_str = (f"{csi_bg_color(Color.yellow)}{Color.black}{dc_sys_ivb}{Color.reset}"
                                    f"{Color.white}").join(', '.join(dc_sys_route_ivb).split(dc_sys_ivb))
            route_path_str = (f"{csi_bg_color(Color.yellow)}{Color.black}{control_table_ivb}{Color.reset}"
                              f"{Color.beige}").join(route_path.split(control_table_ivb))
            if any(ivb.endswith(control_table_ivb) for ivb in dc_sys_route_ivb):
                corresponding_ivb = [ivb for ivb in dc_sys_route_ivb if ivb.endswith(control_table_ivb)][0]
                dc_sys_route_ivb_str = (f"{csi_bg_color(Color.light_red)}{Color.black}{corresponding_ivb}"
                                        f"{Color.reset}{Color.white}").join(dc_sys_route_ivb_str.split(
                                                                            corresponding_ivb))
                print_warning(f"For Route {Color.green}{route}{Color.reset}, the order of the IVBs does not "
                              f"correspond to the Control Table {Color.green}{table_name}{Color.reset}:\n"
                              f"{Color.blue}{dc_sys_ivb = }{Color.reset} does not correspond to "
                              f"{Color.blue}{control_table_ivb = }{Color.reset}.\n"
                              f"DC_SYS Route IVB: {Color.white}{dc_sys_route_ivb_str}{Color.reset}\n"
                              f"Control Table Route Path: {Color.beige}{route_path_str}{Color.reset}\n"
                              f"{Color.default}DC_SYS Route Switch: {', '.join(dc_sys_route_sw)}{Color.reset}")
            else:
                print_error(f"For Route {Color.green}{route}{Color.reset}, {Color.blue}{dc_sys_ivb = }{Color.reset} "
                            f"does not correspond to {Color.blue}{control_table_ivb = }{Color.reset} "
                            f"in the Control Table {Color.green}{table_name}{Color.reset}.\n"
                            f"DC_SYS Route IVB: {Color.white}{dc_sys_route_ivb_str}{Color.reset}\n"
                            f"Control Table Route Path: {Color.beige}{route_path_str}{Color.reset}\n"
                            f"{Color.default}DC_SYS Route Switch: {', '.join(dc_sys_route_sw)}{Color.reset}")
            result = False

    return result


def _check_routes_exist_in_dc_sys(route_dict: dict[str, Any], route_control_tables: dict[str, Any]):
    missing_routes_in_dc_sys = list()
    for route_control_table in route_control_tables.keys():
        if not _is_route_in_dc_sys(route_control_table, route_dict):
            missing_routes_in_dc_sys.append(route_control_table)
    return missing_routes_in_dc_sys


def _is_route_in_dc_sys(route_control_table: str, route_dict: dict[str, Any]):
    for route_dc_sys in route_dict.keys():
        if _correspondence_route_control_table_dc_sys(route_control_table, route_dc_sys):
            return True
    for route_dc_sys in route_dict.keys():
        if _correspondence_route_control_table_dc_sys(route_control_table, route_dc_sys, remove_zero=True):
            return True
    return False
