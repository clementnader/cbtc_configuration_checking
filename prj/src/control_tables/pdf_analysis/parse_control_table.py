#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..control_tables_utils import *


__all__ = ["analyze_pdf_info"]


def analyze_pdf_info(table_type: str, num_page: int, pos_dict: dict[tuple[float, float], str],
                     max_pos: tuple[float, float]) -> Optional[dict[str, dict[str, str]]]:
    titles_info = ROUTE_INFORMATION if table_type == CONTROL_TABLE_TYPE.route else OVERLAP_INFORMATION
    title_pos_dict, pos_dict = _get_title_positions(table_type, num_page, pos_dict)
    if title_pos_dict is None:
        return None

    page_dict = dict()
    for title, title_value in title_pos_dict.items():
        key_name = title_value["key_name"]
        title_pos = title_value["pos"]
        corresponding_title_info = titles_info[title]
        right = corresponding_title_info.get("right", False)
        if right:
            info = _get_corresponding_info_at_right(num_page, key_name, title_pos, max_pos, pos_dict)
        else:
            info = _get_corresponding_info_bottom(num_page, key_name, title_pos, max_pos, pos_dict)

        if not _check_complete_expression(info):
            print_warning(f"Expression \"{info}\" is not complete for key {key_name} on page {num_page}.")
        page_dict[title] = {"key_name": key_name, "info": info}

    return page_dict


def _get_corresponding_info_at_right(num_page: int, key_name: str, title_pos: tuple[float, float],
                                     max_pos: tuple[float, float], pos_dict: dict[tuple[float, float], str]
                                     ) -> Optional[str]:
    title_x, title_y = title_pos
    tol_y = 20. * (max_pos[1] / 1000.)
    info_at_right_dict = [((x, y), text) for (x, y), text in pos_dict.items()
                          if abs(title_y - y) < tol_y and x > title_x]
    if not info_at_right_dict:
        print_error(f"Unable to find corresponding info for key {key_name} on page {num_page}.")
        return None

    info_at_right_dict.sort(key=lambda a: a[0][0])  # looking for the smallest x
    return info_at_right_dict[0][1]


def _get_corresponding_info_bottom(num_page: int, key_name: str, title_pos: tuple[float, float],
                                   max_pos: tuple[float, float], pos_dict: dict[tuple[float, float], str]
                                   ) -> Optional[str]:
    title_x, title_y = title_pos
    tol_neg_x = - 120. * (max_pos[1] / 1000.)
    tol_pos_x = 5. * (max_pos[1] / 1000.)
    info_bottom_dict = [((x, y), text) for (x, y), text in pos_dict.items()
                        if tol_neg_x < (x - title_x) < tol_pos_x and y < title_y]  # y-axis origin is at the bottom of the page
    if not info_bottom_dict:
        print_error(f"Unable to find corresponding info for key {key_name} on page {num_page}.")
        return None

    info_bottom_dict.sort(key=lambda a: -a[0][1])  # looking for the biggest y
    return info_bottom_dict[0][1]


def _check_complete_expression(expression: str) -> bool:
    expression = expression.strip()
    if expression.count("\"") % 2 == 1:
        return False
    if expression.count("(") != expression.count(")"):
        return False
    if not expression.endswith("--") and expression.endswith("-"):
        return False
    if expression.endswith(",") or expression.endswith("_") or expression.endswith("."):
        return False
    return True


def _get_title_positions(table_type: str, num_page: int, pos_dict: dict[tuple[float, float], str]
                         ) -> tuple[Optional[dict[str, dict[str, Union[str, tuple[float, float]]]]],
                                    dict[tuple[float, float], str]]:
    titles_info = ROUTE_INFORMATION if table_type == CONTROL_TABLE_TYPE.route else OVERLAP_INFORMATION
    title_pos_dict = dict()
    keys_to_del = list()
    for pos, text in pos_dict.items():
        for title, info in titles_info.items():
            possible_names = info["names"]
            if any(possible_name in text for possible_name in possible_names):
                title_pos_dict[title] = {"key_name": text, "pos": pos}
                keys_to_del.append(pos)

    if all(title not in title_pos_dict for title in titles_info
           if titles_info[title].get("optional", False) is False and title != "name"):  # only "name" title appears
        # word "Name" can appear on a page without being a Control Table page
        return None, pos_dict
    if "name" not in title_pos_dict:
        # "Name" is missing
        return None, pos_dict

    missing_titles_names = [titles_info[title]["names"] for title in titles_info
                            if title not in title_pos_dict and titles_info[title].get("optional", False) is False]
    if missing_titles_names:  # non-optional titles are missing
        print_error(f"Tool was not able to analyze the whole page {num_page}: some information is missing:")
        print(missing_titles_names)
        return None, pos_dict

    for key in keys_to_del:
        del pos_dict[key]
    return _sort_title_pos_dict(title_pos_dict), pos_dict


def _sort_title_pos_dict(title_pos_dict: dict[str, Any]):
    def convert_alnum_for_sort(alpha_numeric: str) -> tuple[int, str]:  # it has to work with 1a and 1b also
        i = 0
        while i < len(alpha_numeric):
            c = alpha_numeric[i]
            if not c.isnumeric():
                break
            i += 1
        if i == 0:
            return 100_000, alpha_numeric
        return int(alpha_numeric[:i]), alpha_numeric[i:]

    def split_key(key):
        key_name = title_pos_dict[key]["key_name"]
        if "[" not in key_name:  # there is no "[" only for Name key name, which has to appear first
            return -1, ""
        return convert_alnum_for_sort(key_name.split("[", 1)[1].split("]", 1)[0])

    return {key: title_pos_dict[key] for key in sorted(title_pos_dict, key=split_key)}
