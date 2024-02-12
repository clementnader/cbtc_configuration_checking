#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_par import *
# from ..control_tables import *


def cf_signal_12(no_overshoot: bool = False, apz_with_tc: bool = False, apz_from_excel_file: bool = False):
    # In nominal case the IXL approach zone locking for a dedicated signal is configured
    # to contain the first physical track circuit.
    csv = ("Signal Name;Type;Direction;IXL Approach Zone;IVB Limit Downstream;;;;IVB Limit Upstream;;;;"
           "IXL APZ Distance;Distance minus value to remove;DLT Distance;Automatic Status\n")
    csv += ";;;;Seg;x;Track;KP;Seg;x;Track;KP;;;;\n"
    print_title(f"Verification of CF_SIGNAL_12", color=Color.mint_green)
    at_deshunt_max_dist = get_param_value("at_deshunt_max_dist")
    block_laying_uncertainty = get_param_value("block_laying_uncertainty")
    mtc_rollback_dist = get_param_value("mtc_rollback_dist")
    at_rollback_dist = get_param_value("at_rollback_dist")
    overshoot_recovery_dist = get_param_value("overshoot_recovery_dist")
    overshoot_recovery_stopping_max_dist = get_param_value("overshoot_recovery_stopping_max_dist")
    if no_overshoot:
        value_to_remove = (at_deshunt_max_dist + block_laying_uncertainty +
                           max(mtc_rollback_dist, at_rollback_dist))
    else:
        value_to_remove = (at_deshunt_max_dist + block_laying_uncertainty +
                           max(mtc_rollback_dist, at_rollback_dist,
                               overshoot_recovery_dist + overshoot_recovery_stopping_max_dist))

    sig_dict = load_sheet(DCSYS.Sig)
    nb_sigs = len(sig_dict.keys())
    progress_bar(1, 1, end=True)  # reset progress_bar
    i: int
    for i, (sig_name, sig) in enumerate(sig_dict.items()):
        print_log(f"\r{progress_bar(i, nb_sigs)} processing verification of DLT distance of {sig_name}...", end="")
        sig_type = get_dc_sys_value(sig, DCSYS.Sig.Type)
        sig_direction = get_dc_sys_value(sig, DCSYS.Sig.Sens)
        csv += f"{sig_name};{sig_type};{sig_direction};"
        if sig_type in [SignalType.HEURTOIR, SignalType.PERMANENT_ARRET]:
            csv += f";;;;;;;;;;;;{'NA'}\n"
            continue

        dlt_distance = get_dc_sys_value(sig, DCSYS.Sig.DelayedLtDistance)
        if dlt_distance == 0:
            csv += f";;;;;;;;;;;{dlt_distance};{'OK'}\n"
            continue
        (ivb_lim_seg, ivb_lim_x), ivb_lim_str = get_ivb_limit_of_a_signal(sig_name, sig)
        ivb_lim_track, ivb_lim_kp = from_seg_offset_to_kp(ivb_lim_seg, ivb_lim_x)

        min_dist, corresponding_entrance, ivb_names = (
            _get_distance_between_block_and_approach_zone(sig_name, ivb_lim_seg, ivb_lim_x,
                                                          apz_with_tc, apz_from_excel_file))

        if min_dist is None:
            csv += f"{ivb_names};{ivb_lim_seg};{ivb_lim_x};{ivb_lim_track};{ivb_lim_kp};;;;;;;{dlt_distance};{'KO'}\n"
            continue
        corresponding_entrance_track, corresponding_entrance_kp = from_seg_offset_to_kp(*corresponding_entrance)
        test_value = round(min_dist - value_to_remove, 3)
        success = dlt_distance <= test_value

        csv += (f"{ivb_names};{ivb_lim_seg};{ivb_lim_x};{ivb_lim_track};{ivb_lim_kp};"
                f"{corresponding_entrance[0]};{corresponding_entrance[1]};"
                f"{corresponding_entrance_track};{corresponding_entrance_kp};"
                f"{min_dist};{test_value};{dlt_distance};{'OK' if success else 'KO'}\n")

        # if not success:
        #     print_error(f"For Signal {Color.blue}{sig_name}{Color.reset} on IVB {ivb_name}:\n"
        #                 f"The DLT distance {Color.white}{dlt_distance} m{Color.reset} is not "
        #                 f"inferior to {Color.white}{test_value} m{Color.reset}.")
        #     print(f"\tThe distance between the block limit {Color.yellow}{ivb_lim_str}{Color.reset} "
        #           f"{Color.light_grey}{(ivb_lim_seg, ivb_lim_x)}{Color.reset} and the closest entrance "
        #           f"{Color.light_grey}{corresponding_entrance}{Color.reset}\n\t"
        #           f"of all the signalling approach zones\n\t"
        #           f"is equal to {Color.beige}{min_dist} m{Color.reset}.")
        #     print(f"\tThe distance minus {Color.light_grey}{block_laying_uncertainty = }{Color.reset} "
        #           f"minus max({Color.light_grey}{mtc_rollback_dist = }{Color.reset}; "
        #           f"{Color.light_grey}{at_rollback_dist = }{Color.reset}; "
        #           f"{Color.light_grey}{overshoot_recovery_dist = }{Color.reset} + "
        #           f"{Color.light_grey}{overshoot_recovery_stopping_max_dist = }{Color.reset}),\n\t"
        #           f"i.e. minus {Color.beige}{value_to_remove} m{Color.reset} makes:\n\t"
        #           f"{Color.beige}{test_value} m{Color.reset}.")

    print_log(f"\r{progress_bar(nb_sigs, nb_sigs, end=True)} verification of DLT distance finished.\n")
    print(csv)
    return


