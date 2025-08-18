#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...dc_sys import *
from ..survey_types import *
from ..survey_utils import *
from .file_format_utils import *


__all__ = ["create_survey_verif_file"]


SURVEY_VERIF_TEMPLATE = os.path.join(TEMPLATE_DIRECTORY, "template_survey_verification.xlsx")

OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "Correspondence with Site Survey.xlsx"

TOOL_NAME = "Survey_Checking"
FILE_TITLE = "Correspondence with Site Survey"


def create_survey_verif_file(survey_verif_dict: dict[str, dict[str, dict]], block_def_exists_bool: bool,
                             tool_version: str, survey_display_info_list: list[str],
                             block_definition_display_info: str):
    # Load the Excel template for the verification file
    wb = load_xlsx_wb(SURVEY_VERIF_TEMPLATE, template=True)
    # Create Header sheet
    create_empty_header_sheet(wb)
    # Update Header sheet
    update_header_sheet_for_verif_file(wb, title=FILE_TITLE, c_d470=get_current_version(),
                                       tool_name=TOOL_NAME, tool_version=tool_version,
                                       survey_display_info_list=survey_display_info_list,
                                       block_definition_display_info=block_definition_display_info)
    # Update Menu sheet
    _update_menu_sheet(wb)

    # Create Verification sheets
    for sheet_name, verif_dict in survey_verif_dict.items():
        extra_column = (sheet_name == SURVEY_TYPES_DICT["BLOCK"]["res_sheet"]) and block_def_exists_bool
        ws, start_row = create_verif_sheet(wb, sheet_name, extra_column)
        _update_verif_sheet(sheet_name, ws, verif_dict, extra_column, start_row)

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Correspondence with Site Survey\" verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _update_menu_sheet(wb: openpyxl.workbook.Workbook):
    if get_ga_version() >= (7, 2, 0, 0):
        return
    ws = wb["FD - Site Survey"]
    ws.delete_rows(17)  # for older GA versions, delete PSD line that was not verified here
    ws.row_dimensions[17].height = 15  # restore default height


def _update_verif_sheet(sheet_name: str, ws: xl_ws.Worksheet,
                        verif_dict: dict[str, dict], extra_column: bool, start_row: int) -> None:
    tolerance_dict = get_tolerance_dict(sheet_name)
    multiple_dc_sys_objets = _get_multiple_dc_sys_objets(sheet_name)
    multiple_survey_objets = _get_multiple_survey_objets(sheet_name)
    sheet_comments = False
    for row, (obj_full_name, obj_val) in enumerate(verif_dict.items(), start=start_row):
        obj_name = obj_full_name[0]
        dc_sys_sheet = obj_val["dc_sys_sheet"]
        dc_sys_track = obj_val["dc_sys_original_track"]  # display the original track name
        block_def_limit_name = obj_val.get("block_def_limit_name")
        dc_sys_kp = obj_val["dc_sys_kp"]
        survey_name = obj_val["survey_name"]
        survey_type = obj_val["survey_type"]
        survey_track = obj_val["survey_original_track"]  # display the original track name
        surveyed_kp = obj_val["surveyed_kp"]
        surveyed_kp_comment = obj_val["surveyed_kp_comment"]
        comments = obj_val["comments"]

        obj_name = None if dc_sys_sheet is None else obj_name

        tolerance = _get_tolerance(tolerance_dict, dc_sys_sheet, survey_type)
        dc_sys_color = _get_dc_sys_color(multiple_dc_sys_objets, dc_sys_sheet)
        survey_color = _get_survey_color(multiple_survey_objets, survey_type)

        reverse_polarity = check_polarity(dc_sys_kp, surveyed_kp)

        _add_line_info(ws, row, obj_name, dc_sys_sheet, dc_sys_track, dc_sys_kp,
                       survey_name, survey_type, survey_track, surveyed_kp, dc_sys_color, survey_color,
                       extra_column)
        if extra_column:
            _add_block_def_info(ws, row, block_def_limit_name)
        _add_line_cell_comments(ws, row, surveyed_kp_comment, extra_column)
        _add_line_calculations(ws, row, tolerance, extra_column)
        sheet_comments = _add_line_comments_column(ws, row, comments, tolerance, reverse_polarity, extra_column,
                                                   sheet_comments)
    if not sheet_comments:  # no automatic comments, the column can be hidden
        ws.column_dimensions[get_column(AUTOMATIC_COMMENTS_COL, extra_column)].hidden = True


