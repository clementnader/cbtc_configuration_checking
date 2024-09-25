#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pdfreader
# import pypdf
import logging
import re
from ..utils import *
from .pdf_loc_info_pdf_overlap import loc_info_pdf_overlap
from .pdf_loc_info_pdf_route import loc_info_pdf_route
from .pdf_extract_functions import *


__all__ = ["CONTROL_TABLE_TYPE", "pdf_reader_extract_tables"]


NAME_TITLES = ["Name", "Name [0]", "Name[0]"]


def pdf_reader_extract_tables(pdf_file: str, table_type: str, verbose: bool = False,
                              specific_page: int = None, new_method: bool = False) -> dict[str, Any]:
    pdf_name = os.path.split(pdf_file)[-1]
    print_section_title(f"Conversion of {Color.turquoise}{table_type.title()}{Color.reset} "
                        f"{Color.mint_green}Control Tables{Color.reset} for {Color.yellow}{pdf_name}{Color.reset}...")
    res_dict = dict()
    # new_method = False
    # if new_method:
    #     reader = pypdf.PdfReader(pdf_file)
    #     nbpages = len(reader.pages)
    #     progress_bar(1, 1, end=True)  # reset progress_bar
    #     for num_page, page in enumerate(reader.pages, start=1):
    #         if specific_page is not None and num_page != specific_page:
    #             continue
    #         print_log(f"\r{progress_bar(num_page, nbpages)} "
    #                   f"{Color.turquoise}{table_type.title()}{Color.reset} "
    #                   f"{Color.mint_green}Control Tables{Color.reset} conversion in-going...", end="")
    #         page_text = page.extract_text(extraction_mode="layout", layout_mode_scale_weight=1)
    #         if verbose:
    #             print()
    #             print(page_text)
    #             print_bar()
    #         page_dict = _clean_res_dict_new_method(parse_pdf_control_table(page_text, num_page, table_type))
    #         if page_dict is not None:
    #             res_dict[page_dict["name"]["info"]] = page_dict
    #     print_log(f"\r{progress_bar(nbpages, nbpages, end=True)} "
    #               f"{Color.turquoise}{table_type.title()}{Color.reset} "
    #               f"{Color.mint_green}Control Tables{Color.reset} conversion finished.")
    # else:
    with open(pdf_file, "rb") as pdf:
        viewer = pdfreader.SimplePDFViewer(pdf)
        nbpages = len([p for p in viewer.doc.pages()])
        progress_bar(1, 1, end=True)  # reset progress_bar
        for num_page in range(1, nbpages + 1):
            if specific_page is not None and num_page != specific_page:
                continue
            print_log(f"\r{progress_bar(num_page - 1, nbpages)} "
                      f"{Color.turquoise}{table_type.title()}{Color.reset} "
                      f"{Color.mint_green}Control Tables{Color.reset} conversion in-going...", end="")
            viewer.navigate(num_page)
            logging.disable(logging.WARNING)  # deactivate temporarily the warning logs
            # TODO: use warnings.filterwarnings
            viewer.render()
            logging.disable(logging.NOTSET)
            page_text = viewer.canvas.text_content
            print(page_text)
            page_dict = _parse_page_text(page_text, table_type, num_page, verbose=verbose)
            if page_dict:
                res_dict[page_dict["Name"]] = page_dict
        print_log(f"\r{progress_bar(nbpages, nbpages, end=True)} "
                  f"{Color.turquoise}{table_type.title()}{Color.reset} "
                  f"{Color.mint_green}Control Tables{Color.reset} conversion finished.")
    return res_dict


def _parse_page_text(text: str, table_type: str, num_page: int, verbose: bool = False) -> dict[str, str]:
    list_info = list()
    info = {"text": "", "extra_info": []}
    lines = text.splitlines()
    within_text_block = False
    for i, line in enumerate(lines):
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
    return _extract_info(list_info, table_type, num_page, verbose=verbose)


def _parse_text_line(line: str):
    text = str()
    while "(" in line:
        line_split = line.split("(", 1)[1].split(")", 1)
        text += line_split[0]
        line = line_split[1]
    return text


