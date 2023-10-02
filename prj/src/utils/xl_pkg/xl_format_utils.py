#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl.comments as xl_comments
import openpyxl.styles as xl_styles
import openpyxl.styles.differential as xl_diff_styles
import openpyxl.styles.borders as xl_borders
import openpyxl.formatting as xl_format
import openpyxl.formatting.rule as xl_format_rule
import openpyxl.worksheet.worksheet

from .xl_utils import *
from ..common_utils import *


__all__ = ["XlFontColor", "XlBgColor", "get_xl_bg_dimmer_color", "add_cell_comment",
           "create_cell", "create_merged_cell",
           "set_font_size", "set_bold_font", "set_bg_color",
           "center_vertical_alignment", "center_horizontal_alignment", "enable_line_wrap",
           "draw_exterior_borders", "draw_exterior_borders_on_range",
           "add_duplicate_values_conditional_formatting", "add_formula_conditional_formatting"]


class XlFontColor:
    ko = "9C0006"
    ok = "006100"
    na = "9C5700"


class XlBgColor:
    ko = "FFC7CE"
    ok = "C6EFCE"
    na = "FFEB9C"
    yellow = "FFE699"
    light_yellow = "FFF2CC"
    green = "C6E0B4"
    light_green = "E2EFDA"
    blue = "BDD7EE"
    light_blue = "DDEBF7"


def get_xl_bg_dimmer_color(bg: str):
    xl_bg_colors_dict = get_class_attr_dict(XlBgColor)
    for key, val in xl_bg_colors_dict.items():
        if bg == val:
            if key.startswith("light_"):
                dimmer_key = key.removeprefix("light_")
                if dimmer_key in xl_bg_colors_dict:
                    return xl_bg_colors_dict[dimmer_key]
    return bg


# ------ Cell Comment ------ #

