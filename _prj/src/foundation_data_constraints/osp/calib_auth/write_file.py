#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ....utils import *
from ....dc_sys import *
from ....dc_sys_get_cbtc_territory.cbtc_territory_utils import print_in_cbtc
from .file_format_utils import *


__all__ = ["create_verif_file"]


OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "XXX Verification.xlsx"
FILE_TITLE = "Verification of XXX"


def create_verif_file(verif_dict: dict[str, dict[str, Any]], constraint_name: str, in_cbtc: bool) -> str:
    # Adapt to the corresponding constraint
    verif_file_title = VERIF_FILE_NAME.replace("XXX", constraint_name)
    file_title = FILE_TITLE.replace("XXX", constraint_name)

    # Initialize Verification Workbook
    wb = create_empty_verification_file()
    # Update Header sheet
    update_header_sheet_for_verif_file(wb, title=file_title, c_d470=get_current_version())
    # Create Verification sheet
    ws, row = create_empty_verif_sheet(wb)

    # Update Verification sheet
    _update_verif_sheet(ws, row, verif_dict)

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(verif_file_title))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Verification of {constraint_name}\" verification file, {print_in_cbtc(in_cbtc)}, "
                  f"is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _update_verif_sheet(ws: xl_ws.Worksheet, row: int, verif_dict: dict[str, dict[str, Any]]) -> None:
    for osp_name, osp_value in verif_dict.items():
        osp_start_row = row
        calib_auth = osp_value.pop("Allow Accelerometers Calibration")
        osp_position_and_type = osp_value.pop("osp_position_and_type")
        (_, _, osp_direction, osp_track, osp_kp), osp_type = osp_position_and_type
        for train_type, train_type_value in osp_value.items():
            train_type_start_row = row
            train_front_position_at_osp = train_type_value.pop("train_front_position_at_osp")
            _, _, train_front_track, train_front_kp = train_front_position_at_osp
            for accel_car_str, accel_car_value in train_type_value.items():
                accel_car_start_row = row
                accel_car = accel_car_str.removeprefix("accelerometer_car = ")
                for train_polarity_str, train_polarity_value in accel_car_value.items():
                    train_polarity = train_polarity_str.removeprefix("train_polarity = ")
                    accel_car_pos_with_tol = train_polarity_value.get("accelerometer_car_position_with_tolerance_at_osp")
                    ((_, _, _, accel_car_start_track, accel_car_start_kp),
                     (_, _, _, accel_car_end_track, accel_car_end_kp)) = accel_car_pos_with_tol

                    slope_change_under_car = train_polarity_value.get("slope_change_under_car")
                    min_slope = train_polarity_value.get("min_slope")
                    max_slope = train_polarity_value.get("max_slope")

                    _add_train_polarity_info(ws, row, train_polarity, accel_car_start_track, accel_car_start_kp,
                                             accel_car_end_track, accel_car_end_kp,
                                             slope_change_under_car, min_slope, max_slope)
                    row += 1

                _add_accel_car_info(ws, accel_car_start_row, row-1, accel_car)

            _add_train_type_info(ws, train_type_start_row, row-1, train_type, train_front_track, train_front_kp)

        _add_osp_info(ws, osp_start_row, row-1, osp_name, osp_track, osp_kp, osp_direction, osp_type, calib_auth)
        _add_status(ws, osp_start_row, row-1)
        _add_comments(ws, osp_start_row, row-1, calib_auth)
        draw_exterior_borders_of_a_range(ws, start_row=osp_start_row, end_row=row-1,
                                         start_column=OSP_NAME_COL, end_column=COMMENTS_COL)


def _add_osp_info(ws: xl_ws.Worksheet, start_row: int, end_row: int,
                  osp_name: str, osp_track: str, osp_kp: float, osp_direction: str, osp_type: str,
                  calib_auth: bool) -> None:
    # OSP name
    create_merged_cell(ws, osp_name, start_row=start_row, end_row=end_row,
                       start_column=OSP_NAME_COL, end_column=OSP_NAME_COL)
    # OSP position
    create_merged_cell(ws, osp_track, start_row=start_row, end_row=end_row,
                       start_column=OSP_TRACK_COL, end_column=OSP_TRACK_COL, line_wrap=False)
    create_merged_cell(ws, osp_kp, start_row=start_row, end_row=end_row,
                       start_column=OSP_KP_COL, end_column=OSP_KP_COL, nb_of_digits=2, line_wrap=False)
    create_merged_cell(ws, osp_direction, start_row=start_row, end_row=end_row,
                       start_column=OSP_DIRECTION_COL, end_column=OSP_DIRECTION_COL,
                       align_horizontal=XlAlign.center, line_wrap=False)
    create_merged_cell(ws, osp_type, start_row=start_row, end_row=end_row,
                       start_column=OSP_TYPE_COL, end_column=OSP_TYPE_COL,
                       align_horizontal=XlAlign.center, line_wrap=False)
    # Allow Accelerometers Calibration
    create_merged_cell(ws, calib_auth, start_row=start_row, end_row=end_row,
                       start_column=OSP_CALIB_AUTH_COL, end_column=OSP_CALIB_AUTH_COL, line_wrap=False)


