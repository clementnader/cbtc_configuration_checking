#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_sys_draw_path.dc_sys_path_and_distances import *
from ....dc_sys_draw_path.dc_sys_get_zones import get_zones_intersecting_zone, depolarization_in_zone
from ....dc_sys_sheet_utils import *
from ....dc_par import *
from .file_format_utils import *


__all__ = ["compute_ze_impacte_fu", "create_computed_result_file_ze_impacte_fu"]


def compute_ze_impacte_fu() -> dict[str, dict[str, Union[bool, dict[str, Union[bool, tuple[str, ...]]]]]]:
    eb_max_dist = get_param_value("eb_max_dist")
    list_zc = get_all_zc()
    results = {zc_name: dict() for zc_name in list_zc}
    vb_dict = load_sheet(DCSYS.CV)
    maz_dict = load_sheet(DCSYS.Zaum)
    vb_per_zc = {zc_name: sorted([vb_name for vb_name in vb_dict if zc_name in get_zc_of_obj(DCSYS.CV, vb_name)])
                 for zc_name in list_zc}
    maz_per_zc = {zc_name: sorted([maz_name for maz_name in maz_dict if zc_name in get_zc_of_obj(DCSYS.Zaum, maz_name)])
                  for zc_name in list_zc}

    for zc_name in list_zc:
        depol_in_zc = bool(depolarization_in_zone(DCSYS.PAS, zc_name))
        results[zc_name]["depol_in_zc"] = depol_in_zc
        progress_bar(1, 1, end=True)  # reset progress_bar
        nb_vb = len(vb_per_zc[zc_name])
        for i, vb_name in enumerate(vb_per_zc[zc_name]):
            print_log_progress_bar(i, nb_vb, f"processing ZE_IMPACTE_FU for {vb_name} in {zc_name}")
            cv_ze_impacte_fu = list()
            maz_in_vb = get_zones_intersecting_zone(DCSYS.Zaum, DCSYS.CV, vb_name)

            for maz_index, maz_name in enumerate(maz_per_zc[zc_name], start=1):

                if maz_name in maz_in_vb:
                    cv_ze_impacte_fu.append(("ZE_"+maz_name, str(maz_index), "CROISSANT"))
                    cv_ze_impacte_fu.append(("ZE_"+maz_name, str(maz_index), "DECROISSANT"))
                    continue

                # for MAZ outside of VB we compute the distance in both directions and compare it to eb_max_dist
                downstream_dist = get_dist_between_objects(DCSYS.CV, vb_name, DCSYS.Zaum, maz_name, downstream=True,
                                                           avoid_zero=True)
                if downstream_dist is not None and 0 < downstream_dist <= eb_max_dist:
                    cv_ze_impacte_fu.append(("ZE_"+maz_name, str(maz_index), "CROISSANT"))

                upstream_dist = get_dist_between_objects(DCSYS.CV, vb_name, DCSYS.Zaum, maz_name, downstream=False,
                                                         avoid_zero=True)
                if upstream_dist is not None and 0 < upstream_dist <= eb_max_dist:
                    cv_ze_impacte_fu.append(("ZE_"+maz_name, str(maz_index), "DECROISSANT"))

            tuple_ze_name, tuple_ze_index, tuple_directions = list(zip(*cv_ze_impacte_fu))
            results[zc_name][vb_name] = {
                "tuple_ze_name": tuple_ze_name,
                "tuple_ze_index": tuple_ze_index,
                "tuple_directions": tuple_directions,
            }
            if depol_in_zc:
                depol_in_vb = bool(depolarization_in_zone(DCSYS.CV, vb_name))
                results[zc_name][vb_name]["depol_in_vb"] = depol_in_vb
                results[zc_name][vb_name]["reversed_directions"] = _reverse_ze_impacte_fu_directions(tuple_ze_index,
                                                                                                     tuple_directions)

        print_log_progress_bar(nb_vb, nb_vb, f"ZE_IMPACTE_FU computed on {zc_name}", end=True)

    return results


OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "ZC_APPLI_IF_VERIF - ZE_IMPACTE_FU.xlsx"
FILE_TITLE = "Verification of ZC Appli IF \"ZE_IMPACTE_FU\""


def create_computed_result_file_ze_impacte_fu() -> None:
    results = compute_ze_impacte_fu()
    res_file_path = _create_verif_file(results)
    open_excel_file(res_file_path)


