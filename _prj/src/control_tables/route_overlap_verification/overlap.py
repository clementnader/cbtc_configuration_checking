#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.overlap_utils import get_overlap
from ...dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point
from ..load_control_tables import *
from ..control_tables_utils import *
from .common_utils import *
from .format_utils import *


__all__ = ["check_overlap_control_tables"]


def check_overlap_control_tables(use_csv_file: bool = True):
    ovl_dict = get_overlap()
    ovl_control_tables = load_control_tables(CONTROL_TABLE_TYPE.overlap, use_csv_file)
    ovl_control_tables = _update_ovl_control_tables_normal_reverse(ovl_control_tables)

    print_title("Overlap verification...", color=Color.mint_green)
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

    result = print_route_overlap_results("overlap", result, len(ovl_dict), len(ovl_control_tables),
                                         list_missing_ovl, list_missing_ovl_in_dc_sys)
    return result


def _check_ovl(ovl: str, ovl_val: dict[str, str], ovl_control_tables: dict[str, dict]):
    ovl_control_table, table_name = _find_ovl_control_table(ovl, ovl_control_tables)
    if not ovl_control_table:
        return None, ovl
    ct_destination_point = ovl_control_table[OVERLAP_SIGNAL_NAME_KEY].upper().strip()
    ct_ovl_path = ovl_control_table[OVERLAP_IVB_LIST_KEY].upper().strip()
    ct_ovl_sw = ovl_control_table[OVERLAP_SWITCHES_LIST_KEY].upper().strip()

    result = True
    if not _check_ovl_destination_point(ovl, ovl_val, ct_destination_point, table_name):
        result = False
    if not _check_ovl_path(ovl, ovl_val, ct_ovl_path, table_name):
        result = False
    if not _check_ovl_sw(ovl, ovl_val, ct_ovl_sw, ct_ovl_path, table_name):
        result = False
    return result, None


def _find_ovl_control_table(ovl_dc_sys: str, ovl_control_tables: dict[str, dict[str, str]]):
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys):
            return ovl_val, ovl_control_table
    # If failed, we try to associate the overlap names using the corresponding normal and reverse positions
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys, test_with_ovl_pos=True,
                                                    ovl_val=ovl_val):
            return ovl_val, ovl_control_table
    # If failed, we try to associate the overlap names being case-insensitive
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys, case_insensitive=True):
            return ovl_val, ovl_control_table
    # If failed, we try to associate the overlap names removing the leading zeros in the signal name
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys, remove_zero=True):
            return ovl_val, ovl_control_table
    return {}, ""


def _correspondence_ovl_control_table_dc_sys(ct_ovl: str, dc_sys_ovl: str,
                                             case_insensitive: bool = False, remove_zero: bool = False,
                                             test_with_ovl_pos: bool = False, ovl_val: dict[str, Any] = None):
    # Control Tables Overlap
    split_text = ct_ovl.split("-", 1)
    ct_sig = split_text[0]
    ct_ovl = split_text[1]

    if dc_sys_ovl.endswith(ct_ovl):
        return True

    if test_with_ovl_pos and ovl_val["nb_occurrences"] == 1:  # if there is only 1 overlap for this signal in DC_SYS,
        # we only consider the signal name as the overlap name
        ct_end = ""
    elif test_with_ovl_pos and "ovl_pos" in ovl_val:  # if there are 2 overlaps for this signal in DC_SYS,
        # we use the corresponding R/N suffix using the switch R/N position
        ct_end = ovl_val["ovl_pos"]
    else:
        # The IXL overlap name is signal-signalEND
        ct_end = ct_ovl.removeprefix(ct_sig).removeprefix("o").removesuffix("o")

    ct_ovl = ct_sig + (("_" + ct_end) if ct_end else "")

    if dc_sys_ovl.endswith(ct_ovl):
        return True

    if case_insensitive:
        # try removing leading 0 in sig names
        ct_ovl = ct_ovl.upper()
        dc_sys_ovl = dc_sys_ovl.upper()
        if dc_sys_ovl.endswith(ct_ovl):
            return True

    if remove_zero:
        # try removing leading 0 in sig names
        ct_ovl = ct_ovl.removeprefix("0")
        dc_sys_ovl = "_".join(sig.removeprefix("0") for sig in dc_sys_ovl.split("_"))
        if dc_sys_ovl.endswith(ct_ovl):
            return True
    return False


