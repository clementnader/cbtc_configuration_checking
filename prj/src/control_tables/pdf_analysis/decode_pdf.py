#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Check Adobe Systems Incorporated "Portable Document Format Reference Manual" for PDF Text Operators
# (see https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.0.pdf)

import sys
import re
import pdfreader
import logging
from ...utils import *
from .parse_control_table import *


__all__ = ["control_tables_pdf_parsing"]


def control_tables_pdf_parsing(table_type: str, pdf_file: str, specific_pages: list[int] = None,
                               debug: bool = False, print_pdf_code: bool = False) -> dict[str, Any]:
    res_dict = dict()
    with open(pdf_file, "rb") as pdf:
        viewer = pdfreader.SimplePDFViewer(pdf)
        nbpages = len([p for p in viewer.doc.pages()])
        progress_bar(1, 1, end=True)  # reset progress_bar
        for num_page in range(1, nbpages + 1):
            if specific_pages is not None and num_page not in specific_pages:
                continue
            print_log_progress_bar(num_page, nbpages, f"{Color.yellow}{table_type.title()}{Color.reset} "
                                   f"{Color.white}Control Tables{Color.reset} conversion ongoing")
            viewer.navigate(num_page)
            logging.disable(logging.WARNING)  # deactivate temporarily the warning logs
            viewer.render()
            logging.disable(logging.NOTSET)
            page_text = viewer.canvas.text_content  # code of the PDF page
            # Extract the text information from the code
            page_text_info = _get_page_text_info(page_text)
            if print_pdf_code:
                print()
                pretty_print_dict(page_text_info)
                print_bar()
            # Create a dictionary with the position and the associated text (using the Text string operators)
            # and try and merge consecutive lines if any.
            pos_dict, max_pos = _create_pos_dict(page_text_info)
            if debug:
                print()
                pretty_print_dict(pos_dict)
                print_bar()
            if print_pdf_code:
                sys.exit(1)
            # Interpret the collected info using the Control Tables template
            page_dict = analyze_pdf_info(table_type, num_page, pos_dict, max_pos, debug=debug)
            if debug:
                print()
                pretty_print_dict(page_dict)
                print_bar()
                sys.exit(1)
            if page_dict:
                res_dict[page_dict["name"]["info"]] = {info["key_name"]: {"text": info["info"],
                                                                          "csv_title": info["csv_title"]}
                                                       for info in page_dict.values()}
        print_log_progress_bar(nbpages, nbpages, f"{Color.yellow}{table_type.title()}{Color.reset} "
                               f"{Color.white}Control Tables{Color.reset} conversion finished", end=True)
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
            if line == "ET":  # Ends a text object
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
        if line == "BT":  # Begins a text object
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
        loc, tf, font, tc = _get_loc_info(info)
        info["loc"] = loc
        info["tf"] = tf
        info["font"] = font
        info["tc"] = tc
        list_info[i] = info
    max_x = max(info["loc"][0] for info in list_info) - min(info["loc"][0] for info in list_info)
    # we have to do a delta because the loc can be negative and so the minimum is not always zero
    max_y = max(info["loc"][1] for info in list_info) - min(info["loc"][1] for info in list_info)
    # we have to do a delta because the loc can be negative and so the minimum is not always zero
    max_pos = max_x, max_y
    return list_info, max_pos


def _get_lines_to_merge(list_info: list[dict[str, Any]], max_pos: tuple[float, float]) -> list[tuple[int, int]]:
    tol_x = 100. * (max_pos[0] / 1000.)  # for titles on multiple instances
    neg_tol_y = 120. * (max_pos[1] / 1000.)
    pos_tol_x = 80. * (max_pos[0] / 1000.)  # for names on multiple instances

    lines_to_merge = list()
    previous_text = list_info[0]["text"]
    previous_x, previous_y = list_info[0]["loc"]
    previous_tf = list_info[0]["tf"]
    previous_font = list_info[0]["font"]
    previous_tc = list_info[0]["tc"]

    for i, info in enumerate(list_info[1:], start=1):
        text = list_info[0]["text"]
        x, y = info["loc"]
        tf = info["tf"]
        font = info["font"]
        tc = info["tc"]

        if (previous_x, previous_y) == (None, None) or (x, y) == (None, None):
            previous_text = text
            previous_x, previous_y = x, y
            previous_tf = tf
            previous_font = font
            previous_tc = tc
            continue

        if (((previous_font == font) and (previous_tc == tc) and abs(previous_tf - tf) < .001)
                # same font, same character spacing and same font size
                and ("[" not in previous_text
                     and (abs(previous_x - x) < .01 and (previous_y - neg_tol_y) < y < previous_y)
                    # for not titles, same x and y down
                    or "[" in previous_text
                     and (abs(previous_x - x) < tol_x and (previous_y - neg_tol_y) < y < previous_y)
                    # for titles, it can be center-aligned, so we put a tolerance on x (y down)
                    or (previous_x < x < (previous_x + pos_tol_x) and abs(previous_y - y) < .01))):
                    # x right and same y for names
            lines_to_merge.append((i-1, i))

        previous_x, previous_y = x, y
        previous_tf = tf
        previous_font = font
        previous_tc = tc
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


def _get_loc_info(pdf_info
                  ) -> tuple[tuple[Optional[float], Optional[float]], Optional[float], Optional[str], Optional[float]]:
    extra_info: list[str] = pdf_info["extra_info"]
    tm_info = str()
    td_info = str()
    tf_info = str()
    tc_info = str()
    for info in extra_info:
        if info.endswith("Tm"):  # Text matrix (a b c d e f Tm)
            if not tm_info:
                tm_info = info
        if info.endswith("Td") or info.endswith("TD"):  # Text displacement (tx ty Td) or (tx ty TD)
            if not td_info:
                td_info = info
        if info.endswith("Tf"):  # Font and size (fontname size Tf)
            if not tf_info:
                tf_info = info
        if info.endswith("Tc"):  # Character spacing (charSpace Tc)
            if not tc_info:
                tc_info = info
    if not tm_info and not td_info:
        return (None, None), 1., None, None

    x, y = 1., 1.  # when BT is reached, initialize the text matrix to the identity matrix.

    if td_info:  # Text displacement (tx ty Td) (tx ty TD)
        td_split = td_info.split()
        tx = float(td_split[0])
        ty = float(td_split[1])
        x += tx
        y += ty

    if tm_info:  # Text matrix (a b c d e f Tm)
        tm_split = tm_info.split()
        a = float(tm_split[0])
        b = float(tm_split[1])
        c = float(tm_split[2])
        d = float(tm_split[3])
        e = float(tm_split[4])
        f = float(tm_split[5])
        x = a*x + c*y + e
        y = b*x + d*y + f

    if tf_info:
        tf_split = tf_info.split()
        tf = float(tf_split[1])
        font = tf_split[0]
    else:
        tf = 1.
        font = None

    if tc_info:
        tc_split = tc_info.split()
        tc = float(tc_split[0])
    else:
        tc = None

    return (round(x, 4), round(y, 4)), tf, font, tc


def _sort_pos_dict(pos_dict: dict[tuple[float, float], str]) -> dict[tuple[float, float], str]:
    return {key: pos_dict[key] for key in sorted(pos_dict, key=lambda x: (-x[1], x[0]))}

def _clean_info(info: str) -> str:
    info = info.replace("\\t", "")  # remove tabulation symbols
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
