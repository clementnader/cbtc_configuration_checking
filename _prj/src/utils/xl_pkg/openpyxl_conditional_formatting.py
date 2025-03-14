#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl.styles as xl_styles
import openpyxl.styles.differential as xl_diff_styles
import openpyxl.formatting as xl_format
import openpyxl.formatting.rule as xl_format_rule
from .xl_utils import *
from ..common_utils import *


__all__ = ["add_unique_values_conditional_formatting", "add_duplicate_values_conditional_formatting",
           "add_is_equal_conditional_formatting", "add_formula_conditional_formatting"]


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

def add_unique_values_conditional_formatting(ws: xl_ws.Worksheet, cell_range: str,
                                             font_color: str, bg_color: str, bold: bool = False) -> None:
    dxf = _get_differential_style(font_color, bg_color, bold)
    if dxf is None:
        return
    rule = xl_format.Rule(type="uniqueValues", priority=1, dxf=dxf)
    ws.conditional_formatting.add(cell_range, rule)


def add_duplicate_values_conditional_formatting(ws: xl_ws.Worksheet, cell_range: str,
                                                font_color: str, bg_color: str, bold: bool = False) -> None:
    dxf = _get_differential_style(font_color, bg_color, bold)
    if dxf is None:
        return
    rule = xl_format.Rule(type="duplicateValues", priority=1, dxf=dxf)
    ws.conditional_formatting.add(cell_range, rule)


def add_is_equal_conditional_formatting(ws: xl_ws.Worksheet, cell_range: str,
                                        value: Union[str, float, int],
                                        font_color: str = None, bg_color: str = None, bold: bool = False) -> None:
    dxf = _get_differential_style(font_color, bg_color, bold)
    if dxf is None:
        return
    formula_rule = xl_format.Rule(type="cellIs", operator="equal", formula=[value], dxf=dxf)
    ws.conditional_formatting.add(cell_range, formula_rule)


def _get_font_n_fill(font_color: str = None, bg_color: str = None, bold: bool = False):
    if font_color is not None and bold:
        font = xl_styles.Font(color=font_color, bold=True)
    elif font_color is not None:
        font = xl_styles.Font(color=font_color)
    elif bold:
        font = xl_styles.Font(bold=True)
    else:
        font = None
    if bg_color is not None:
        fill = xl_styles.PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    else:
        fill = None
    return font, fill


def _get_differential_style(font_color: str = None, bg_color: str = None, bold: bool = False):
    font, fill = _get_font_n_fill(font_color, bg_color, bold)
    if font is not None and fill is not None:
        dxf = xl_diff_styles.DifferentialStyle(font=font, fill=fill)
    elif font is not None:
        dxf = xl_diff_styles.DifferentialStyle(font=font)
    elif fill is not None:
        dxf = xl_diff_styles.DifferentialStyle(fill=fill)
    else:
        dxf = None
    return dxf


def add_formula_conditional_formatting(ws: xl_ws.Worksheet, cell_range: str, formula: str,
                                       font_color: str, bg_color: str, bold: bool = False) -> None:
    font, fill = _get_font_n_fill(font_color, bg_color, bold)
    if font is not None and fill is not None:
        formula_rule = xl_format_rule.FormulaRule(formula=[formula], stopIfTrue=True, font=font, fill=fill)
    elif font is not None:
        formula_rule = xl_format_rule.FormulaRule(formula=[formula], stopIfTrue=True, font=font)
    elif fill is not None:
        formula_rule = xl_format_rule.FormulaRule(formula=[formula], stopIfTrue=True, fill=fill)
    else:
        return
    ws.conditional_formatting.add(cell_range, formula_rule)