def _update_ovl_control_tables_normal_reverse(ovl_control_tables: dict[str, dict[str, Any]]):
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        ct_ovl_sw = ovl_val[OVERLAP_SWITCHES_LIST_KEY].upper().strip()
        ct_ovl_sw_list = get_control_tables_switch_list(ct_ovl_sw)

        sig = ovl_control_table.split("-", 1)[0]
        # Get all overlaps for this signal
        list_occurrences = [key for key in ovl_control_tables if key.split("-", 1)[0] == sig]
        ovl_control_tables[ovl_control_table]["nb_occurrences"] = len(list_occurrences)

        # In case there are 2 overlaps for this same signal, we try and find the normal and reverse one.
        if len(list_occurrences) == 2:
            if ct_ovl_sw_list[0].endswith("N"):
                ovl_control_tables[ovl_control_table]["ovl_pos"] = "N"
            elif ct_ovl_sw_list[0].endswith("R"):
                ovl_control_tables[ovl_control_table]["ovl_pos"] = "R"

    return ovl_control_tables


def _check_ovl_destination_point(ovl: str, ovl_val: dict[str, Any], ct_destination_point: str, table_name: str) -> bool:
    dc_sys_destination_signal: str = get_dc_sys_value(ovl_val, DCSYS.IXL_Overlap.DestinationSignal)
    if are_signals_matching(ct_destination_point, dc_sys_destination_signal):
        return True
    print_error(f"For Overlap {Color.green}{ovl}{Color.reset}, DC_SYS Destination Signal {Color.yellow}"
                f"{dc_sys_destination_signal}{Color.reset} does not correspond to the Control Table {Color.green}"
                f"{table_name}{Color.reset} where Destination Point is {Color.yellow}{ct_destination_point}{Color.reset}.")
    return False


def _check_ovl_sw(ovl: str, ovl_val: dict[str, Any], ct_ovl_sw: str, ct_ovl_path: str, table_name: str) -> bool:
    dc_sys_ovl_sw: list[str] = ovl_val["Overlap Path Switch"]
    ct_ovl_sw_list = get_control_tables_switch_list(ct_ovl_sw)

    result = True
    if len(ct_ovl_sw_list) != len(dc_sys_ovl_sw):
        dc_sys_ovl_sw_str = ", ".join(dc_sys_ovl_sw) if dc_sys_ovl_sw else "None"
        print_error(f"For Overlap {Color.green}{ovl}{Color.reset}, DC_SYS Overlap Switch does not have the same "
                    f"number of switches {Color.yellow}({len(dc_sys_ovl_sw)}){Color.reset} as in the Control Table "
                    f"{Color.green}{table_name}{Color.reset} {Color.yellow}({len(ct_ovl_sw_list)}){Color.reset}.\n"
                    f"DC_SYS Overlap Switch: {Color.white}{dc_sys_ovl_sw_str}{Color.reset}\n"
                    f"Control Table Switch Overlap Path: {Color.beige}{ct_ovl_sw}{Color.reset}"
                    f"\n{Color.default}Control Table Overlap IVB Path: {ct_ovl_path}")
        result = False
        return result

    for dc_sys_sw, control_table_sw in zip(dc_sys_ovl_sw, ct_ovl_sw_list):
        if not are_sw_names_matching(control_table_sw, dc_sys_sw):
            dc_sys_ovl_sw_str = f"{csi_bg_color(Color.yellow)}{Color.black}{dc_sys_sw}{Color.reset}{Color.white}".join(
                ", ".join(dc_sys_ovl_sw).split(dc_sys_sw))
            ovl_sw_str = f"{csi_bg_color(Color.yellow)}{Color.black}{control_table_sw}{Color.reset}{Color.white}".join(
                ct_ovl_sw.split(control_table_sw))
            if any(are_sw_names_matching(control_table_sw, sw) for sw in dc_sys_ovl_sw):
                corresponding_sw = [sw for sw in dc_sys_ovl_sw if are_sw_names_matching(control_table_sw, sw)][0]
                dc_sys_ovl_sw_str = (f"{csi_bg_color(Color.light_red)}{Color.black}{corresponding_sw}"
                                     f"{Color.reset}{Color.white}").join(dc_sys_ovl_sw_str.split(corresponding_sw))
                print_warning(f"For Overlap {Color.green}{ovl}{Color.reset}, the order of the switches does not "
                              f"correspond to the Control Table {Color.green}{table_name}{Color.reset}:\n"
                              f"{Color.blue}{dc_sys_sw = }{Color.reset} does not correspond to "
                              f"{Color.blue}{control_table_sw = }{Color.reset}.\n"
                              f"DC_SYS Overlap Switch: {Color.white}{dc_sys_ovl_sw_str}{Color.reset}{NBSP}\n"
                              f"Control Table Switch Overlap Path: {Color.beige}{ovl_sw_str}{Color.reset}{NBSP}"
                              f"\n{Color.default}Control Table Overlap IVB Path: {ct_ovl_path}")
            else:
                print_error(f"For Overlap {Color.green}{ovl}{Color.reset}, switch {Color.blue}{dc_sys_sw = }"
                            f"{Color.reset} does not correspond to switch {Color.blue}{control_table_sw = }"
                            f"{Color.reset} in the Control Table {Color.green}{table_name}{Color.reset}.\n"
                            f"DC_SYS Overlap Switch: {Color.white}{dc_sys_ovl_sw_str}{Color.reset}{NBSP}\n"
                            f"Control Table Switch Overlap Path: {Color.beige}{ovl_sw_str}{Color.reset}{NBSP}"
                            f"\n{Color.default}Control Table Overlap IVB Path: {ct_ovl_path}")
            result = False

    return result