def _add_line_info(ws: xl_ws.Worksheet, row: int,
                   obj_name: str, dc_sys_sheet: str, dc_sys_track: str, dc_sys_kp: float,
                   survey_name: str, survey_type: str, survey_track: float, surveyed_kp: float,
                   dc_sys_color: str, survey_color: str, extra_column: bool) -> None:
    bg_color_dc_sys = dc_sys_color if obj_name is not None else None
    bg_color_survey = survey_color if survey_name is not None else None
    # Name
    create_cell(ws, obj_name, row=row, column=NAME_COL, borders=True,
                bg_color=bg_color_dc_sys)
    # DC_SYS Sheet
    create_cell(ws, dc_sys_sheet, row=row, column=DC_SYS_SHEET_COL, borders=True,
                bg_color=bg_color_dc_sys)
    # DC_SYS Track
    create_cell(ws, dc_sys_track, row=row, column=DC_SYS_TRACK_COL, borders=True,
                bg_color=bg_color_dc_sys)
    # DC_SYS KP
    create_cell(ws, dc_sys_kp, row=row, column=DC_SYS_KP_COL, borders=True,
                nb_of_digits=2, bg_color=bg_color_dc_sys)
    # Survey Name
    create_cell(ws, survey_name, row=row, column=get_column(SURVEY_NAME_COL, extra_column), borders=True,
                bg_color=bg_color_survey)
    # Survey Type
    create_cell(ws, survey_type, row=row, column=get_column(SURVEY_TYPE_COL, extra_column), borders=True,
                bg_color=bg_color_survey)
    # Survey Track
    create_cell(ws, survey_track, row=row, column=get_column(SURVEY_TRACK_COL, extra_column), borders=True,
                bg_color=bg_color_survey)
    # Surveyed KP
    create_cell(ws, surveyed_kp, row=row, column=get_column(SURVEYED_KP_COL, extra_column), borders=True,
                nb_of_digits=3, bg_color=bg_color_survey)


def _add_block_def_info(ws: xl_ws.Worksheet, row: int,
                        block_def_limit_name: str) -> None:
    # Block Def. Limit Name
    create_cell(ws, block_def_limit_name, row=row, column=BLOCK_DEF_LIMIT_NAME_COL, borders=True,
                bg_color=XlBgColor.light_grey if block_def_limit_name is not None else None)


def _add_line_cell_comments(ws: xl_ws.Worksheet, row: int,
                            surveyed_kp_comment: str, extra_column: bool) -> None:
    # Comments on Surveyed KP cell to tell from which survey info comes
    if surveyed_kp_comment is not None:
        add_cell_comment(ws, surveyed_kp_comment, row=row, column=get_column(SURVEYED_KP_COL, extra_column))


def _add_line_calculations(ws: xl_ws.Worksheet, row: int,
                           tolerance: str, extra_column: bool) -> None:
    # Difference
    difference_formula = (f'= IF({DC_SYS_KP_COL}{row} = "", "Not in DC_SYS", '
                          f'IF({get_column(SURVEYED_KP_COL, extra_column)}{row} = "", "Not Surveyed", '
                          f'{DC_SYS_KP_COL}{row} - {get_column(SURVEYED_KP_COL, extra_column)}{row}))')
    create_cell(ws, difference_formula, row=row, column=get_column(DIFFERENCE_COL, extra_column), borders=True,
                nb_of_digits=4)
    # Status
    status_formula = (f'= IF({get_column(DIFFERENCE_COL, extra_column)}{row} = "Not in DC_SYS", "Not in DC_SYS", '
                      f'IF({get_column(DIFFERENCE_COL, extra_column)}{row} = "Not Surveyed", "Not Surveyed", '
                      f'IF(ABS({get_column(DIFFERENCE_COL, extra_column)}{row}) <= {tolerance}, "OK", "KO")))')
    create_cell(ws, status_formula, row=row, column=get_column(STATUS_COL, extra_column),
                borders=True, align_horizontal=XlAlign.center)