def _add_train_type_info(ws: xl_ws.Worksheet, start_row: int, end_row: int,
                         train_type: str, train_front_track: str, train_front_kp: float) -> None:
    # Train Type
    create_merged_cell(ws, train_type, start_row=start_row, end_row=end_row,
                       start_column=TRAIN_TYPE_COL, end_column=TRAIN_TYPE_COL,
                       align_horizontal=XlAlign.center)
    # Train Front Position
    create_merged_cell(ws, train_front_track, start_row=start_row, end_row=end_row,
                       start_column=TRAIN_FRONT_TRACK_COL, end_column=TRAIN_FRONT_TRACK_COL, line_wrap=False)
    create_merged_cell(ws, train_front_kp, start_row=start_row, end_row=end_row,
                       start_column=TRAIN_FRONT_KP_COL, end_column=TRAIN_FRONT_KP_COL, nb_of_digits=2, line_wrap=False)


def _add_accel_car_info(ws: xl_ws.Worksheet, start_row: int, end_row: int,
                        accel_car: int) -> None:
    # Car with Accelerometer
    create_merged_cell(ws, accel_car, start_row=start_row, end_row=end_row,
                       start_column=ACCEL_CAR_NB_COL, end_column=ACCEL_CAR_NB_COL,
                       align_horizontal=XlAlign.center, line_wrap=False)


def _add_train_polarity_info(ws: xl_ws.Worksheet, row: int,
                             train_polarity: str, accel_car_start_track: str, accel_car_start_kp: float,
                             accel_car_end_track: str, accel_car_end_kp: float,
                             slope_change_under_car: bool, min_slope: float, max_slope: float) -> None:
    # Train Polarity
    create_cell(ws, train_polarity, row=row, column=TRAIN_POLARITY_COL, align_horizontal=XlAlign.center)
    # Car Position
    create_cell(ws, accel_car_start_track, row=row, column=ACCEL_CAR_WITH_TOL_START_TRACK_COL)
    create_cell(ws, accel_car_start_kp, row=row, column=ACCEL_CAR_WITH_TOL_START_KP_COL, nb_of_digits=2)
    create_cell(ws, accel_car_end_track, row=row, column=ACCEL_CAR_WITH_TOL_END_TRACK_COL)
    create_cell(ws, accel_car_end_kp, row=row, column=ACCEL_CAR_WITH_TOL_END_KP_COL, nb_of_digits=2)
    # Slope under Car
    create_cell(ws, slope_change_under_car, row=row, column=SLOPE_CHANGE_UNDER_CAR_COL)
    create_cell(ws, min_slope, row=row, column=MIN_SLOPE_COL, percentage_nb_of_digits=4)
    create_cell(ws, max_slope, row=row, column=MAX_SLOPE_COL, percentage_nb_of_digits=4)
    # Constant Slope under Car
    constant_slope_formula = f'= {MIN_SLOPE_COL}{row} = {MAX_SLOPE_COL}{row}'
    create_cell(ws, constant_slope_formula, row=row, column=CONSTANT_SLOPE_COL)


def _add_status(ws: xl_ws.Worksheet, start_row: int, end_row: int) -> None:
    # Status
    test_slope_is_constant = ", ".join([f'{CONSTANT_SLOPE_COL}{row} = {True}' for row in range(start_row, end_row+1)])
    status_formula = (f'= IF({OSP_CALIB_AUTH_COL}{start_row} = {False}, "NA",\n'
                      f'    IF(AND({test_slope_is_constant}), "OK", "KO"))')
    create_merged_cell(ws, status_formula, start_row=start_row, end_row=end_row,
                       start_column=STATUS_COL, end_column=STATUS_COL, align_horizontal=XlAlign.center, line_wrap=False)


def _add_comments(ws: xl_ws.Worksheet, start_row: int, end_row: int, calib_auth: bool) -> None:
    if not calib_auth:
        comments = "Accelerometers Calibration is not authorized at OSP."
    else:
        comments = None
    # Comments
    create_merged_cell(ws, comments, start_row=start_row, end_row=end_row,
                       start_column=COMMENTS_COL, end_column=COMMENTS_COL)
