#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import openpyxl.styles
from ..colors_pkg import *
from ..xl_pkg import *
from ..common_utils import *


__all__ = ["create_empty_verification_file", "create_empty_header_sheet"]


XL_THEME_XML = os.path.join(TEMPLATE_DIRECTORY, "xl_default_theme.xml")
LOGO_PATH = os.path.join(TEMPLATE_DIRECTORY, "logo_hitachi_global.png")

IMAGE_CELL = "B3"
TITLE_CELL = "B10"

AUTHOR_COLUMN = "C"
VERIFIER_COLUMN = "D"
APPROVER_COLUMN = "E"


def create_empty_verification_file() -> openpyxl.workbook.Workbook:
    wb = openpyxl.Workbook()
    # Modify openpyxl default theme to one more recent.
    # Openpyxl default theme (in openpyxl.writer.theme) corresponds to Excel 2007-2010.
    with open(XL_THEME_XML, "r", encoding="utf-8") as f:
        theme_xml = f.read()
    wb.loaded_theme = theme_xml
    # Delete default sheet
    wb.remove(wb.active)
    # Create Header sheet
    create_empty_header_sheet(wb)
    return wb


def create_empty_header_sheet(wb: openpyxl.workbook.Workbook):
    # Create Header sheet
    # When a sheet is created at index 0, it becomes the active sheet, so we need to restore the active sheet after.
    print_log(f" > Creating \"Header\" sheet...")
    active_ws = wb.active  # get active sheet
    wb.create_sheet("Header", 0)  # insert at first position
    if active_ws is not None:  # restore active sheet if any
        wb.active = active_ws

    header_ws = wb["Header"]
    # Set properties and display options for the sheet
    header_ws.sheet_properties.tabColor = "000000"  # black
    _set_columns_width(header_ws)
    header_ws.sheet_view.zoomScale = 100  # set zoom level to 100 %
    header_ws.sheet_view.showGridLines = False  # turn off gridlines display
    # Add logo
    add_image(header_ws, LOGO_PATH, IMAGE_CELL, target_width_cm=7.5, target_height_cm=4)
    # Select title cell
    select_cell(header_ws, TITLE_CELL)


def _set_columns_width(header_ws: xl_ws.Worksheet):
    header_ws.column_dimensions[AUTHOR_COLUMN].width = 31
    header_ws.column_dimensions[VERIFIER_COLUMN].width = 51
    header_ws.column_dimensions[APPROVER_COLUMN].width = 31