def _get_distance_between_block_and_approach_zone(sig_name: str, ivb_lim_seg, ivb_lim_x,
                                                  apz_with_tc: bool = False, apz_from_excel_file: bool = False):
    list_ivb = _get_approach_area_ivb(sig_name, apz_with_tc, apz_from_excel_file)
    if not list_ivb:
        print(f"\nThe signal {sig_name} has no IXL approach area: {list_ivb}")
        return None, None, None
    ivb_names = ", ".join(list_ivb)
    list_entrance_points = _get_entrance_points_of_approach_zone(sig_name, list_ivb, apz_with_tc)
    min_dist = None
    corresponding_entrance = None

    sig_dict = load_sheet(DCSYS.Sig)
    sig_direction = get_dc_sys_value(sig_dict[sig_name], DCSYS.Sig.Sens)
    for entrance_seg, entrance_x in list_entrance_points:
        if are_points_matching(entrance_seg, entrance_x, ivb_lim_seg, ivb_lim_x):
            continue
        dist = get_dist_downstream(entrance_seg, entrance_x, ivb_lim_seg, ivb_lim_x,
                                   downstream=sig_direction == Direction.CROISSANT)
        if dist is None:
            continue
        if min_dist is None or dist < min_dist:
            min_dist = dist
            corresponding_entrance = (entrance_seg, entrance_x)
    return min_dist, corresponding_entrance, ivb_names


def _get_entrance_points_of_approach_zone(sig_name: str, list_ivb: list[str], apz_with_tc: bool
                                          ) -> list[tuple[str, float]]:
    ivb_dict = load_sheet(DCSYS.IVB)
    tc_dict = load_sheet(DCSYS.CDV)
    list_points = list()
    for ivb_name in list_ivb:
        if (not apz_with_tc and ivb_name not in ivb_dict) or (apz_with_tc and ivb_name not in tc_dict):
            obj_type = "IVB" if not apz_with_tc else "CDV"
            print_error(f"For Signal {sig_name}, IXL APZ is defined containing {obj_type} {ivb_name}. "
                        f"But this {obj_type} does not exist in the DC_SYS.")
            continue
        if not apz_with_tc:
            list_points.extend(list(get_dc_sys_zip_values(ivb_dict[ivb_name],
                                                          DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X)))
        else:
            list_points.extend(list(get_dc_sys_zip_values(tc_dict[ivb_name],
                                                          DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)))

    list_points_without_double = list()
    i: int
    for i, (entrance_seg, entrance_x) in enumerate(list_points):
        list_points_reduced = list_points[:i] + list_points[i+1:]
        if any(are_points_matching(entrance_seg, entrance_x, seg, x) for seg, x in list_points_reduced):
            continue
        list_points_without_double.append((entrance_seg, entrance_x))

    return list_points_without_double


