#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdfreader
from ..utils import *
from .pdf_loc_info_pdf_overlap import loc_info_pdf_overlap
from .pdf_loc_info_pdf_route import loc_info_pdf_route


class CONTROL_TABLE_TYPE:
    route = "route"
    overlap = "overlap"


def pdf_reader_extract_tables(pdf_file: str, table_type: str, cmc: bool = False) -> dict:
    res_dict = dict()
    with open(pdf_file, "rb") as pdf:
        viewer = pdfreader.SimplePDFViewer(pdf)
        nbpages = len([p for p in viewer.doc.pages()])
        for num_page in range(1, nbpages + 1):
            if table_type == CONTROL_TABLE_TYPE.overlap or num_page % 5 == 0:
                print_log(f"\t {(num_page-1) / nbpages:.2%} {table_type.title()} Control Tables "
                          f"for {'CMC' if cmc else 'Line'} conversion in-going...")
            viewer.navigate(num_page)
            viewer.render()
            page_text = viewer.canvas.text_content
            page_dict = _parse_page_text(page_text, table_type, num_page)
            if page_dict:
                res_dict[page_dict["Name"]] = page_dict
    return res_dict


def _parse_page_text(text: str, table_type: str, num_page: int) -> dict[str, str]:
    list_info = list()
    info = {"text": "", "extra_info": []}
    lines = text.splitlines()
    within_text_block = False
    for line in lines:
        line = line.strip().replace(r"\\", "!!|").replace(r"\(", "!![").replace(r"\)", "!!]")
        if within_text_block:
            if line == "ET":
                info["text"] = info["text"].strip()
                list_info.append(info)
                within_text_block = False
            elif "(" in line and ")" in line:
                info["text"] += _parse_text_line(line).replace("!!|", "\\").replace("!![", "(").replace("!!]", ")")
            else:
                info["extra_info"].append(line)
        if line == "BT":
            info = {"text": "", "extra_info": []}
            within_text_block = True
    return _extract_info(list_info, table_type, num_page)


def _parse_text_line(line: str):
    text = str()
    while "(" in line:
        line_split = line.split("(", 1)[1].split(")", 1)
        text += line_split[0]
        line = line_split[1]
    return text


def _extract_info(list_info: list[dict[str]], table_type: str, num_page: int) -> dict[str, str]:
    if table_type == CONTROL_TABLE_TYPE.route:
        loc_dict = loc_info_pdf_route()
    elif table_type == CONTROL_TABLE_TYPE.overlap:
        loc_dict = loc_info_pdf_overlap()
    else:
        return {}

    res_dict = {key: "" for key in loc_dict}
    if not _check_useful_page(list_info, num_page):
        return {}
    for info in list_info:
        loc: str = _get_loc_info(info)
        text: str = info["text"]
        for key, loc_ref in loc_dict.items():
            if _does_pos_correspond(loc, loc_ref):
                res_dict[key] += text
    _check_correct_res_dict(res_dict, list_info)
    return res_dict


def _check_useful_page(list_info: list[dict[str]], num_page: int):
    if num_page < 3:
        return False
    loc_ref = {"x": 55, "y": 752, "x_tol": 30, "y_tol": 30}
    for info in list_info:
        loc: str = _get_loc_info(info)
        text: str = info["text"]
        if not loc:
            continue
        if _does_pos_correspond(loc, loc_ref):
            if text.strip() == "Name":
                return True
        if text.strip() == "Name":
            print_warning(f"Name information does not seem to be at the correct place."
                          f"for page {Color.beige}{num_page}{Color.reset}.")
    return False


def _get_loc_info(info):
    extra_info: list[str] = info["extra_info"]
    for loc in extra_info:
        if loc.endswith("Tm"):
            return loc
    return None


def _does_pos_correspond(loc: str, loc_ref: dict[str, float]):
    x_ref = loc_ref["x"]
    y_ref = loc_ref["y"]
    x_tol = loc_ref.get("x_tol", 5)
    y_tol = loc_ref.get("y_tol", 5)

    loc_split = loc.split()
    x = float(loc_split[4])
    y = float(loc_split[5])
    if loc_split[6] != "Tm":
        return False

    if abs(x - x_ref) <= x_tol and abs(y - y_ref) <= y_tol:
        return True
    return False


def _check_correct_res_dict(res_dict, list_info):
    if any(text == "" for text in res_dict.values()):
        print_error(f"Not all information has been parsed from the pdf:")
        for key, val in res_dict.items():
            print("\t-", key, ":", val)
        print(f"The pdf information is the following")
        for info in list_info:
            print(info)
        print("\n")
