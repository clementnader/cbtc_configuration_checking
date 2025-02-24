#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..control_tables_utils import *
from ..ini_file import *


__all__ = ["analyze_pdf_info"]


def analyze_pdf_info(table_type: str, num_page: int, pos_dict: dict[tuple[float, float], str],
                     max_pos: tuple[float, float],
                     debug: bool = False) -> Optional[dict[str, dict[str, str]]]:
    # titles_info = ROUTE_INFORMATION if table_type == CONTROL_TABLE_TYPE.route else OVERLAP_INFORMATION
    route_information, overlap_information = get_control_tables_template_info()
    titles_info = route_information if table_type == CONTROL_TABLE_TYPE.route else overlap_information
    title_pos_dict, pos_dict = _get_title_positions(titles_info, num_page, pos_dict)
    if title_pos_dict is None:
        return None
    if debug:
        print("title_pos_dict:")
        pretty_print_dict(title_pos_dict)
        print_bar()
        print("pos_dict:")
        pretty_print_dict(pos_dict)
        print_bar()

    page_dict = dict()
    for title, title_value in title_pos_dict.items():
        key_name = title_value["key_name"]
        title_pos = title_value["pos"]
        csv_title = title_value["csv_title"]
        corresponding_title_info = titles_info[title]
        right = corresponding_title_info.get("right", False)
        if right:
            info = _get_corresponding_info_at_right(num_page, key_name, title_pos, max_pos, pos_dict)
        else:
            info = _get_corresponding_info_bottom(num_page, key_name, title_pos, max_pos, pos_dict)

        if not _check_complete_expression(info):
            print_warning(f"Expression \"{info}\" is not complete for key {key_name} on page {num_page}.")
        page_dict[title] = {"key_name": key_name, "info": info, "csv_title": csv_title}

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
    neg_tol_x = 350. * (max_pos[0] / 1000.)
    neg_tol_y = 120. * (max_pos[1] / 1000.)
    pos_tol_x = 5. * (max_pos[0] / 1000.)

    info_bottom_dict = [((x, y), text) for (x, y), text in pos_dict.items()
                        if (title_x - neg_tol_x) < x < (title_x + pos_tol_x) and (title_y - neg_tol_y) < y < title_y]
    # y-axis origin is at the bottom of the page
    if not info_bottom_dict:
        print_error(f"Unable to find corresponding info for key {key_name} on page {num_page}.")
        return None

    def _sort_function(x: float, y: float) -> float:
        delta_x = abs((x-title_x))
        delta_y = abs((y-title_y))
        return 5*delta_y + delta_x  # setting more weight to delta y,
        # for similar delta y, the delta x will be considered to get the corresponding info

    info_bottom_dict.sort(key=lambda a: _sort_function(a[0][0], a[0][1]))
    return info_bottom_dict[0][1]


def _check_complete_expression(expression: str) -> bool:
    if expression is None:
        return False
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


def _get_title_positions(titles_info, num_page: int, pos_dict: dict[tuple[float, float], str],
                         ) -> tuple[Optional[dict[str, dict[str, Union[str, tuple[float, float]]]]],
                                    dict[tuple[float, float], str]]:
    title_pos_dict = {key: dict() for key in titles_info}
    keys_to_del = list()  # we remove the key titles from the dictionary
    for pos, text in pos_dict.items():
        for title, info in titles_info.items():
            if info["name"] in text:
                title_pos_dict[title] = {"key_name": text, "pos": pos, "csv_title": info["csv_name"]}
                keys_to_del.append(pos)

    if all(not title_pos_dict[title] for title in titles_info if title != "name"):  # only "name" title appears
        # word "Name" can appear on a page without being a Control Table page
        return None, pos_dict
    if not title_pos_dict["name"]:
        # "Name" is missing
        return None, pos_dict

    missing_titles_names = [titles_info[title]["name"] for title in titles_info if not title_pos_dict[title]]
    if missing_titles_names:  # titles are missing
        print_error(f"Tool was not able to analyze the whole page {num_page}: some information is missing:")
        print(missing_titles_names)
        return None, pos_dict

    for key in keys_to_del:
        del pos_dict[key]
    return title_pos_dict, pos_dict