def _check_ovl_path(ovl_name: str, ovl_val: dict[str, Any], ct_ovl_path: str, table_name: str) -> bool:
    result = True
    # dc_sys_ovl_sw: list[str] = ovl_val["Overlap Path Switch"]  # TODO use the switch to determine
    #                                                               which IVB limit is the correct one
    # dc_sys_sig = get_dc_sys_value(ovl_val, DCSYS.IXL_Overlap.DestinationSignal)
    # sig_dict = load_sheet(DCSYS.Sig)
    # sig_value = sig_dict[dc_sys_sig]
    # dc_sys_upstream_ivb = get_dc_sys_value(sig_value, DCSYS.Sig.IvbJoint.UpstreamIvb)
    # dc_sys_downstream_ivb = get_dc_sys_value(sig_value, DCSYS.Sig.IvbJoint.DownstreamIvb)

    # Work on DC_SYS
    vsp_seg = get_dc_sys_value(ovl_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Seg)
    vsp_x = round(get_dc_sys_value(ovl_val, DCSYS.IXL_Overlap.VitalStoppingPoint.X), 3)
    vsp_track = get_dc_sys_value(ovl_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Voie)
    vsp_kp = round(get_dc_sys_value(ovl_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Pk), 3)
    vsp_direction = get_dc_sys_value(ovl_val, DCSYS.IXL_Overlap.VitalStoppingPoint.Sens)
    ivb_on_vsp = _get_ivb_on_vsp(ovl_name, vsp_seg, vsp_x, vsp_direction)

    # Work on Control Table
    ovl_path_list = get_control_tables_ivb_list(ct_ovl_path)
    last_ivb = ovl_path_list[-1]
    corresponding_last_ivb = _get_corresponding_ivb(last_ivb)

    if ivb_on_vsp is None:
        print_error(f"VSP of Overlap {Color.green}{ovl_name}{Color.reset} is not in an IVB "
                    f"{Color.default}(it is at KP {vsp_kp} on track {vsp_track}){Color.reset}.")
        result = False
        ivb_downstream_vsp = None
    else:
        ivb_downstream_vsp = _get_ivb_on_vsp(ovl_name, vsp_seg, vsp_x, get_reverse_direction(vsp_direction), other=True)
        if ivb_downstream_vsp is None:  # end of track, VSP placed at end of last IVB
            ivb_downstream_vsp = "End of track"
        elif ivb_downstream_vsp == ivb_on_vsp:
            print_error(f"VSP of Overlap {Color.green}{ovl_name}{Color.reset} is not on a joint between two IVBs.\n"
                        f"It is inside {Color.white}{ivb_on_vsp}{Color.reset} "
                        f"{Color.default}(it is at KP {vsp_kp} on track {vsp_track}){Color.reset}.\n"
                        f"{Color.default}In Control Table {Color.green}{table_name}{Color.default}, "
                        f"the path is {Color.yellow}{ct_ovl_path = }{Color.default} "
                        f"(last IVB: {Color.beige}{last_ivb} -> {corresponding_last_ivb}{Color.default})")
            result = False

    if corresponding_last_ivb is None:
        print_error(f"For Overlap {Color.green}{ovl_name}{Color.reset}, corresponding to Control Table "
                    f"{Color.green}{table_name}{Color.reset},\n"
                    f"last IVB of the path {Color.yellow}{ct_ovl_path = }{Color.reset} is not found in the DC_SYS.\n"
                    f"Control Table Overlap last IVB: {Color.beige}{last_ivb} -> {corresponding_last_ivb}{Color.reset}"
                    f"\n{Color.default}DC_SYS Overlap last IVB: {Color.white}{ivb_on_vsp}{Color.reset} "
                    f"{Color.default}(on joint with {ivb_downstream_vsp})")
        result = False

    elif corresponding_last_ivb != ivb_on_vsp:
        print_error(f"For Overlap {Color.green}{ovl_name}{Color.reset}, corresponding to Control Table "
                    f"{Color.green}{table_name}{Color.reset},\n"
                    f"VSP {Color.blue}({vsp_seg}, {vsp_x}){Color.reset} does not correspond to the last IVB of "
                    f"the path {Color.yellow}{ct_ovl_path = }{Color.reset} in the Control Table.\n"
                    f"DC_SYS Overlap last IVB: {Color.white}{ivb_on_vsp}{Color.reset} "
                    f"{Color.default}(on joint with {ivb_downstream_vsp}){Color.reset}\n"
                    f"Control Table Overlap last IVB: {Color.beige}{last_ivb} -> {corresponding_last_ivb}{Color.reset}")
        result = False
    return result