def _extract_info(list_info: list[dict[str, Any]], table_type: str, num_page: int, verbose: bool = False
                  ) -> dict[str, str]:
    if table_type == CONTROL_TABLE_TYPE.route:
        loc_dict = loc_info_pdf_route()
    elif table_type == CONTROL_TABLE_TYPE.overlap:
        loc_dict = loc_info_pdf_overlap()
    else:
        return {}

    res_dict = {key: "" for key in loc_dict if key != "Name_Title"}
    verbose_dict = {key: None for key in loc_dict}
    list_info = _add_pos_list_info(list_info)
    useful_page, verbose_dict, left_name = _check_useful_page(list_info, num_page, loc_dict["Name_Title"], verbose_dict)
    if not useful_page:
        return {}
    if left_name is not None:
        key = "Name"
        loc = verbose_dict["Name_Title"]["loc"][0]
        text: str = left_name
        res_dict[key] += " " + text
        if verbose_dict[key] is not None:
            verbose_dict[key]["loc"].append(loc)
            verbose_dict[key]["text"] += " " + text
        else:
            verbose_dict[key] = {"loc": [loc], "text": text}
    for info in list_info:
        loc: dict[str, float] = info["loc"]
        text: str = info["text"]
        for key, loc_ref in loc_dict.items():
            if key != "Name_Title":
                if _does_pos_correspond(loc, loc_ref):
                    if not any(text.lstrip().startswith(_key.split("]", 1)[0] + "]") for _key in loc_dict
                               if _key.startswith("[")):
                        res_dict[key] += " " + text
                        loc = {key: round(loc[key]) for key in loc}
                        if verbose_dict[key] is not None:
                            verbose_dict[key]["loc"].append(loc)
                            verbose_dict[key]["text"] += " " + text
                        else:
                            verbose_dict[key] = {"loc": [loc], "text": text}
    if verbose:
        print()
        for i, (key, val) in enumerate(verbose_dict.items()):
            if val:
                loc = val["loc"]
                text = val["text"]
                color = Color.light_blue if i % 2 == 0 else Color.pale_green
                print(f"{key = }, loc={color}{loc}{Color.reset}, text={Color.yellow}{text}{Color.reset}")
            else:
                print(f"{Color.orange}{key = }{Color.reset} information not found")
        print()
    _check_correct_res_dict(res_dict, num_page, list_info)
    return _clean_res_dict(res_dict)


def _clean_res_dict(res_dict: dict[str, str]) -> dict[str, str]:
    for key, val in res_dict.items():
        val = re.sub(r"\s+", r" ", val)  # removing multiple spaces
        val = re.sub(r"\s*-\s*", r"-", val)  # removing spaces around hyphen character
        val = re.sub(r"[(]\s*", r"(", val)  # removing space inside parentheses
        val = re.sub(r"\s*[)]", r")", val)  # removing space inside parentheses
        val = re.sub(r"\s*,\s*", r", ", val)  # correctly format comma
        val = re.sub(r"^([A-Z])\s([A-Za-z])", r"\1\2", val)  # removing space inside word
        val = re.sub(r"([0-9])\s([0-9])", r"\1\2", val)  # removing space inside word
        val = re.sub(r"(\s[A-Z])\s([A-Za-z])", r"\1\2", val)  # removing space inside word
        val = re.sub(r"([A-Za-z])\s([A-Za-z0-9])$", r"\1\2", val)  # removing space inside word
        val = re.sub(r"([A-Za-z])\s([A-Za-z0-9][\s,])", r"\1\2", val)  # removing space inside word
        val = val.strip()
        if (val.endswith(",") or val.endswith("_") or val.endswith(".")
                or (val != "--" and val.endswith("-"))
                or val.count("(") != val.count(")")):
            print_warning(f"Key {Color.blue}{key}{Color.reset} is on multiple lines "
                          f"and it was not completely parsed from the Control Tables:")
            print(f"{val = }\n")
        res_dict[key] = val
    return res_dict