def _add_line_comments_column(ws: xl_ws.Worksheet, row: int,
                              comments: str, tolerance: str, reverse_polarity: bool, extra_column: bool,
                              sheet_comments: bool) -> bool:
    if comments is not None:
        comments = comments.replace("2 times", "twice")

    if reverse_polarity:
        if comments is None:
            full_comments = '= '
        else:
            full_comments = f'= "{comments}\n\n" & '
        full_comments += (f'"Opposite sign in survey.\n'
                          f'Difference with absolute signs makes " & '
                          f'ROUND(ABS({DC_SYS_KP_COL}{row}) - '
                          f'ABS({get_column(SURVEYED_KP_COL, extra_column)}{row}), 4) & ", which is "'
                          f' & IF(ABS(ABS({DC_SYS_KP_COL}{row}) - '
                          f'ABS({get_column(SURVEYED_KP_COL, extra_column)}{row})) <= {tolerance},'
                          f' "lower", "larger") & " than the tolerance " & {tolerance}'
                          f' & IF(ABS(ABS({DC_SYS_KP_COL}{row}) - '
                          f'ABS({get_column(SURVEYED_KP_COL, extra_column)}{row})) <= {tolerance},'
                          f' " -> OK", " -> KO") & "."')
    else:
        full_comments = comments
    if full_comments is not None:
        sheet_comments = True

    # Comments
    create_cell(ws, full_comments, row=row, column=get_column(AUTOMATIC_COMMENTS_COL, extra_column),
                borders=True, line_wrap=True, align_vertical=XlAlign.top)
    if reverse_polarity:
        # line feeds inside a formula are not directly taken into account by the line wrap to autofit the row height
        # extra_row = 1 if comments else 0
        polarity_comments_length = len(
            "Difference with absolute signs makes -00.0000, which is larger than the tolerance 0.006 -> KO.")
        adjust_fixed_row_height(ws, row=row, column=get_column(AUTOMATIC_COMMENTS_COL, extra_column),
                                line_length=polarity_comments_length + (len(comments) if comments is not None else 0))
    # Manual Verification
    create_cell(ws, None, row=row, column=get_column(MANUAL_VERIFICATION_COL, extra_column),
                borders=True, align_horizontal=XlAlign.center)
    # Manual Comments
    create_cell(ws, None, row=row, column=get_column(COMMENTS_COL, extra_column),
                borders=True, line_wrap=True, align_vertical=XlAlign.top)
    return sheet_comments


def _get_tolerance(tolerance_dict: Optional[Union[tuple[str, str, float], dict[str, tuple[str, str, float]]]],
                   dc_sys_sheet: Optional[str], survey_type: Optional[str]) -> Optional[str]:
    if tolerance_dict is None:
        return None
    if isinstance(tolerance_dict, tuple):
        return tolerance_dict[1]

    for (list_test_sh_name, corresponding_key), tol in tolerance_dict.items():
        if dc_sys_sheet is not None:
            if dc_sys_sheet in list_test_sh_name:
                return tol[1]
        else:
            test_survey_type_names = SURVEY_TYPES_DICT[corresponding_key]["survey_type_names"]
            if survey_type.upper() in test_survey_type_names:
                return tol[1]
    return None


def _get_multiple_dc_sys_objets(sheet_name: str) -> Optional[list]:
    for val in SURVEY_TYPES_DICT.values():
        if val["res_sheet"] == sheet_name:
            return val.get("multiple_dc_sys_objets")
    print_error(f"{sheet_name = } not found inside SURVEY_TYPES_DICT:\n"
                f"{SURVEY_TYPES_DICT = }")
    return None


def _get_dc_sys_color(multiple_dc_sys_objets: Optional[list], dc_sys_sheet: str):
    list_colors = [XlBgColor.light_yellow, XlBgColor.light_orange, XlBgColor.light_pink, XlBgColor.light_red]
    if dc_sys_sheet is None:
        return list_colors[0]
    if not multiple_dc_sys_objets:
        return list_colors[0]
    for obj, color in zip(multiple_dc_sys_objets, list_colors):
        if obj == dc_sys_sheet:
            return color
    print_warning(f"{dc_sys_sheet = } not found inside multiple_dc_sys_objets or not enough colors defined:\n"
                  f"{multiple_dc_sys_objets = }\n"
                  f"{list_colors = }")
    return list_colors[0]


def _get_multiple_survey_objets(sheet_name: str) -> Optional[list[str]]:
    for val in SURVEY_TYPES_DICT.values():
        if val["res_sheet"] == sheet_name:
            return val.get("multiple_survey_objets")
    print_error(f"{sheet_name = } not found inside SURVEY_TYPES_DICT:\n"
                f"{SURVEY_TYPES_DICT = }")
    return None


def _get_survey_color(multiple_survey_objets: Optional[list[tuple]], survey_type: str):
    list_colors = [XlBgColor.light_green, XlBgColor.light_blue3, XlBgColor.light_blue2]
    if survey_type is None:
        return list_colors[0]
    if not multiple_survey_objets:
        return list_colors[0]
    for obj_name, color in zip(multiple_survey_objets, list_colors):
        list_survey_objects = SURVEY_TYPES_DICT[obj_name]["survey_type_names"]
        if survey_type.strip().upper() in list_survey_objects:
            return color
    print_warning(f"{survey_type = } not found inside multiple_survey_objets or not enough colors defined:\n"
                  f"{multiple_survey_objets = }\n"
                  f"{list_colors = }")
    return list_colors[0]
