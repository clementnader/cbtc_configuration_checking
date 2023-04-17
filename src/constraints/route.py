#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys import *
from ..control_tables import *

CONTROL_SIG_CONTROL_TABLE = "[1]"
ROUTE_SW_CONTROL_TABLE = "[9]"
ROUTE_PATH_CONTROL_TABLE = "[10]"


def check_route_control_tables(use_csv_file: bool = False):
    route_dict = get_routes()
    route_control_tables = parse_control_tables(CONTROL_TABLE_TYPE.route, use_csv_file)

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

    print()
    if result is True and not (missing_routes or missing_routes_in_dc_sys):
        print_success("Routes in DC_SYS correspond to the Control Tables.")
        return True

    if missing_routes:
        print_warning(f"The following {len(missing_routes)} routes are missing in the Control Tables:\n"
                      f"\t{Color.yellow}" + "\n\t".join(missing_routes) + f"{Color.reset}")
    if missing_routes_in_dc_sys:
        print_warning(f"The following {len(missing_routes_in_dc_sys)} routes are missing in the DC_SYS:\n"
                      f"\t{Color.yellow}" + "\n\t".join(missing_routes_in_dc_sys) + f"{Color.reset}")
    print(f"\n{Color.beige}Final result of Route verification:{Color.reset}\n")
    print_error("Routes in DC_SYS do not correspond to the Control Tables.")
    return False


def _check_route(route: str, route_val: dict[str, str], route_control_tables: dict[str, dict]):
    route_control_table, table_name = _find_route_control_table(route, route_control_tables)
    if not route_control_table:
        return None, route
    control_sig = [route_control_table[key] for key in route_control_table.keys()
                   if key.startswith(CONTROL_SIG_CONTROL_TABLE)][0]
    route_sw = [route_control_table[key] for key in route_control_table.keys()
                if key.startswith(ROUTE_SW_CONTROL_TABLE)][0]
    route_path = [route_control_table[key] for key in route_control_table.keys()
                  if key.startswith(ROUTE_PATH_CONTROL_TABLE)][0]

    result = True
    if _check_controlled_sig(route, route_val, control_sig, table_name) is False:
        result = False
    if _check_route_sw(route, route_val, route_sw, table_name) is False:
        result = False
    if _check_route_path(route, route_val, route_path, table_name) is False:
        result = False
    return result, None


def _find_route_control_table(route: str, route_control_tables: dict[str, dict[str, str]]):
    route = "_".join([sig.removeprefix("0") for sig in route.split("_")])
    for route_control_table, route_val in route_control_tables.items():
        route_control_table = "_".join([sig.removeprefix("0") for sig in route_control_table.split("-")])
        if route.endswith(route_control_table):
            return route_val, route_control_table
    return {}, ""


def _check_controlled_sig(route: str, route_val: dict[str], control_sig: str, table_name: str):
    route_cols_name = get_cols_name("route")
    dc_sys_origin_signal: str = route_val[route_cols_name['B']]
    if dc_sys_origin_signal.endswith(control_sig.removeprefix("0")):
        return True
    print_error(f"For Route {Color.turquoise}{route}{Color.reset}, the Origin Signal {dc_sys_origin_signal} "
                f"does not correspond to the Control Table {table_name} where the Controlled Signal is {control_sig}.")
    return False


