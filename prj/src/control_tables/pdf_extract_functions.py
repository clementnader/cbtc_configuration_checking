#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ..utils import *
from .control_table_info_route import *
from .control_table_info_overlap import *


__all__ = ["CONTROL_TABLE_TYPE", "parse_pdf_control_table"]


class CONTROL_TABLE_TYPE:
    route = "route"
    overlap = "overlap"


def parse_pdf_control_table(text: str, num_page: int, table_type: str) -> Optional[dict[str, dict[str, str]]]:
    if table_type == CONTROL_TABLE_TYPE.route:
        control_table_info = ROUTE_INFORMATION
    elif table_type == CONTROL_TABLE_TYPE.overlap:
        control_table_info = OVERLAP_INFORMATION
    else:
        print_error(f"Control Table type {table_type} is not known.")
        return {}

    max_len = max(len(line) for line in text.splitlines())
    pos_dict = dict()
    for key in control_table_info:
        num_line, abscissa = _get_key_position(text, num_page, key, control_table_info)
        if (num_line is not False and
                (num_line, abscissa) in [(pos_info["num_line"], pos_info["abscissa"])
                                         for pos_info in pos_dict.values()]):
            num_line, abscissa = False, -1
        pos_dict[key] = {"num_line": num_line, "abscissa": abscissa}
    if all(pos_dict[key]["num_line"] is False for key in control_table_info if key != "name"):
        # word "Name" can appear on a page without being a Control Table page
        return None
    if pos_dict["name"]["num_line"] is False:
        # "Name" is missing
        return None
    missing_keys = [key for key in control_table_info if pos_dict[key]["num_line"] is False
                    and control_table_info[key].get("optional", False) is False]  # if a non-optional key is missing
    if missing_keys:
        print_warning(f"Missing key(s) on page {num_page}:\n"
                      f"{[control_table_info[key]['names'][0].split()[0] for key in missing_keys]}. "
                      f"Page is not analyzed.")
        return None

    res_dict = dict()
    for key in control_table_info:
        if pos_dict[key]["num_line"] is False:
            continue
        expression, corresponding_key_name = _get_info_for_key(text, num_page, key, control_table_info,
                                                               pos_dict[key]["num_line"], pos_dict[key]["abscissa"],
                                                               max_len)
        res_dict[key] = {"key_name": corresponding_key_name, "info": expression}

    return _sort_control_table_dict(res_dict)