def add_cell_comment(ws: openpyxl.worksheet.worksheet.Worksheet, comment: str,
                     cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    comment = xl_comments.Comment(comment, None)
    ws[cell].comment = comment


# ------ Cell Formatting ------ #

def create_cell(ws: openpyxl.worksheet.worksheet.Worksheet, value: Union[str, float, None],
                cell: str = None, row: int = None, column: Union[str, int] = None,
                font_size: int = None, bold: bool = False, italic: bool = False, bg_color: str = None,
                center_vertical: bool = True, center_horizontal: bool = False, line_wrap: bool = False,
                borders: bool = False) -> None:
    row, column = get_row_and_column_from_cell(cell, row, column)

    ws.cell(row=row, column=column, value=value)
    # Cell Formatting
    _update_cell_formatting(ws, row, column, font_size, bold, italic, bg_color, center_vertical, center_horizontal,
                            line_wrap)
    # Cell Borders
    if borders:
        draw_exterior_borders(ws, row=row, column=column)


def create_merged_cell(ws: openpyxl.worksheet.worksheet.Worksheet, value: str,
                       start_cell: str = None, start_row: int = None, start_column: Union[str, int] = None,
                       end_cell: str = None, end_row: int = None, end_column: Union[str, int] = None,
                       font_size: int = None, bold: bool = False, italic: bool = False, bg_color: str = None,
                       center_vertical: bool = True, center_horizontal: bool = False,
                       line_wrap: bool = True,
                       borders: bool = False) -> None:
    start_row, start_column = get_row_and_column_from_cell(start_cell, start_row, start_column)
    end_row, end_column = get_row_and_column_from_cell(end_cell, end_row, end_column)

    ws.merge_cells(start_row=start_row, end_row=end_row,
                   start_column=start_column, end_column=end_column)
    ws.cell(row=start_row, column=start_column, value=value)
    # Cell Formatting
    _update_cell_formatting(ws, start_row, start_column, font_size, bold, italic, bg_color, center_vertical,
                            center_horizontal, line_wrap)
    # Cell Borders
    if borders:
        draw_exterior_borders_on_range(ws, start_row=start_row, end_row=end_row,
                                       start_column=start_column, end_column=end_column)


def _update_cell_formatting(ws: openpyxl.worksheet.worksheet.Worksheet, row: int, column: int,
                            font_size: int, bold: bool, italic: bool, bg_color: str,
                            center_vertical: bool, center_horizontal: bool,
                            line_wrap: bool) -> None:
    if font_size is not None:
        set_font_size(ws, font_size=font_size, row=row, column=column)
    if bold:
        set_bold_font(ws, row=row, column=column)
    if italic:
        set_italic_font(ws, row=row, column=column)
    if bg_color is not None:
        set_bg_color(ws, hex_color=bg_color, row=row, column=column)
    if center_vertical:
        center_vertical_alignment(ws, row=row, column=column)
    if center_horizontal:
        center_horizontal_alignment(ws, row=row, column=column)
    if line_wrap:
        enable_line_wrap(ws, row=row, column=column)


def set_font_size(ws: openpyxl.worksheet.worksheet.Worksheet, font_size: int,
                  cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    font_style = openpyxl.styles.Font(size=font_size)
    ws[cell].font = font_style


def set_bold_font(ws: openpyxl.worksheet.worksheet.Worksheet,
                  cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    font_style = openpyxl.styles.Font(bold=True)
    ws[cell].font += font_style


def set_italic_font(ws: openpyxl.worksheet.worksheet.Worksheet,
                    cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    font_style = openpyxl.styles.Font(italic=True)
    ws[cell].font += font_style


def set_bg_color(ws: openpyxl.worksheet.worksheet.Worksheet, hex_color: str,
                 cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    pattern_style = xl_styles.PatternFill(start_color=hex_color, end_color=hex_color, fill_type="solid")
    ws[cell].fill = pattern_style


def center_vertical_alignment(ws: openpyxl.worksheet.worksheet.Worksheet,
                              cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    alignment_style = xl_styles.Alignment(vertical="center")
    ws[cell].alignment += alignment_style


def center_horizontal_alignment(ws: openpyxl.worksheet.worksheet.Worksheet,
                                cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    alignment_style = xl_styles.Alignment(horizontal="center")
    ws[cell].alignment += alignment_style


def enable_line_wrap(ws: openpyxl.worksheet.worksheet.Worksheet,
                     cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    alignment_style = openpyxl.styles.Alignment(wrap_text=True)
    ws[cell].alignment += alignment_style


# ------ Cell Borders ------ #

def draw_exterior_borders(ws: openpyxl.worksheet.worksheet.Worksheet,
                          cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    side = xl_borders.Side(border_style="thin")
    border = xl_borders.Border(left=side, right=side, top=side, bottom=side)
    ws[cell].border = border


def draw_exterior_borders_on_range(ws: openpyxl.worksheet.worksheet.Worksheet, cell_range: str = None,
                                   start_row: int = None, end_row: int = None,
                                   start_column: Union[int, str] = None, end_column: Union[int, str] = None) -> None:
    cell_range = get_cell_range(cell_range, start_row, end_row, start_column, end_column)
    side = xl_borders.Side(border_style="thin")
    border = xl_borders.Border(left=side, right=side, top=side, bottom=side)
    for row in ws[cell_range]:
        for cell in row:
            cell.border = border


# ------ Conditional Formatting ------ #

# xl_format.Rule
#   rule type: ['expression', 'cellIs', 'colorScale', 'dataBar', 'iconSet', 'top10', 'uniqueValues',
# 'duplicateValues', 'containsText', 'notContainsText', 'beginsWith', 'endsWith', 'containsBlanks',
# 'notContainsBlanks', 'containsErrors', 'notContainsErrors', 'timePeriod', 'aboveAverage']
#   rule priority: int
#   rule stopIfTrue: bool
#   rule operator: ['lessThan', 'lessThanOrEqual', 'equal', 'notEqual', 'greaterThanOrEqual', 'greaterThan',
# 'between', 'notBetween', 'containsText', 'notContains', 'beginsWith', 'endsWith']
#   rule formula: list[str]
#   rule dxf: DifferentialStyle

def add_duplicate_values_conditional_formatting(ws: openpyxl.worksheet.worksheet.Worksheet, cell_range: str,
                                                font_color: str, bg_color: str) -> None:
    font = xl_styles.Font(color=font_color)
    fill = xl_styles.PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    dxf = xl_diff_styles.DifferentialStyle(font=font, fill=fill)
    rule = xl_format.Rule(type="duplicateValues", priority=1, dxf=dxf)
    ws.conditional_formatting.add(cell_range, rule)


def add_formula_conditional_formatting(ws: openpyxl.worksheet.worksheet.Worksheet, cell_range: str, formula: str,
                                       font_color: str, bg_color: str) -> None:
    font = xl_styles.Font(color=font_color)
    fill = xl_styles.PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    formula_rule = xl_format_rule.FormulaRule(formula=[formula], stopIfTrue=True, font=font, fill=fill)
    ws.conditional_formatting.add(cell_range, formula_rule)