def _check_route_sw(route: str, route_val: dict[str], route_sw: str, table_name: str):
    dc_sys_route_sw: list[str] = route_val['Route Switch']
    if route_sw == "--":
        route_sw_list = []
    else:
        route_sw_list = route_sw.split(",")
        route_sw_list = [sw.strip().removeprefix("0") for sw in route_sw_list]
        route_sw_list = [sw for sw in route_sw_list if len(sw) < 5]  # In Control Table, when on diamond crossing,
        # an extra switch appears with 4 digits (and the letter R or N at the end)

    result = True

    if len(route_sw_list) != len(dc_sys_route_sw):
        print_error(f"For Route {Color.turquoise}{route}{Color.reset}, DC_SYS Route Switch does not have the same "
                    f"number of switches ({len(route_sw_list)}) as in the Control Table {table_name} "
                    f"({len(dc_sys_route_sw)}).\n"
                    f"DC_SYS Route Switch: {Color.white}{dc_sys_route_sw}{Color.reset}\n"
                    f"Switch Route Path: {Color.white}{route_sw}{Color.reset}")
        result = False

    for dc_sys_sw, control_table_sw in zip(dc_sys_route_sw, route_sw_list):
        if not dc_sys_sw.endswith(control_table_sw):
            if any(sw.endswith(control_table_sw) for sw in dc_sys_route_sw):
                print_warning(f"For Route {Color.turquoise}{route}{Color.reset}, the order of the switches does not "
                              f"correspond to the Control Table {table_name}:\n"
                              f"{dc_sys_sw=} does not correspond to {control_table_sw=}.\n"
                              f"DC_SYS Route Switch: {Color.white}{dc_sys_route_sw}{Color.reset}\n"
                              f"Switch Route Path: {Color.white}{route_sw}{Color.reset}")
            else:
                print_error(f"For Route {Color.turquoise}{route}{Color.reset}, switch {dc_sys_sw=} does not "
                            f"correspond to switch {control_table_sw=} in the Control Table {table_name}.\n"
                            f"DC_SYS Route Switch: {Color.white}{dc_sys_route_sw}{Color.reset}\n"
                            f"Switch Route Path: {Color.white}{route_sw}{Color.reset}")
            result = False

    return result


def _check_route_path(route: str, route_val: dict[str], route_path: str, table_name: str):
    dc_sys_route_ivb: list[str] = route_val['Route IVB']
    if route_path == "--":
        route_path_list = []
    else:
        route_path_list = route_path.split(",")
        route_path_list = [sw.strip().removeprefix("0") for sw in route_path_list]
        route_path_list[0] = route_path_list[0].removeprefix("[").removesuffix("]")

    result = True

    if len(dc_sys_route_ivb) != len(route_path_list):
        print_error(f"For Route {Color.turquoise}{route}{Color.reset}, DC_SYS Route IVB does not have the same "
                    f"number of IVBs ({len(dc_sys_route_ivb)}) as in the Control Table {route_path_list} "
                    f"({len(route_path_list)}).\n"
                    f"DC_SYS Route IVB: {Color.white}{dc_sys_route_ivb}{Color.reset}\n"
                    f"Route Path: {Color.white}{route_path}{Color.reset}")
        result = False

    for dc_sys_ivb, control_table_ivb in zip(dc_sys_route_ivb, route_path_list):
        if not dc_sys_ivb.endswith(control_table_ivb):
            if any(ivb.endswith(control_table_ivb) for ivb in dc_sys_route_ivb):
                print_warning(f"For Route {Color.turquoise}{route}{Color.reset}, the order of the IVBs does not "
                              f"correspond to the Control Table {table_name}:\n"
                              f"{dc_sys_ivb=} does not correspond to {control_table_ivb=}.\n"
                              f"DC_SYS Route IVB: {Color.white}{dc_sys_route_ivb}{Color.reset}\n"
                              f"Route Path: {Color.white}{route_path}{Color.reset}")
            else:
                print_error(f"For Route {Color.turquoise}{route}{Color.reset}, {dc_sys_ivb=} does not "
                            f"correspond to {control_table_ivb=} in the Control Table {table_name}.\n"
                            f"DC_SYS Route IVB: {Color.white}{dc_sys_route_ivb}{Color.reset}\n"
                            f"Route Path: {Color.white}{route_path}{Color.reset}")
            result = False

    return result


def _check_routes_exist_in_dc_sys(route_dict: dict[str], route_control_tables: dict[str]):
    missing_routes_in_dc_sys = list()

    for route_name in route_control_tables.keys():
        if _is_route_in_dc_sys(route_name, route_dict) is False:
            missing_routes_in_dc_sys.append(route_name)

    return missing_routes_in_dc_sys


def _is_route_in_dc_sys(route_name: str, route_dict: dict[str]):
    route_name = "_".join([sig.removeprefix("0") for sig in route_name.split("-")])
    for route in route_dict.keys():
        route = "_".join([sig.removeprefix("0") for sig in route.split("_")])
        if route.endswith(route_name):
            return True
    return False
