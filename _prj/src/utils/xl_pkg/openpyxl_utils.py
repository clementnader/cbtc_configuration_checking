#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PIL.Image
import openpyxl.comments as xl_comments
import openpyxl.drawing.image as xl_image
import openpyxl.workbook.defined_name as xl_defined_name
from .xl_utils import *
from ..common_utils import *


__all__ = ["add_cell_comment", "add_image", "create_defined_name", "select_cell"]


# ------ Cell Comment ------ #

def add_cell_comment(ws: xl_ws.Worksheet, comment: str,
                     cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    comment = xl_comments.Comment(comment, None)
    ws[cell].comment = comment


# ------ Image ------ #

def add_image(ws: xl_ws.Worksheet, image_path: str,
              cell: str = None, row: int = None, column: Union[str, int] = None,
              target_width_cm: float = None, target_height_cm: float = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)

    # Openpyxl uses 96 dpi by default. The image needs to be scaled using the same dpi.
    # We use PIL to get the dpi information.
    with (PIL.Image.open(image_path) as pil_img):
        width_dpi, height_dpi = pil_img.info["dpi"]
        width_px, height_px = pil_img.width, pil_img.height

    if target_width_cm is not None:
        width_cm = width_px / width_dpi * 2.54  # 1 inch = 2.54 cm
        ratio_width = target_width_cm / width_cm
    else:
        ratio_width = 1.

    if target_height_cm is not None:
        height_cm = height_px / height_dpi * 2.54  # 1 inch = 2.54 cm
        ratio_height = target_height_cm / height_cm
    else:
        ratio_height = 1.

    ratio = min(ratio_width, ratio_height, 1.)

    image = xl_image.Image(image_path)
    # We scale the width and height so that it corresponds to a 96 dpi image.
    image.width *= 96. / width_dpi * ratio
    image.height *= 96. / height_dpi * ratio

    ws.add_image(image, anchor=cell)


# ------ Defined Name ------ #

def create_defined_name(wb: openpyxl.workbook.Workbook, sheet_name: str, name: str,
                        cell: str = None, row: int = None, column: Union[str, int] = None):
    cell = get_cell_from_row_and_column(cell, row, column)

    ref = f"{xl_ut.quote_sheetname(sheet_name)}!{xl_ut.absolute_coordinate(cell)}"
    defined_name = xl_defined_name.DefinedName(name, attr_text=ref)
    wb.defined_names.add(defined_name)


# ------ Select Cell ------ #

def select_cell(ws: xl_ws.Worksheet,
                cell: str = None, row: int = None, column: Union[str, int] = None) -> None:
    cell = get_cell_from_row_and_column(cell, row, column)
    ws.sheet_view.selection[0].activeCell = cell
    ws.sheet_view.selection[0].sqref = cell
