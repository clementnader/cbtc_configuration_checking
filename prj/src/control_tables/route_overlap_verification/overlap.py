#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.overlap_utils import get_overlap
from ...dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point
from ...database_location import *
from ..load_control_tables import *
from ..control_tables_utils import *
from .common_utils import *


__all__ = ["check_overlap_control_tables"]


def check_overlap_control_tables(use_csv_file: bool = False):
    ovl_dict = get_overlap()
    ovl_control_tables = load_control_tables(CONTROL_TABLE_TYPE.overlap, use_csv_file)
    ovl_control_tables = _update_ovl_control_tables(ovl_control_tables)

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
    destination_point = [ovl_control_table[key].upper() for key in ovl_control_table.keys()
                         if key.startswith(OVL_DESTINATION_POINT_CONTROL_TABLE)][0]
    ovl_sw = [ovl_control_table[key].upper() for key in ovl_control_table.keys()
              if key.startswith(OVL_SW_CONTROL_TABLE)][0]
    ovl_path = [ovl_control_table[key].upper() for key in ovl_control_table.keys()
                if key.startswith(OVL_PATH_CONTROL_TABLE)][0]  # TODO use it to determine DC_SYS VSP

    result = True
    if _check_ovl_destination_point(ovl, ovl_val, destination_point, table_name) is False:
        result = False
    if _check_ovl_sw(ovl, ovl_val, ovl_sw, ovl_path, table_name) is False:
        result = False
    if _check_ovl_path(ovl, ovl_val, ovl_path, table_name) is False:
        result = False
    return result, None


def _find_ovl_control_table(ovl_dc_sys: str, ovl_control_tables: dict[str, dict[str, str]]):
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys):
            return ovl_val, ovl_control_table
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys, remove_zero=True):
            return ovl_val, ovl_control_table
    for ovl_control_table, ovl_val in ovl_control_tables.items():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys,
                                                    test_with_ovl_pos=True, ovl_val=ovl_val):
            return ovl_val, ovl_control_table
    return {}, ""


def _correspondence_ovl_control_table_dc_sys(ovl_control_table: str, ovl_dc_sys: str, remove_zero: bool = False,
                                             test_with_ovl_pos: bool = False, ovl_val: dict[str, Any] = None):
    if remove_zero is True:
        # try removing leading 0 in sig names
        split_text = [sig.removeprefix("0") for sig in ovl_dc_sys.split("_")]
    else:
        split_text = [sig for sig in ovl_dc_sys.split("_")]
    end = split_text[-1]
    if len(end) > 2:
        ovl_dc_sys = end
    else:
        ovl_dc_sys = split_text[-2] + end
    split_text = ovl_control_table.split("-", 1)
    sig = split_text[0]
    if test_with_ovl_pos and PROJECT_NAME.startswith("Glasgow"):
        end = split_text[1].removeprefix(sig).removeprefix("o").removesuffix("o")
        sig = "S" + sig
    elif test_with_ovl_pos and ovl_val["nb_occurrences"] == 1:
        sig = sig.removesuffix("N").removesuffix("R")
        end = ""
    elif test_with_ovl_pos and "ovl_pos" in ovl_val:
        end = ovl_val["ovl_pos"]
    else:
        end = split_text[1].removeprefix(sig).removeprefix("o").removesuffix("o")

    if remove_zero is True:
        # try removing leading 0 in sig names
        ovl_control_table = sig.removeprefix("0") + (end if end else "")
    else:
        ovl_control_table = sig + (end if end else "")
    return ovl_dc_sys == ovl_control_table


def _update_ovl_control_tables(ovl_control_tables: dict[str, dict[str, Any]]):
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


def _check_ovl_destination_point(ovl: str, ovl_val: dict[str, Any], destination_point: str, table_name: str):
    dc_sys_destination_signal: str = get_dc_sys_value(ovl_val, DCSYS.IXL_Overlap.DestinationSignal)
    if dc_sys_destination_signal.endswith(destination_point.removeprefix("0")):
        return True
    print_error(f"For Overlap {Color.green}{ovl}{Color.reset}, DC_SYS Destination Signal {Color.yellow}"
                f"{dc_sys_destination_signal}{Color.reset} does not correspond to the Control Table {Color.green}"
                f"{table_name}{Color.reset} where Destination Point is {Color.yellow}{destination_point}{Color.reset}.")
    return False


