#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import pdfreader
import logging
from ...utils import *
from ..ini_file import *
from .parse_control_table import *


__all__ = ["control_tables_pdf_parsing"]



def control_tables_pdf_parsing(table_type: str, pdf_file: str, specific_pages: list[int] = None,
                               debug: bool = False) -> dict[str, Any]:
    res_dict = dict()
    with open(pdf_file, "rb") as pdf:
        viewer = pdfreader.SimplePDFViewer(pdf)
        nbpages = len([p for p in viewer.doc.pages()])
        progress_bar(1, 1, end=True)  # reset progress_bar
        for num_page in range(1, nbpages + 1):
            if specific_pages is not None and num_page not in specific_pages:
                continue
            print_log(f"\r{progress_bar(num_page, nbpages)} "
                      f"{Color.yellow}{table_type.title()}{Color.reset} "
                      f"{Color.white}Control Tables{Color.reset} conversion in-going...", end="")
            viewer.navigate(num_page)
            logging.disable(logging.WARNING)  # deactivate temporarily the warning logs
            viewer.render()
            logging.disable(logging.NOTSET)
            page_text = viewer.canvas.text_content  # code of the PDF page
            page_text_info = _get_page_text_info(page_text)  # extract the text information from the code
            pos_dict, max_pos = _create_pos_dict(page_text_info)
            if debug:
                print()
                pretty_print_dict(pos_dict)
                print_bar()
            # Interpret the info collected with the Control Tables template
            page_dict = analyze_pdf_info(table_type, num_page, pos_dict, max_pos, debug=debug)
            if debug:
                sys.exit(1)
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
        # The backslash and parentheses characters are escaped in the PDF code.
        # We replace them by temporarily characters so that we can discriminate the parentheses that are not text
        # but internal PDF code symbol.
        line = line.strip().replace(r"\\", "!!|").replace(r"\(", "!![").replace(r"\)", "!!]")
        if within_text_block:
            if line == "ET":
                if info["text"].strip():
                    list_info.append(info)
                within_text_block = False
            elif "(" in line and ")" in line:
                # The characters of a same group can be split inside parentheses, we regroup them.
                text = _parse_text_line(line)
                # We restore back the actual text backslash and parentheses characters that were replaced,
                # and we remove the escaping character, so that it can be read properly.
                text = text.replace("!!|", "\\").replace("!![", "(").replace("!!]", ")")
                info["text"] += text
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
        loc, tf = _get_loc_info(info)
        info["loc"] = loc
        info["tf"] = tf
        list_info[i] = info
    max_pos = max(info["loc"][0] for info in list_info), max(info["loc"][1] for info in list_info)
    return list_info, max_pos


def _get_lines_to_merge(list_info: list[dict[str, Any]], max_pos: tuple[float, float]) -> list[tuple[int, int]]:
    tol_x = 100. * (max_pos[0] / 1000.)  # for titles on multiple instances
    neg_tol_y = 120. * (max_pos[1] / 1000.)
    pos_tol_x = 100. * (max_pos[0] / 1000.)  # for names on multiple instances
    lines_to_merge = list()
    previous_x, previous_y = list_info[0]["loc"]
    previous_tf = list_info[0]["tf"]
    for i, info in enumerate(list_info[1:], start=1):
        x, y = info["loc"]
        tf = info["tf"]
        if (previous_x, previous_y) == (None, None) or (x, y) == (None, None):
            previous_x, previous_y = x, y
            previous_tf = tf
            continue
        if ((abs(previous_x - x) < tol_x and (previous_y - neg_tol_y) < y < previous_y
                    and abs(previous_tf - tf) < .001)
                # around same x (with a tolerance for it to work for titles) and y below
                or (previous_x < x < (previous_x + pos_tol_x) and abs(previous_y - y) < .01)
                    and abs(previous_tf - tf) < .001):  # x right and same y for names
            lines_to_merge.append((i-1, i))
        previous_x, previous_y = x, y
        previous_tf = tf
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


def _get_loc_info(info) -> tuple[tuple[Optional[float], Optional[float]], Optional[float]]:
    extra_info: list[str] = info["extra_info"]
    tm_info = str()
    td_info = str()
    tf_info = str()
    for info in extra_info:
        if info.upper().endswith("TM"):  # Text transformation matrix (mx 0 0 my tx ty Tm)
            if not tm_info:
                tm_info = info
        if info.upper().endswith("TD"):  # Positioning text cursor (tx ty Td)
            if not td_info:
                td_info = info
        if info.upper().endswith("TF"):  # Font (/FONT_NAME font_size Tf)
            if not tf_info:
                tf_info = info
    if not tm_info and not td_info:
        return (None, None), 1.
    if tm_info:
        tm_split = tm_info.split()
        x_mult = float(tm_split[0])
        y_mult = float(tm_split[3])
        tf = (x_mult + y_mult) / 2.
        x = float(tm_split[-3])
        y = float(tm_split[-2])
        if td_info and not x and not y:
            td_split = td_info.split()
            x += float(td_split[-3]) * x_mult
            y += float(td_split[-2]) * y_mult
    else:
        td_split = td_info.split()
        x = float(td_split[-3])
        y = float(td_split[-2])
        tf = 1.
    if tf_info:
        tf_split = tf_info.split()
        tf *= float(tf_split[-2])
    return (round(x, 4), round(y, 4)), tf


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
    info = re.sub(r"([0-9]+) ([a-zA-Z])$", r"\1\2", info)  # delete space between numbers and simple letter
    info = info.strip()
    return info