def _create_verif_file(results: dict[str, dict[str, Union[bool, dict[str, Union[bool, tuple[str, ...]]]]]]) -> str:
    # Initialize Verification Workbook
    wb = create_empty_verification_file()
    # Update Header sheet
    update_header_sheet_for_verif_file(wb, title=FILE_TITLE, c_d470=get_current_version())
    # Create Verification sheet for each ZC
    first_sheet = True
    for zc_name, sub_dict in results.items():
        # Get Boolean for depolarization point in ZC
        depol_in_zc = sub_dict.pop("depol_in_zc")
        # Create empty Verification sheet
        ws, row = create_empty_verif_sheet(wb, zc_name, first_sheet, depol_in_zc)
        first_sheet = False
        # Update Verification sheet
        _update_verif_sheet(ws, row, sub_dict, depol_in_zc)

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Verification of CBTC Approach Zone\" verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _update_verif_sheet(ws: xl_ws.Worksheet, start_row: int,
                        verif_dict: dict[str, dict[str, Union[bool, tuple[str, ...]]]], depol_in_zc: bool) -> None:
    first_row = True
    for row, (vb_name, info) in enumerate(verif_dict.items(), start=start_row):
        tuple_ze_name = info["tuple_ze_name"]
        tuple_ze_index = info["tuple_ze_index"]
        tuple_directions = info["tuple_directions"]
        _add_line_info(ws, row, vb_name, tuple_ze_name, tuple_ze_index, tuple_directions)
        if depol_in_zc:
            reversed_directions = info["reversed_directions"]
            depol_in_vb = info["depol_in_vb"]
            _add_line_depol_info(ws, row, reversed_directions, depol_in_vb, first_row)
            if not depol_in_vb:
                first_row = False


def _add_line_info(ws: xl_ws.Worksheet, row: int, vb_name: str, tuple_ze_name: tuple[str, ...],
                   tuple_ze_index: tuple[str, ...], tuple_directions: tuple[str, ...]) -> None:
    # VB name
    create_cell(ws, vb_name, row=row, column=VB_NAME_COL)
    # List of ZE impacted by EB
    tuple_ze_name_str = ";".join(tuple_ze_name)
    create_cell(ws, tuple_ze_name_str, row=row, column=ZE_IMPACTED_BY_EB_COL)
    # List of the corresponding ZE ID
    tuple_ze_index_str = ";".join(tuple_ze_index)
    create_cell(ws, tuple_ze_index_str, row=row, column=ZE_ID_COL)
    # List of the corresponding directions
    tuple_directions_str = ";".join(tuple_directions)
    create_cell(ws, tuple_directions_str, row=row, column=DIRECTION_COL)
    # Cell with space to not have the list of directions spreading to other columns
    create_cell(ws, " ", row=row, column=AUTOMATIC_COMMENTS_COL)


def _add_line_depol_info(ws: xl_ws.Worksheet, row: int, reversed_directions: tuple[str, ...],
                         depol_in_vb: bool, first_row: bool) -> None:
    if depol_in_vb:
        comments = f"Virtual Block containing a depolarization point, to be analyzed manually."
        reversed_directions_str = None  # Reversed directions are not useful in that case
        comments_bg_color = XlBgColor.ko
        comments_font_color = XlFontColor.ko
    else:
        if first_row:
            comments = (f"ZC contains a depolarization point, the tool gives the results in the segments direction, "
                        f"verifications need to be done with the reversed directions for the Virtual Blocks where the "
                        f"ZC direction is opposed to segment direction.")
        else:
            comments = None
        comments_bg_color = XlBgColor.warning
        comments_font_color = XlFontColor.warning
        reversed_directions_str = ";".join(reversed_directions)
    # Automatic Comments
    create_cell(ws, comments, row=row, column=AUTOMATIC_COMMENTS_COL, line_wrap=True, bg_color=comments_bg_color,
                font_color=comments_font_color)
    # List of the reversed directions
    create_cell(ws, reversed_directions_str, row=row, column=REVERSE_DIRECTION_COL)
    # Cell with space to not have the list of directions spreading to other columns
    create_cell(ws, " ", row=row, column=BLANK_COL)


def _reverse_ze_impacte_fu_directions(tuple_ze_index: tuple[str, ...], tuple_directions: tuple[str, ...]
                                      ) -> tuple[str, ...]:
    list_reverse_directions = list()
    for ze_direction in tuple_directions:
        reverse_direction = "DECROISSANT" if ze_direction == "CROISSANT" else "CROISSANT"
        list_reverse_directions.append(reverse_direction)
    sorted_list_reverse_directions = [ze_direction for (_, ze_direction)
                                      in sorted(zip(tuple_ze_index, list_reverse_directions))]
    return tuple(sorted_list_reverse_directions)
