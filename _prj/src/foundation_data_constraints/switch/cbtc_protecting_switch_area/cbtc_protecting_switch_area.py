#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ....utils import *
from ....dc_sys import *
from ....fouling_points_utils import *
from .compute_verif import *
from .file_format_utils import *


__all__ = ["check_cbtc_protecting_switch_area"]


OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "CBTC Protecting Switch Area Verification.xlsx"
FILE_TITLE = "Verification of CBTC Protecting Switch Area"


def check_cbtc_protecting_switch_area() -> None:
    print_title(f"Verification of CBTC Protecting Switch Area", color=Color.mint_green)

    verif_dict = compute_verif()
    _create_verif_file(verif_dict)


def _create_verif_file(verif_dict: dict[str, dict[str, Any]]) -> None:
    # Initialize Verification Workbook
    wb = create_empty_verification_file()
    # Update Header sheet
    update_header_sheet_for_verif_file(wb, title=FILE_TITLE, c_d470=get_current_version(),
                                       fouling_point_file=get_fouling_point_file())
    # Create Verification sheet
    ws, row = create_empty_verif_sheet(wb)
    # Create Parameters sheet
    create_parameters_sheet(wb)

    # Update Verification sheet
    _update_verif_sheet(ws, row, verif_dict)

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Verification of CBTC Protecting Switch Area\" verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    open_excel_file(res_file_path)


def _update_verif_sheet(ws: xl_ws.Worksheet, start_row: int, verif_dict: dict[str, dict[str, Any]]) -> None:

    for row, (sw_name, sw_val) in enumerate(verif_dict.items(), start=start_row):
        sw_block_locking_area = sw_val.get("sw_block_locking_area")
        cbtc_protecting_switch_area = sw_val.get("cbtc_protecting_switch_area")
        fouling_point_distance = sw_val.get("fouling_point_distance")
        local_speed_km_per_h = sw_val.get("local_speed_km_per_h")
        list_ivb_to_protect = sw_val.get("list_ivb_to_protect")
        ivb_that_shall_be_added = sw_val.get("ivb_that_shall_be_added")
        ivb_that_can_be_removed = sw_val.get("ivb_that_can_be_removed")
        status = sw_val.get("status")
        comments = sw_val.get("comments")

        _add_line_info(ws, row, sw_name, sw_block_locking_area, cbtc_protecting_switch_area,
                       fouling_point_distance, local_speed_km_per_h,
                       list_ivb_to_protect, ivb_that_shall_be_added, ivb_that_can_be_removed)
        _add_status(ws, row, status)
        _add_comments(ws, row, comments)

    # Hide empty columns
    max_len_sw_block_locking_area = max(len(sw_val.get("sw_block_locking_area"))
                                        for sw_val in verif_dict.values())
    for sw_block_locking_area_col in range(SW_BLOCK_LOCKING_AREA_START_COL+max_len_sw_block_locking_area,
                                           SW_BLOCK_LOCKING_AREA_START_COL+CBTC_PROTECTING_SW_AREA_NB_COL):
        ws.column_dimensions[get_xl_column_letter(sw_block_locking_area_col)].hidden = True

    # Hide empty columns
    max_cbtc_protecting_switch_area = max(len(sw_val.get("cbtc_protecting_switch_area"))
                                          for sw_val in verif_dict.values())
    for cbtc_protecting_sw_area_col in range(CBTC_PROTECTING_SW_AREA_START_COL+max_cbtc_protecting_switch_area,
                                             CBTC_PROTECTING_SW_AREA_START_COL+CBTC_PROTECTING_SW_AREA_NB_COL):
        ws.column_dimensions[get_xl_column_letter(cbtc_protecting_sw_area_col)].hidden = True


def _add_line_info(ws: xl_ws.Worksheet, row: int, sw_name: str,
                   sw_block_locking_area, cbtc_protecting_switch_area,
                   fouling_point_distance, local_speed_km_per_h,
                   list_ivb_to_protect, ivb_that_shall_be_added, ivb_that_can_be_removed) -> None:
    # Switch Name
    create_cell(ws, sw_name, row=row, column=SWITCH_NAME_COL, borders=True)
    # Switch block locking area
    for ivb_id, sw_block_locking_area_col in enumerate(
            range(SW_BLOCK_LOCKING_AREA_START_COL,
                  SW_BLOCK_LOCKING_AREA_START_COL+SW_BLOCK_LOCKING_AREA_NB_COL)):
        ivb_name = sw_block_locking_area[ivb_id] if ivb_id < len(sw_block_locking_area) else None
        create_cell(ws, ivb_name, row=row, column=sw_block_locking_area_col, borders=True,
                    align_horizontal=XlAlign.center)
    # CBTC protecting switch area
    for ivb_id, cbtc_protecting_sw_area_col in enumerate(
            range(CBTC_PROTECTING_SW_AREA_START_COL,
                  CBTC_PROTECTING_SW_AREA_START_COL+CBTC_PROTECTING_SW_AREA_NB_COL)):
        ivb_name = cbtc_protecting_switch_area[ivb_id] if ivb_id < len(cbtc_protecting_switch_area) else None
        create_cell(ws, ivb_name, row=row, column=cbtc_protecting_sw_area_col, borders=True,
                    align_horizontal=XlAlign.center)
        if ivb_name in sw_block_locking_area:
            set_font_color(ws, font_color=XlFontColor.ko, row=row, column=cbtc_protecting_sw_area_col)
            set_bg_color(ws, bg_color=XlBgColor.ko, row=row, column=cbtc_protecting_sw_area_col)
    # Fouling Point Distance
    create_cell(ws, fouling_point_distance, row=row, column=FOULING_POINT_DISTANCE_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
    # Local Speed
    create_cell(ws, local_speed_km_per_h, row=row, column=LOCAL_SPEED_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Distance to protect
    distance_formula = (f"= (oc_zc_data_freshness_threshold + ixl_cycle_time) * "
                        f"({get_xl_column_letter(LOCAL_SPEED_COL)}{row} / 3.6)")
    create_cell(ws, distance_formula, row=row, column=DIST_TO_PROTECT_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)

    # List IVB to protect
    create_cell(ws, ", ".join(list_ivb_to_protect), row=row, column=COMPUTED_LIST_IVB_TO_PROTECT_COL, borders=True,
                line_wrap=True)
    # IVB that shall be added
    create_cell(ws, ", ".join(ivb_that_shall_be_added), row=row, column=IVB_THAT_SHALL_BE_ADDED_COL, borders=True,
                line_wrap=True)
    # IVB that can be removed
    create_cell(ws, ", ".join(ivb_that_can_be_removed), row=row, column=IVB_THAT_CAN_BE_REMOVED_COL, borders=True,
                line_wrap=True)


def _add_status(ws: xl_ws.Worksheet, row: int, status: Optional[str]) -> None:
    # Status
    create_cell(ws, status, row=row, column=STATUS_COL, borders=True,
                align_horizontal=XlAlign.center)


def _add_comments(ws: xl_ws.Worksheet, row: int, comments: Optional[str]) -> None:
    # Comments
    create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)
