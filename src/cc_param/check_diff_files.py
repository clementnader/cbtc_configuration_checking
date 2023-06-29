#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *
from .cc_param_utils import *
from .html_style_diff_file import additional_css_style

# MAIN_DIRECTORY = r"C:\Users\naderc\Desktop\Ankara\ANK_L2_C11_D470_06_05_03_V06\ANK_L2_C11_D470_06_05_03_V06"
MAIN_DIRECTORY = r"C:\Users\naderc\Desktop\ML4_TF3_C11_D470_06_05_05_V03\ML4_TF3_C11_D470_06_05_05_V03"
RESULT_FOLDER = r"C:\Users\naderc\Desktop"

# From DC_SYS > Train
# TYPES_OF_TRAIN = ["BOMB", "ZELC"]
# LIST_TRAIN_NUM_LIMITS = [f"{1}-{36}",  # first type of train is between 1 and 36
#                          f"{37}-{144}"]  # second type of train is between 37 and 144
# NB_CABS_OF_TYPES = [1, 1]  # TODO
TYPES_OF_TRAIN = ["ML"]
LIST_TRAIN_NUM_LIMITS = [f"{401}-{447}"]  # first type of train is between 1 and 36
NB_CABS_OF_TYPES = [1]  # TODO


def get_train_unit_files() -> dict[int, dict[str, str]]:
    dict_train_units = dict()
    for train_dir in os.listdir(MAIN_DIRECTORY):
        full_path = os.path.join(MAIN_DIRECTORY, train_dir)
        if os.path.isdir(full_path) and train_dir.startswith(TRAIN_UNIT_PREFIX):
            train_num = get_num_train(train_dir)
            type_of_train = get_type_of_train(train_num, TYPES_OF_TRAIN, LIST_TRAIN_NUM_LIMITS)
            if type_of_train is not None:
                dict_train_units[train_num] = {"type": type_of_train, "main_dir": train_dir}
            else:
                print(f"{train_num = } is not identified as a possible train number in {LIST_TRAIN_NUM_LIMITS = }.")
    return sort_dict(dict_train_units)


def get_cc_param():
    dict_train_units = get_train_unit_files()
    for train_num, train_values in dict_train_units.items():
        train_dir = train_values["main_dir"]
        list_cab_dir = list()
        for cab_dir in os.listdir(os.path.join(MAIN_DIRECTORY, train_dir)):
            cab_full_path = os.path.join(MAIN_DIRECTORY, train_dir, cab_dir)
            if os.path.isdir(cab_full_path) and cab_dir.startswith(CAB_DIR_PREFIX):
                list_cab_dir.append(cab_dir)
        if not list_cab_dir:
            print_warning(f"No Cab in {os.path.join(MAIN_DIRECTORY, train_dir)}.")
        else:
            if len(list_cab_dir) != 1:  # TODO take multiple cabs into account
                print_warning(f"Multiple Cabs in {os.path.join(MAIN_DIRECTORY, train_dir)}:"
                              f"\n\t{list_cab_dir = }.")
            dict_train_units[train_num]["file_path"] = get_cc_param_from_cabdir(train_dir, list_cab_dir[0])
    return dict_train_units


def get_cc_param_from_cabdir(train_dir, cab_dir):
    list_cc_param = list()
    cab_full_path = os.path.join(MAIN_DIRECTORY, train_dir, cab_dir)
    for cc_param_dir in os.listdir(cab_full_path):
        cc_param_full_path = os.path.join(cab_full_path, cc_param_dir)
        if os.path.isdir(cc_param_full_path) and cc_param_dir == CC_PARAM_DIR:
            for cc_param_file in os.listdir(cc_param_full_path):
                file_full_path = os.path.join(cc_param_full_path, cc_param_file)
                if os.path.isfile(file_full_path) and cc_param_file == CC_PARAM_FILE:
                    list_cc_param.append(os.path.join(cab_dir, cc_param_dir, cc_param_file))
    if not list_cc_param:
        print_warning(f"No {CC_PARAM_FILE} in {os.path.join(MAIN_DIRECTORY, train_dir)}")
    else:
        if len(list_cc_param) != 1:
            print_warning(f"Multiple {CC_PARAM_FILE} in {os.path.join(MAIN_DIRECTORY, train_dir)}")
        return list_cc_param[0]


def split_type_trains(dict_train_units):
    dict_split_type_trains = {train_type: dict() for train_type in TYPES_OF_TRAIN}
    for train_num, train_values in dict_train_units.items():
        train_type = train_values["type"]
        dict_split_type_trains[train_type][train_num] = train_values
    return dict_split_type_trains