def _clean_res_dict_new_method(res_dict: dict[str, dict[str, str]]) -> Optional[dict[str, dict[str, str]]]:
    if res_dict is None:
        return None
    for key, val in res_dict.items():
        info = val["info"]
        info = re.sub(r"\s+", r" ", info)  # removing multiple spaces
        info = re.sub(r"\s*-\s*", r"-", info)  # removing spaces around hyphen character
        info = re.sub(r"[(]\s*", r"(", info)  # removing space inside parentheses
        info = re.sub(r"\s*[)]", r")", info)  # removing space inside parentheses
        info = re.sub(r"\s*,\s*", r", ", info)  # correctly format comma
        info = re.sub(r"^([A-Z])\s([A-Za-z])", r"\1\2", info)  # removing space inside word
        info = re.sub(r"([0-9])\s([0-9])", r"\1\2", info)  # removing space inside word
        info = re.sub(r"(\s[A-Z])\s([A-Za-z])", r"\1\2", info)  # removing space inside word
        info = re.sub(r"([A-Za-z])\s([A-Za-z0-9])$", r"\1\2", info)  # removing space inside word
        info = re.sub(r"([A-Za-z])\s([A-Za-z0-9][\s,])", r"\1\2", info)  # removing space inside word
        info = info.strip()
        if (info.endswith(",") or info.endswith("_") or info.endswith(".")
                or (info != "--" and info.endswith("-"))
                or info.count("(") != info.count(")")):
            print_warning(f"Key {Color.blue}{res_dict[key]['key_name']}{Color.reset} is on multiple lines "
                          f"and it was not completely parsed from the Control Tables:")
            print(f"{val = }\n")
        res_dict[key]["info"] = info
    return res_dict


def _add_pos_list_info(list_info: list[dict[str, Any]]):
    for i, info in enumerate(list_info):
        loc = _get_loc_info(info)
        list_info[i]["loc"] = loc
    return list_info


def _get_loc_info(info) -> dict[str, float]:
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
        return {}
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
    return {"x": x, "y": y}


def _check_useful_page(list_info: list[dict[str, Any]], num_page: int, loc_ref: dict[str, float], verbose_dict: dict):
    for info in list_info:
        loc: dict[str, float] = info["loc"]
        text: str = info["text"]
        if not loc:
            continue
        if _does_pos_correspond(loc, loc_ref):
            if text.strip() in NAME_TITLES:
                loc = {key: round(loc[key]) for key in loc}
                verbose_dict["Name_Title"] = {"loc": [loc], "text": text}
                return True, verbose_dict, None
            for name_title in NAME_TITLES:
                if text.strip().startswith(name_title):
                    loc = {key: round(loc[key]) for key in loc}
                    verbose_dict["Name_Title"] = {"loc": [loc], "text": text}
                    return True, verbose_dict, text.strip().removeprefix(name_title).lstrip()
        if text.strip() in NAME_TITLES:
            print()
            print_warning(f"Name information does not seem to be at the correct place "
                          f"for page {Color.beige}{num_page}{Color.reset}.")
    return False, verbose_dict, None


def _does_pos_correspond(loc: dict[str, float], loc_ref: dict[str, float]):
    x_ref = loc_ref["x"]
    y_ref = loc_ref["y"]
    x_tol = loc_ref.get("x_tol", 20)
    y_tol = loc_ref.get("y_tol", 20)

    x = loc["x"]
    y = loc["y"]

    if abs(x - x_ref) <= x_tol and abs(y - y_ref) <= y_tol:
        return True
    return False


def _check_correct_res_dict(res_dict, num_page: int, list_info):
    if any(text == "" for text in res_dict.values()):
        print()
        print_error(f"Not all information has been parsed from the pdf "
                    f"for page {Color.beige}{num_page}{Color.reset}:")
        print(f"{Color.orange}Missing info is {Color.light_blue}"
              f"{', '.join([key for key, text in res_dict.items() if text == ''])}{Color.orange}."
              f"{Color.reset}\n")
        for key, val in res_dict.items():
            print(f"\t- {key}: {Color.yellow}{val}{Color.reset}")
        print(f"\nThe pdf information is the following:")
        for i, info in enumerate(list_info):
            info = {key: {sub_key: round(val[sub_key]) for sub_key in val} if key == "loc" else val
                    for key, val in info.items()}
            color = Color.light_blue if i % 2 == 0 else Color.pale_green
            print("{" + ", ".join([f"{key}: {color if key in ['text', 'loc'] else ''}{val}{Color.reset}"
                                   for key, val in info.items()]) + "}")
        print("\n")