def _sort_control_table_dict(in_dict: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    def convert_alnum_for_sort(alpha_numeric: str) -> tuple[int, str]:
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
        key_name = in_dict[key]["key_name"]
        if "[" not in key_name:
            return -1, ""
        return convert_alnum_for_sort(key_name.split("[", 1)[1].split("]", 1)[0])

    return {key: in_dict[key] for key in sorted(in_dict.keys(), key=split_key)}


def _get_key_position(text: str, num_page: int, key: str, control_table_info: dict[str, dict[str, Any]]
                      ) -> tuple[Union[bool, int], int]:
    possible_key_names = control_table_info[key]["names"]
    possible_prefixes = [name.split()[0] for name in possible_key_names]  # [X]
    lines = [(num_line, line) for num_line, line in enumerate(text.splitlines())
             if any(prefix in line for prefix in possible_prefixes)]
    if not lines:
        return False, -1
    if len(lines) > 2:
        print_error(f"Multiple lines containing the prefix of the attribute {key} ({possible_prefixes}) "
                    f"in page {num_page}:")
        print(lines)
    num_line, line = lines[0]
    abscissa = [line.find(prefix) for prefix in possible_prefixes if prefix in line][0]
    return num_line, abscissa


def _get_info_for_key(text: str, num_page: int, key: str, control_table_info: dict[str, dict[str, Any]],
                      num_line: int, abscissa: int, max_len: int):
    possible_key_names = control_table_info[key]["names"]
    possible_key_names = sorted(possible_key_names, key=lambda x: len(x), reverse=True)  # sort by largest string
    right = control_table_info[key].get("right", False)
    next_line = control_table_info[key].get("next_line", False)
    first = control_table_info[key].get("first", False)
    multiple_lines = control_table_info[key].get("multiple_lines", False)
    negative_tol = int(control_table_info[key].get("negative_tol", 25)*max_len/550)
    info_format = control_table_info[key].get("info_format")
    if right:
        line = text.splitlines()[num_line][abscissa:]
        for key_name in possible_key_names:
            if line.startswith(key_name):
                corresponding_key_name = key_name
                expression, _ = _get_expression(line.removeprefix(key_name).lstrip(), max_len)
                if expression is None:
                    continue
                if info_format is None or re.search(info_format, expression) is not None:
                    # print_section_title(corresponding_key_name)
                    # print(expression)
                    return expression, corresponding_key_name
    if next_line:
        corresponding_key_name, num_line = _get_key_name_multiple_lines(text, max_len, num_line, abscissa,
                                                                        possible_key_names, negative_tol)
        # print_section_title(corresponding_key_name)
        num_line += 1
        expression, new_abscissa, num_line = _get_next_expression(text, max_len, num_line, abscissa, negative_tol,
                                                                  first, only_one_line=False)
        if not expression:
            print_error(f"1.{corresponding_key_name=}\t{num_page=}\t{expression=}")
        while (not (expression[0].isnumeric() or expression[0].isupper() or expression[0] == "," or expression == "--"
                    or (expression[0] == "[" and re.match(r"^\[[1-9a-z]{1,2}]", expression) is None))):
            num_line += 1
            expression, new_abscissa, num_line = _get_next_expression(text, max_len, num_line, abscissa, negative_tol,
                                                                      first, only_one_line=False)
            if not expression:
                print_error(f"2.{corresponding_key_name=}\t{num_page=}\t{expression=}")
        # print("\t", expression)
        if not multiple_lines and info_format is not None:
            while re.search(info_format, expression) is None:
                num_line += 1
                expression, _, num_line = _get_next_expression(text, max_len, num_line, abscissa, negative_tol,
                                                               first, only_one_line=False)

        if multiple_lines and expression != "--":
            test, test_num_line = _test_next_line(text, num_line, new_abscissa)
            while test:
                next_expression, _, test_num_line = _get_next_expression(text, max_len, test_num_line, new_abscissa,
                                                                         negative_tol=0, only_one_line=True)
                expression += " " + next_expression
                test, test_num_line = _test_next_line(text, test_num_line, new_abscissa)
            if not _check_complete_expression(expression):
                print_warning(f"Expression \"{expression}\" is not complete (on page {num_page}, "
                              f"for key {corresponding_key_name}).")
        # print(expression)
        return expression, corresponding_key_name


def _get_key_name_multiple_lines(text: str, max_len: int, num_line: int, abscissa: int, possible_key_names: list[str],
                                 negative_tol: int, first_line: bool = True, split_index: int = 0) -> tuple[str, int]:

    if first_line:
        line = text.splitlines()[num_line][abscissa:]
    else:
        prefix = " ".join(possible_key_names[0].split()[:split_index])
        expression, _, num_line = _get_next_expression(text, max_len, num_line, abscissa, negative_tol,
                                                       positive_tol=60, only_one_line=False)
        if expression is None:
            print_error(f"{prefix=}")

        line = prefix + " " + expression

    line = re.sub(r"\s{2,5}", r" ", line)
    line = _remove_spaces(line)

    for key_name in possible_key_names:
        if line.startswith(_remove_spaces(key_name)):
            return key_name, num_line

    while any(line.startswith(_remove_spaces(" ".join(key_name.split()[:split_index])))
              for key_name in possible_key_names):
        for key_name in possible_key_names[:]:
            if not line.startswith(_remove_spaces(" ".join(key_name.split()[:split_index]))):
                possible_key_names.pop()
        split_index += 1
    return _get_key_name_multiple_lines(text, max_len, num_line+1, abscissa, possible_key_names, negative_tol,
                                        first_line=False, split_index=split_index-1)


def _remove_spaces(line: str) -> str:
    pattern = re.compile(r"([A-Za-z]+)\s([A-Za-z]+)")
    while re.search(pattern, line) is not None:
        line = re.sub(pattern, r"\1\2", line)
    return line


def _get_next_expression(text: str, max_len: int, num_line: int, abscissa: int, negative_tol: int, first: bool = False,
                         positive_tol: int = 40,
                         only_one_line: bool = True) -> tuple[Optional[str], Optional[int], int]:
    expression, new_abscissa = _get_expression(text.splitlines()[num_line], max_len, abscissa, negative_tol, first)
    if not only_one_line:
        while expression is None:
            num_line += 1
            if num_line >= len(text.splitlines()):
                return None, None, num_line
            expression, new_abscissa = _get_expression(text.splitlines()[num_line], max_len, abscissa, negative_tol,
                                                       first, positive_tol)
    return expression, new_abscissa, num_line


def _get_expression(line: str, max_len: int, abscissa: int = 0, negative_tol: int = 0, first: bool = False,
                    positive_tol: int = 50) -> tuple[Optional[str], Optional[int]]:
    max_nb_spaces = int(12*max_len/550)
    positive_tol = int(positive_tol*max_len/550)
    start = 0 if first or abscissa - negative_tol < 0 else abscissa-negative_tol
    started = False
    expression = None
    first_column = None
    cnt_spaces = 0
    for column, character in enumerate(line[start:], start=start):
        if not started:
            if character == " ":
                if column < abscissa + positive_tol:
                    continue
                return None, None
            started = True
            expression = character
            first_column = column
        else:
            expression += character
            # print(expression)
            if character == " ":
                if expression[-2] == " ":
                    cnt_spaces += 1
                else:
                    cnt_spaces = 1
                if cnt_spaces > max_nb_spaces:
                    break
    if expression is None:
        return None, None
    # print_success(expression)
    return expression.rstrip(), first_column


def _test_next_line(text: str, num_line: int, abscissa: int, current_cnt: int = 0) -> tuple[bool, int]:
    limit = 3
    if current_cnt >= limit:
        return False, num_line
    if num_line+1 >= len(text.splitlines()):
        return False, num_line
    if abscissa >= len(text.splitlines()[num_line+1]):  # next line is too short
        return _test_next_line(text, num_line+1, abscissa, current_cnt+1)

    min_char = abscissa-10 if abscissa > 10 else 0
    previous_characters = text.splitlines()[num_line+1][min_char:abscissa-1] if abscissa > 0 else " "
    current_characters = text.splitlines()[num_line+1][abscissa:abscissa+3]
    if (all(previous_character == " " for previous_character in previous_characters)
            and any(current_character != " " for current_character in current_characters)):  # start of a word
        return True, num_line+1
    if (all(previous_character == " " for previous_character in previous_characters)
            and any(current_character == " " for current_character in current_characters)):  # blank space
        return _test_next_line(text, num_line+1, abscissa, current_cnt+1)  # try next line
    return False, num_line


def _check_complete_expression(expression: str) -> bool:
    if expression.count("\"") % 2 == 1:
        return False
    if expression.count("(") != expression.count(")"):
        return False
    if not expression.endswith("--") and expression.endswith("-"):
        return False
    if expression.endswith(","):
        return False
    return True