def check_diff_cc_param():
    dict_split_type_trains = split_type_trains(get_cc_param())
    dict_diff_results = dict()
    for train_type, type_dict in dict_split_type_trains.items():
        ref_train_num = list(type_dict.keys())[0]
        ref_train_unit_dir = type_dict[ref_train_num]["main_dir"]
        ref_cc_param_path = type_dict[ref_train_num]["file_path"]
        ref_file = os.path.join(MAIN_DIRECTORY, ref_train_unit_dir, ref_cc_param_path)
        with open(os.path.join(ref_file), 'r') as ref_f:
            ref_lines = ref_f.readlines()
            titles = read_csv(ref_lines[0])
            dict_diff = dict()
            for train_values in type_dict.values():
                train_unit_dir = train_values["main_dir"]
                cc_param_path = train_values["file_path"]
                other_file = os.path.join(MAIN_DIRECTORY, train_unit_dir, cc_param_path)
                with open(os.path.join(MAIN_DIRECTORY, other_file), 'r') as f:
                    lines = f.readlines()
                    for i, (ref_line, line) in enumerate(zip(ref_lines, lines)):
                        ref_values = read_csv(ref_line)
                        ref_values[INFO_COLUMN] = ref_values[INFO_COLUMN].replace(",", ",<br />")
                        values = read_csv(line)
                        values[INFO_COLUMN] = values[INFO_COLUMN].replace(",", ",<br />")
                        if line != ref_line:
                            if values[VALUE_COLUMN] != ref_values[VALUE_COLUMN]:
                                if i not in dict_diff:
                                    dict_diff[i] = {title: ref_values[j] for j, title in enumerate(titles)
                                                    if j != VALUE_COLUMN}
                                    dict_diff[i][ref_train_unit_dir] = ref_values[VALUE_COLUMN]
                                dict_diff[i][train_unit_dir] = values[VALUE_COLUMN]
                            else:
                                print_warning(f"Difference on something else than the {titles[VALUE_COLUMN]}:"
                                              f"\n{line = }\n{ref_line = }")
        dict_diff_results[train_type] = dict_diff
    create_html_file(dict_diff_results)
    return dict_diff_results


def read_csv(line):
    return line.strip().split(";")


def html_display_info():
    multiple_types = len(TYPES_OF_TRAIN) > 1
    html_code = f"<p>"
    html_code += f"There are {len(TYPES_OF_TRAIN)} types of train units:" if multiple_types \
        else f"There is {len(TYPES_OF_TRAIN)} type of train units:"
    html_code += "<br />\n"
    html_code += ", ".join([f"{train_type} ({html_display_train_types_limits(limits)})"
                            for train_type, limits in zip(TYPES_OF_TRAIN, LIST_TRAIN_NUM_LIMITS)])
    html_code += "</p>\n"
    return html_code


def html_display_train_types_limits(train_limits: str):
    inf = int(train_limits.split("-")[0])
    sup = int(train_limits.split("-")[1])
    return f"between {inf} and {sup}"


def write_file(html_code):
    file_path = os.path.join(RESULT_FOLDER, "Results of Diff between CC parameters.html")
    with open(file_path, 'w') as f:
        f.write(html_code)


def create_html_file(dict_diff_results):
    html_code = html_start(title="CCparam_diff", additional_style=additional_css_style())
    html_code += html_h1("Differences between CC parameters")
    html_code += html_h2(f"within {MAIN_DIRECTORY.split(os.path.sep)[-1]}")
    html_code += html_display_info()
    for train_type, dict_diff in dict_diff_results.items():
        html_code += html_h2(train_type)
        html_code += html_result_table(dict_diff)
    html_code += html_end()
    write_file(html_code)


def html_result_table(dict_diff):
    html_code = "<div class=\"view\">\n"
    html_code += "\t<table class=\"diff-table\">\n"
    # Headline
    list_sub_keys = get_sub_keys(dict_diff)
    html_code += "\t\t<tr class=\"headline\">\n"
    for i, sub_key in enumerate(list_sub_keys):
        if i == RANK_COLUMN:
            # html_code += f"\t\t\t<th class=\"sticky first-col\">" \
            html_code += f"\t\t\t<th>" \
                         f"{sub_key}</th>\n"
        elif i == ID_COLUMN:
            # html_code += f"\t\t\t<th class=\"sticky second-col\">" \
            html_code += f"\t\t\t<th>" \
                         f"{sub_key}</th>\n"
        else:
            html_code += f"\t\t\t<th>{sub_key}</th>\n"
    html_code += "\t\t</tr>\n"
    # Main lines
    for line, values in dict_diff.items():
        if isinstance(line, int):
            html_code += "\t\t<tr>\n"
            for i, value in enumerate(values):
                if i == RANK_COLUMN:
                    # html_code += f"\t\t\t<th class=\"sticky first-col\">" \
                    html_code += f"\t\t\t<th>" \
                                 f"{values.get(value, '-')}</th>\n"
                elif i == ID_COLUMN:
                    # html_code += f"\t\t\t<th class=\"sticky second-col\">" \
                    html_code += f"\t\t\t<th>" \
                                 f"{values.get(value, '-')}</th>\n"
                else:
                    html_code += f"\t\t\t<td>{values.get(value, '-')}</td>\n"
            html_code += "\t\t</tr>\n"
    html_code += "\t</table>\n"
    html_code += "</div>\n"
    return html_code


def get_sub_keys(in_dict):
    list_sub_keys = list()
    for sub_dict in in_dict.values:
        if isinstance(sub_dict, dict):
            for sub_key in sub_dict:
                if sub_key not in list_sub_keys:
                    list_sub_keys.append(sub_key)
    return list_sub_keys