# IXL_APZ_FILE = (r"C:\Users\naderc\Desktop\KCR"
#                 r"\CR-ASTS-GEN=Gen-PS=ATC=GEN-IFM-ICD-042155_14.00#ATT004XLSX - ATC - C12_D404  IXL APZ Rev01.xlsx")
IXL_APZ_FILE = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_IXL_APZ.xlsx"
# IXL_APZ_SHEET_NAME = r"IXL APZ"
IXL_APZ_SHEET_NAME = r"IXL_APZ"
START_LINE = 2
# SIG_COLUMN = 'A'
SIG_COLUMN = 'B'
# APZ_START_COLUMN = 2
APZ_START_COLUMN = 6
# APZ_NB_COLUMNS = 5
APZ_NB_COLUMNS = 3

LOADED_DB = dict()


def _get_approach_area_ivb_from_excel_file(sig_name: str) -> Optional[list[str]]:
    if not LOADED_DB:
        wb = load_xlsx_wb(IXL_APZ_FILE)
        ws = get_xl_sheet_by_name(wb, IXL_APZ_SHEET_NAME)
        for row in range(START_LINE, get_xl_number_of_rows(ws) + 1):
            sig = get_xl_cell_value(ws, row=row, column=SIG_COLUMN)
            if sig is None:
                continue
            apz_ivb_list = list()
            for column in range(APZ_START_COLUMN, APZ_START_COLUMN+APZ_NB_COLUMNS):
                ivb = get_xl_cell_value(ws, row=row, column=column)
                if ivb is not None:
                    apz_ivb_list.append(ivb)
            LOADED_DB[sig] = apz_ivb_list
    return LOADED_DB.get(sig_name)


def _get_approach_area_ivb(sig_name: str, apz_with_tc: bool = False, apz_from_excel_file: bool = False) -> list[str]:
    if apz_from_excel_file:
        apz_ivb_list = _get_approach_area_ivb_from_excel_file(sig_name)
        if apz_ivb_list is not None:
            return apz_ivb_list
    sig_dict = load_sheet(DCSYS.Sig)
    current_ivb = get_dc_sys_value(sig_dict[sig_name], DCSYS.Sig.IvbJoint.UpstreamIvb)
    if not apz_with_tc:
        return [current_ivb]  # default IXL Approach Zone = first IVB
    # IXL Approach Zone = first Track Circuit
    return [get_related_block_of_ivb(current_ivb)]


# def _get_approach_area_ivb(sig_name: str):
#     list_approach_ivb = list()
#     route_control_tables = parse_control_tables(CONTROL_TABLE_TYPE.route, use_csv_file=True)
#     for route_name, route_val in route_control_tables.items():
#         control_sig = [val.upper().strip() for key, val in route_val.items()
#                        if any(key.startswith(key_id) for key_id in ROUTE_CONTROL_SIG_CONTROL_TABLE)][0]
#         if _control_table_sig_correspond(sig_name, control_sig):
#             approach_ivb = [val.upper().strip() for key, val in route_val.items()
#                             if key.startswith(ROUTE_APPROACH_AREA_CLEARANCE_CONTROL_TABLE)][0]
#             if approach_ivb == "--":
#                 approach_ivb_list = []
#             else:
#                 approach_ivb_list = approach_ivb.split(",")
#                 approach_ivb_list = [ivb.strip() for ivb in approach_ivb_list]
#             if not list_approach_ivb or len(approach_ivb_list) < len(list_approach_ivb):
#                 list_approach_ivb = approach_ivb_list
#     return [_get_corresponding_dc_sys_ivb(ivb) for ivb in list_approach_ivb]
#
#
# def _control_table_sig_correspond(sig_name: str, control_table_sig_name: str) -> bool:
#     sig_nb = sig_name.split("_")[-1]
#     return sig_nb == control_table_sig_name
#
#
# def _get_corresponding_dc_sys_ivb(control_table_ivb_name: str):
#     ivb_dict = load_sheet(DCSYS.IVB)
#     for ivb_name in ivb_dict.keys():
#         if ivb_name.upper().endswith(control_table_ivb_name):
#             return ivb_name
#     return None
