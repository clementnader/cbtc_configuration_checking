#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.route_utils import get_routes
from ..load_control_tables import *
from ..control_tables_utils import *
from .common_utils import *
from .format_utils import *


__all__ = ["check_route_control_tables"]


def check_route_control_tables(use_csv_file: bool = True):
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
    control_sig = route_control_table[ROUTE_ORIGIN_SIGNAL_KEY].upper().strip()
    route_path = route_control_table[ROUTE_IVB_LIST_KEY].upper().strip()
    route_sw = route_control_table[ROUTE_SWITCHES_LIST_KEY].upper().strip()

    result = True
    if not _check_controlled_sig(route, route_val, control_sig, table_name):
        result = False
    if not _check_route_path(route, route_val, route_path, table_name):
        result = False
    if not _check_route_sw(route, route_val, route_sw, table_name):
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
    if remove_zero:
        # try removing leading 0 in sig names
        route_dc_sys = "_".join([sig.removeprefix("0") for sig in route_dc_sys.split("_")])
        route_control_table = "-".join([sig.removeprefix("0") for sig in route_control_table.split("-")])

    route_dc_sys = "_".join([sig.upper() for sig in route_dc_sys.split("_")])
    route_control_table = "_".join([sig.upper() for sig in route_control_table.split("-")]).replace(" ", "")
    if route_dc_sys.endswith(route_control_table):
        return True
    # in some projects, the route in DC_SYS is named with 'S' in front of signals name
    test_route_control_table = "_".join(["S" + sig for sig in route_control_table.split("_")])
    if route_dc_sys.endswith(test_route_control_table):
        return True
    # in some projects, the route in DC_SYS is named with 'f' or 'F' in at the end of route name
    route_dc_sys = "_".join([sig.removesuffix("F") for sig in route_dc_sys.split("_")])
    if route_dc_sys.endswith(route_control_table) or route_dc_sys.endswith(test_route_control_table):
        return True

    return False


def _check_controlled_sig(route: str, route_val: dict[str, Any], ct_control_sig: str, table_name: str) -> bool:
    dc_sys_origin_signal: str = get_dc_sys_value(route_val, DCSYS.Iti.SignalOrig)
    if are_signals_matching(ct_control_sig, dc_sys_origin_signal):
        return True

    print_error(f"For Route {Color.green}{route}{Color.reset}, DC_SYS Origin Signal {Color.yellow}"
                f"{dc_sys_origin_signal}{Color.reset} does not correspond to the Control Table {Color.green}"
                f"{table_name}{Color.reset} where Controlled Signal is {Color.yellow}{ct_control_sig}{Color.reset}.")
    return False


def _check_route_sw(route: str, route_val: dict[str, Any], ct_route_sw: str, table_name: str) -> bool:
    dc_sys_route_sw: list[str] = route_val["Route Switch"]
    dc_sys_route_ivb: list[str] = [ivb.upper() for ivb in route_val["Route IVB"]]
    ct_route_sw_list = get_control_tables_switch_list(ct_route_sw)

    result = True
    if len(ct_route_sw_list) != len(dc_sys_route_sw):
        print_error(f"For Route {Color.green}{route}{Color.reset}, DC_SYS Route Switch does not have the same "
                    f"number of switches {Color.yellow}({len(dc_sys_route_sw)}){Color.reset} as in the Control Table "
                    f"{Color.green}{table_name}{Color.reset} {Color.yellow}({len(ct_route_sw_list)}){Color.reset}.\n"
                    f"DC_SYS Route Switch: {Color.white}{', '.join(dc_sys_route_sw)}{Color.reset}\n"
                    f"Control Table Switch Route Path: {Color.beige}{ct_route_sw}{Color.reset}\n"
                    f"{Color.default}DC_SYS Route IVB: {', '.join(dc_sys_route_ivb)}{Color.reset}")
        result = False
        return result

    for dc_sys_sw, control_table_sw in zip(dc_sys_route_sw, ct_route_sw_list):
        if not are_sw_names_matching(control_table_sw, dc_sys_sw):
            dc_sys_route_sw_str = (f"{csi_bg_color(Color.yellow)}{Color.black}{dc_sys_sw}{Color.reset}"
                                   f"{Color.white}").join(", ".join(dc_sys_route_sw).split(dc_sys_sw))
            route_sw_str = (f"{csi_bg_color(Color.yellow)}{Color.black}{control_table_sw}{Color.reset}"
                            f"{Color.beige}").join(ct_route_sw.split(control_table_sw))
            if any(are_sw_names_matching(control_table_sw, sw) for sw in dc_sys_route_sw):
                corresponding_sw = [sw for sw in dc_sys_route_sw if are_sw_names_matching(control_table_sw, sw)][0]
                dc_sys_route_sw_str = (f"{csi_bg_color(Color.light_red)}{Color.black}{corresponding_sw}"
                                       f"{Color.reset}{Color.white}").join(dc_sys_route_sw_str.split(corresponding_sw))
                print_warning(f"For Route {Color.green}{route}{Color.reset}, the order of the switches does not "
                              f"correspond to the Control Table {Color.green}{table_name}{Color.reset}:\n"
                              f"{Color.blue}{dc_sys_sw = }{Color.reset} does not correspond to "
                              f"{Color.blue}{control_table_sw = }{Color.reset}.\n"
                              f"DC_SYS Route Switch: {Color.white}{dc_sys_route_sw_str}{Color.reset}{NBSP}\n"
                              f"Control Table Switch Route Path: {Color.beige}{route_sw_str}{Color.reset}{NBSP}\n"
                              f"{Color.default}DC_SYS Route IVB: {', '.join(dc_sys_route_ivb)}{Color.reset}")
            else:
                print_error(f"For Route {Color.green}{route}{Color.reset}, switch {Color.blue}{dc_sys_sw = }"
                            f"{Color.reset} does not correspond to switch {Color.blue}{control_table_sw = }"
                            f"{Color.reset} in the Control Table {Color.green}{table_name}{Color.reset}.\n"
                            f"DC_SYS Route Switch: {Color.white}{dc_sys_route_sw_str}{Color.reset}{NBSP}\n"
                            f"Control Table Switch Route Path: {Color.beige}{route_sw_str}{Color.reset}{NBSP}\n"
                            f"{Color.default}DC_SYS Route IVB: {', '.join(dc_sys_route_ivb)}{Color.reset}")
            result = False

    return result