def _get_ivb_on_vsp(ovl_name: str, vsp_seg: str, vsp_x: float, vsp_direction: str,
                    other: bool = False) -> Optional[str]:
    list_ivb_on_vsp = get_zones_on_point(DCSYS.IVB, vsp_seg, vsp_x, direction=vsp_direction)
    if not list_ivb_on_vsp:
        if not other:
            print_error(f"VSP of Overlap {ovl_name} is on no IVB.")
        return None
    if len(list_ivb_on_vsp) > 1:
        print_error(f"VSP {'of' if not other else 'downstream'} Overlap {ovl_name} is on multiple IVBs: "
                    f"{list_ivb_on_vsp}.")
        return None
    ivb_on_vsp = list_ivb_on_vsp[0]
    return ivb_on_vsp


def _get_corresponding_ivb(control_table_ivb: str) -> Optional[str]:
    ivb_dict = load_sheet(DCSYS.IVB)
    for ivb_name, ivb_val in ivb_dict.items():
        ivb_test_name = ivb_name.split("_")[-1]
        if ivb_test_name.upper() == control_table_ivb.upper():
            return ivb_name
    for ivb_name, ivb_val in ivb_dict.items():
        ivb_test_name = ivb_name.split("_")[-1]
        ivb_test_name = ivb_test_name.removeprefix("Ts").removeprefix("vTs")
        if ivb_test_name.upper() == control_table_ivb.upper():
            return ivb_name
    return None


def _check_ovl_exist_in_dc_sys(ovl_dict: dict[str, Any], ovl_control_tables: dict[str, Any]):
    missing_ovl_in_dc_sys = list()
    found_ovl = list()
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        result = _is_ovl_in_dc_sys(ovl_control_table, ovl_val, ovl_dict)
        if result is False:
            missing_ovl_in_dc_sys.append(ovl_control_table)
        else:
            if result is not None:
                found_ovl.append(result)
    found_ovl.sort()
    return missing_ovl_in_dc_sys


def _is_ovl_in_dc_sys(ovl_control_table: str, ovl_val: dict[str, Any], ovl_dict: dict[str, Any]):
    for ovl_dc_sys in ovl_dict:
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys):
            return None
    # If failed, we try to associate the overlap names using the corresponding normal and reverse positions
    for ovl_dc_sys in ovl_dict:
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys, test_with_ovl_pos=True,
                                                    ovl_val=ovl_val):
            return f"{ovl_dc_sys} -> {ovl_control_table}"
    # If failed, we try to associate the overlap names being case-insensitive
    for ovl_dc_sys in ovl_dict:
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys, case_insensitive=True):
            return None
    # If failed, we try to associate the overlap names removing the leading zeros in the signal name
    for ovl_dc_sys in ovl_dict:
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys, remove_zero=True):
            return None
    return False
