#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pdfreader
import logging
from ...utils import *
from .parse_control_table import *


__all__ = ["control_tables_pdf_parsing"]



def control_tables_pdf_parsing(table_type: str, pdf_file: str, specific_pages: list[int] = None
                               ) -> dict[str, Any]:
    res_dict = dict()
    with open(pdf_file, "rb") as pdf:
        viewer = pdfreader.SimplePDFViewer(pdf)
        nbpages = len([p for p in viewer.doc.pages()])
        progress_bar(1, 1, end=True)  # reset progress_bar
        for num_page in range(1, nbpages + 1):
            if specific_pages is not None and num_page not in specific_pages:
                continue
            print_log(f"\r{progress_bar(num_page - 1, nbpages)} "
                      f"{Color.yellow}{table_type.title()}{Color.reset} "
                      f"{Color.white}Control Tables{Color.reset} conversion in-going...", end="")
            viewer.navigate(num_page)
            logging.disable(logging.WARNING)  # deactivate temporarily the warning logs
            viewer.render()
            logging.disable(logging.NOTSET)
            page_text = viewer.canvas.text_content
            page_text_info = _get_page_text_info(page_text)
            pos_dict, max_pos = _create_pos_dict(page_text_info)
            page_dict = analyze_pdf_info(table_type, num_page, pos_dict, max_pos)
            if page_dict:
                res_dict[page_dict["name"]["info"]] = {info["key_name"]: info["info"] for info in page_dict.values()}
        print_log(f"\r{progress_bar(nbpages, nbpages, end=True)} "
                  f"{Color.yellow}{table_type.title()}{Color.reset} "
                      f"{Color.white}Control Tables{Color.reset} conversion finished.")
    return res_dict


def _get_page_text_info(text: str) -> list[dict[str, Any]]:
    list_info = list()
    info = {"text": "", "extra_info": []}
    lines = text.splitlines()
    within_text_block = False
    for i, line in enumerate(lines):
        line = line.strip().replace(r"\\", "!!|").replace(r"\(", "!![").replace(r"\)", "!!]")
        if within_text_block:
            if line == "ET":
                if info["text"].strip():
                    list_info.append(info)
                within_text_block = False
            elif "(" in line and ")" in line:
                info["text"] += (_parse_text_line(line).replace("!!|", "\\")
                                 .replace("!![", "(").replace("!!]", ")"))
            else:
                info["extra_info"].append(line)
        if line == "BT":
            info = {"text": "", "extra_info": []}
            within_text_block = True
    return list_info


def _parse_text_line(line: str):
    text = str()
    while "(" in line:
        line_split = line.split("(", 1)[1].split(")", 1)
        text += line_split[0]
        line = line_split[1]
    return text


def _add_loc_info(list_info: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], tuple[float, float]]:
    for i, info in enumerate(list_info):
        loc = _get_loc_info(info)
        info["loc"] = loc
        list_info[i] = info
    max_pos = max(info["loc"][0] for info in list_info), max(info["loc"][1] for info in list_info)
    return list_info, max_pos


def _get_lines_to_merge(list_info: list[dict[str, Any]], max_pos: tuple[float, float]) -> list[tuple[int, int]]:
    tol_y = 120. * (max_pos[1] / 1000.)
    lines_to_merge = list()
    previous_x, previous_y = list_info[0]["loc"]
    for i, info in enumerate(list_info[1:], start=1):
        x, y = info["loc"]
        if (previous_x, previous_y) == (None, None) or (x, y) == (None, None):
            previous_x, previous_y = x, y
            continue
        if abs(x - previous_x) < 1. and (previous_y - tol_y) < y < previous_y:
            lines_to_merge.append((i-1, i))
        previous_x, previous_y = x, y
    return lines_to_merge


def _merge_next_lines(list_info: list[dict[str, Any]], max_pos: tuple[float, float]) -> list[dict[str, Any]]:
    lines_to_merge = _get_lines_to_merge(list_info, max_pos)
    for (i, j) in reversed(lines_to_merge):
        text = f"{list_info[i]['text']} {list_info[j]['text']}"
        list_info[i]["text"] = text
    for (_, j) in reversed(lines_to_merge):
        del list_info[j]
    return list_info


def _create_pos_dict(list_info: list[dict[str, Any]]) -> tuple[dict[tuple[float, float], str], tuple[float, float]]:
    list_info, max_pos = _add_loc_info(list_info)
    page_text_info_with_loc = _merge_next_lines(list_info, max_pos)
    pos_dict = dict()
    for info in page_text_info_with_loc:
        loc = info["loc"]
        if loc != (None, None):
            pos_dict[loc] = _clean_info(info["text"])
    return _sort_pos_dict(pos_dict), max_pos


def _get_loc_info(info) -> tuple[Optional[float], Optional[float]]:
    extra_info: list[str] = info["extra_info"]
    tm_info = str()
    td_info = str()
    for loc in extra_info:
        if loc.upper().endswith("TM"):  # Text transformation matrix (mx 0 0 my tx ty Tm)
            if not tm_info:
                tm_info = loc
        if loc.upper().endswith("TD"):  # Positioning text cursor (tx ty Td)
            if not td_info:
                td_info = loc
    if not tm_info and not td_info:
        return None, None
    if tm_info:
        tm_split = tm_info.split()
        x = float(tm_split[-3])
        y = float(tm_split[-2])
        if td_info and not x and not y:
            td_split = td_info.split()
            x_mult = float(tm_split[0])
            y_mult = float(tm_split[3])
            x += float(td_split[-3]) * x_mult
            y += float(td_split[-2]) * y_mult
    else:
        td_split = td_info.split()
        x = float(td_split[-3])
        y = float(td_split[-2])
    return round(x, 4), round(y, 4)


def _sort_pos_dict(pos_dict: dict[tuple[float, float], str]) -> dict[tuple[float, float], str]:
    return {key: pos_dict[key] for key in sorted(pos_dict, key=lambda x: (-x[1], x[0]))}

def _clean_info(info: str) -> str:
    info = re.sub(r"\s+", r" ", info)  # removing multiple spaces
    info = re.sub(r"\s*-\s*", r"-", info)  # removing spaces around hyphen character
    info = re.sub(r"[(]\s+", r"(", info)  # removing space inside parentheses
    info = re.sub(r"\s+[)]", r")", info)  # removing space inside parentheses
    info = re.sub(r"([^\s(])([(])", r"\1 \2", info)  # adding space outside parentheses
    info = re.sub(r"([)])([^\s)])", r"\1 \2", info)  # adding space outside parentheses
    info = re.sub(r"\s*,\s*", r", ", info)  # correctly format comma
    info = re.sub(r"(\")\s*(.*?)\s*(\")", r"\1\2\3", info)  # format spaces inside quotes
    info = re.sub(r"(\S)\s?(\".*?\")\s?(\S)", r"\1 \2 \3", info)  # format spaces outside quotes
    info = re.sub(r"(pass-by)(\S)", r"\1 \2", info)  # add a space after "pass-by"
    info = info.strip()
    return info