def _check_route_path(route: str, route_val: dict[str, Any], ct_route_path: str, table_name: str) -> bool:
    dc_sys_route_sw: list[str] = route_val["Route Switch"]
    dc_sys_route_ivb: list[str] = [ivb.upper() for ivb in route_val["Route IVB"]]
    ct_route_path_list = get_control_tables_ivb_list(ct_route_path)

    result = True

    if len(dc_sys_route_ivb) != len(ct_route_path_list):
        print_error(f"For Route {Color.green}{route}{Color.reset}, DC_SYS Route IVB does not have the same "
                    f"number of IVBs {Color.yellow}({len(dc_sys_route_ivb)}){Color.reset} as in the Control Table "
                    f"{Color.green}{table_name}{Color.reset} {Color.yellow}({len(ct_route_path_list)}){Color.reset}.\n"
                    f"DC_SYS Route IVB: {Color.white}{', '.join(dc_sys_route_ivb)}{Color.reset}\n"
                    f"Control Table Route Path: {Color.beige}{ct_route_path}{Color.reset}\n"
                    f"{Color.default}DC_SYS Route Switch: {', '.join(dc_sys_route_sw)}{Color.reset}")
        result = False
        return result

    for dc_sys_ivb, control_table_ivb in zip(dc_sys_route_ivb, ct_route_path_list):
        if not dc_sys_ivb.endswith(control_table_ivb):
            dc_sys_route_ivb_str = (f"{csi_bg_color(Color.yellow)}{Color.black}{dc_sys_ivb}{Color.reset}"
                                    f"{Color.white}").join(", ".join(dc_sys_route_ivb).split(dc_sys_ivb))
            route_path_str = (f"{csi_bg_color(Color.yellow)}{Color.black}{control_table_ivb}{Color.reset}"
                              f"{Color.beige}").join(ct_route_path.split(control_table_ivb))
            if any(ivb.endswith(control_table_ivb) for ivb in dc_sys_route_ivb):
                corresponding_ivb = [ivb for ivb in dc_sys_route_ivb if ivb.endswith(control_table_ivb)][0]
                dc_sys_route_ivb_str = (f"{csi_bg_color(Color.light_red)}{Color.black}{corresponding_ivb}"
                                        f"{Color.reset}{Color.white}").join(dc_sys_route_ivb_str.split(
                                                                            corresponding_ivb))
                print_warning(f"For Route {Color.green}{route}{Color.reset}, the order of the IVBs does not "
                              f"correspond to the Control Table {Color.green}{table_name}{Color.reset}:\n"
                              f"{Color.blue}{dc_sys_ivb = }{Color.reset} does not correspond to "
                              f"{Color.blue}{control_table_ivb = }{Color.reset}.\n"
                              f"DC_SYS Route IVB: {Color.white}{dc_sys_route_ivb_str}{Color.reset}{NBSP}\n"
                              f"Control Table Route Path: {Color.beige}{route_path_str}{Color.reset}{NBSP}\n"
                              f"{Color.default}DC_SYS Route Switch: {', '.join(dc_sys_route_sw)}{Color.reset}")
            else:
                print_error(f"For Route {Color.green}{route}{Color.reset}, {Color.blue}{dc_sys_ivb = }{Color.reset} "
                            f"does not correspond to {Color.blue}{control_table_ivb = }{Color.reset} "
                            f"in the Control Table {Color.green}{table_name}{Color.reset}.\n"
                            f"DC_SYS Route IVB: {Color.white}{dc_sys_route_ivb_str}{Color.reset}{NBSP}\n"
                            f"Control Table Route Path: {Color.beige}{route_path_str}{Color.reset}{NBSP}\n"
                            f"{Color.default}DC_SYS Route Switch: {', '.join(dc_sys_route_sw)}{Color.reset}")
            result = False

    return result


def _check_routes_exist_in_dc_sys(route_dict: dict[str, Any], route_control_tables: dict[str, Any]):
    missing_routes_in_dc_sys = list()
    for route_control_table in route_control_tables:
        if not _is_route_in_dc_sys(route_control_table, route_dict):
            missing_routes_in_dc_sys.append(route_control_table)
    return missing_routes_in_dc_sys


def _is_route_in_dc_sys(route_control_table: str, route_dict: dict[str, Any]):
    for route_dc_sys in route_dict:
        if _correspondence_route_control_table_dc_sys(route_control_table, route_dc_sys):
            return True
    for route_dc_sys in route_dict:
        if _correspondence_route_control_table_dc_sys(route_control_table, route_dc_sys, remove_zero=True):
            return True
    return False