def _check_ovl_sw(ovl: str, ovl_val: dict[str, Any], ovl_sw: str, ovl_path: str, table_name: str):
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
        dc_sys_ovl_sw_str = ', '.join(dc_sys_ovl_sw) if dc_sys_ovl_sw else "None"
        print_error(f"For Overlap {Color.green}{ovl}{Color.reset}, DC_SYS Overlap Switch does not have the same "
                    f"number of switches {Color.yellow}({len(dc_sys_ovl_sw)}){Color.reset} as in the Control Table "
                    f"{Color.green}{table_name}{Color.reset} {Color.yellow}({len(ovl_sw_list)}){Color.reset}.\n"
                    f"DC_SYS Overlap Switch: {Color.white}{dc_sys_ovl_sw_str}{Color.reset}\n"
                    f"Control Table Switch Overlap Path: {Color.beige}{ovl_sw}{Color.reset}"
                    f"\n{Color.default}Control Table Overlap IVB Path: {ovl_path}")
        result = False

    for dc_sys_sw, control_table_sw in zip(dc_sys_ovl_sw, ovl_sw_list):
        if not dc_sys_sw.endswith(control_table_sw):
            dc_sys_ovl_sw_str = f"{csi_bg_color(Color.yellow)}{Color.black}{dc_sys_sw}{Color.reset}{Color.white}".join(
                ', '.join(dc_sys_ovl_sw).split(dc_sys_sw))
            ovl_sw_str = f"{csi_bg_color(Color.yellow)}{Color.black}{control_table_sw}{Color.reset}{Color.white}".join(
                ovl_sw.split(control_table_sw))
            if any(sw.endswith(control_table_sw) for sw in dc_sys_ovl_sw):
                print_warning(f"For Overlap {Color.green}{ovl}{Color.reset}, the order of the switches does not "
                              f"correspond to the Control Table {Color.green}{table_name}{Color.reset}:\n"
                              f"{Color.blue}{dc_sys_sw = }{Color.reset} does not correspond to "
                              f"{Color.blue}{control_table_sw = }{Color.reset}.\n"
                              f"DC_SYS Overlap Switch: {Color.white}{dc_sys_ovl_sw_str}{Color.reset}\n"
                              f"Control Table Switch Overlap Path: {Color.beige}{ovl_sw_str}{Color.reset}"
                              f"\n{Color.default}Control Table Overlap IVB Path: {ovl_path}")
            else:
                print_error(f"For Overlap {Color.green}{ovl}{Color.reset}, switch {Color.blue}{dc_sys_sw = }"
                            f"{Color.reset} does not correspond to switch {Color.blue}{control_table_sw = }"
                            f"{Color.reset} in the Control Table {Color.green}{table_name}{Color.reset}.\n"
                            f"DC_SYS Overlap Switch: {Color.white}{dc_sys_ovl_sw_str}{Color.reset}\n"
                            f"Control Table Switch Overlap Path: {Color.beige}{ovl_sw_str}{Color.reset}"
                            f"\n{Color.default}Control Table Overlap IVB Path: {ovl_path}")
            result = False

    return result


def _check_ovl_path(ovl_name: str, ovl_val: dict[str, Any], ovl_path: str, table_name: str):
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
    ovl_path_list = ovl_path.split(",")
    ovl_path_list = [ivb.strip() for ivb in ovl_path_list]
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
                        f"the path is {Color.yellow}{ovl_path = }{Color.default} "
                        f"(last IVB: {Color.beige}{last_ivb} -> {corresponding_last_ivb}{Color.default})")
            result = False

    if corresponding_last_ivb is None:
        print_error(f"For Overlap {Color.green}{ovl_name}{Color.reset}, corresponding to Control Table "
                    f"{Color.green}{table_name}{Color.reset},\n"
                    f"last IVB of the path {Color.yellow}{ovl_path = }{Color.reset} is not found in the DC_SYS.\n"
                    f"Control Table Overlap last IVB: {Color.beige}{last_ivb} -> {corresponding_last_ivb}{Color.reset}"
                    f"\n{Color.default}DC_SYS Overlap last IVB: {Color.white}{ivb_on_vsp}{Color.reset} "
                    f"{Color.default}(on joint with {ivb_downstream_vsp})")
        result = False

    elif corresponding_last_ivb != ivb_on_vsp:
        print_error(f"For Overlap {Color.green}{ovl_name}{Color.reset}, corresponding to Control Table "
                    f"{Color.green}{table_name}{Color.reset},\n"
                    f"VSP {Color.blue}({vsp_seg}, {vsp_x}){Color.reset} does not correspond to the last IVB of "
                    f"the path {Color.yellow}{ovl_path = }{Color.reset} in the Control Table.\n"
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
    for ovl_dc_sys in ovl_dict.keys():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys):
            return None
    for ovl_dc_sys in ovl_dict.keys():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys, remove_zero=True):
            return None
    for ovl_dc_sys in ovl_dict.keys():
        if _correspondence_ovl_control_table_dc_sys(ovl_control_table, ovl_dc_sys,
                                                    test_with_ovl_pos=True, ovl_val=ovl_val):
            return f"{ovl_dc_sys} -> {ovl_control_table}"
    return False
