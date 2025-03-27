#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .....utils import *
from ..dc_tu_utils import *


__all__ = ["get_number_of_cc", "get_ip_address_and_ssh_key"]


def get_number_of_cc(dc_tu_dict: dict[int, dict[int, dict[str, str]]]) -> int:
    number_of_cc = 0
    for line_number, sub_dict in dc_tu_dict.items():  # for each line
        for train_unit_number, sub_sub_dict in sub_dict.items():  # for each train unit
            for param_name in sub_sub_dict.keys():  # for each parameter
                if CC_ID_REGEX_PATTERN.search(param_name) is None:
                    continue
                num_cc = get_num_cc_param_name(param_name)
                if num_cc == 1:
                    if number_of_cc == 0:
                        number_of_cc = 1
                elif num_cc == 2:
                    number_of_cc = 2
                else:
                    print_error(f"CC number of {param_name} is not 1 or 2\n"
                                f"\tfor Train Unit {train_unit_number} and Line {line_number}.")
    if number_of_cc == 0:
        print_error(f"No {get_pattern(CC_ID_REGEX_PATTERN)} parameter has been found in {DC_TU_FILE} "
                    f"in any Train Unit.")
    return number_of_cc


def get_ip_address_and_ssh_key(dc_tu_dict: dict[int, dict[int, dict[str, str]]]) -> tuple[
            dict[int, dict[int, dict[int, dict[str, Union[str, list[tuple[int, str]]]]]]],
            dict[int, dict[int, dict[int, dict[str, Union[str, list[tuple[int, str]]]]]]]
        ]:
    ip_address_dict = dict()
    ssh_key_dict = dict()
    for line_number, sub_dict in dc_tu_dict.items():  # for each line
        ip_address_dict[line_number] = dict()
        ssh_key_dict[line_number] = dict()
        for train_unit_number, sub_sub_dict in sub_dict.items():  # for each train unit
            ip_address_dict[line_number][train_unit_number] = dict()
            ssh_key_dict[line_number][train_unit_number] = dict()
            for param_name, param_value in sub_sub_dict.items():  # for each parameter
                # CCx_IDx parameter, initialization of the 2 dictionaries
                if CC_ID_REGEX_PATTERN.search(param_name) is not None:
                    current_cc_num = get_num_cc_param_name(param_name)
                    ip_address_dict[line_number][train_unit_number][current_cc_num] = {
                        get_pattern(CC_ID_REGEX_PATTERN): param_value,
                        get_pattern(CC_PMC_ALPHA_ADDRESS_REGEX_PATTERN): list(),
                        get_pattern(CC_PMC_BETA_ADDRESS_REGEX_PATTERN): list(),
                    }
                    ssh_key_dict[line_number][train_unit_number][current_cc_num] = {
                        get_pattern(CC_ID_REGEX_PATTERN): param_value,
                        get_pattern(CC_PMC_SSH_PUBLIC_KEY_REGEX_PATTERN): list(),
                    }
                # CCx_PMCx_ALPHA_ADDRESS parameter
                elif CC_PMC_ALPHA_ADDRESS_REGEX_PATTERN.search(param_name) is not None:
                    current_cc_num = get_num_cc_param_name(param_name)
                    current_pmc_num = get_num_pmc_param_name(param_name)
                    ip_address_dict[line_number][train_unit_number][current_cc_num][
                        get_pattern(CC_PMC_ALPHA_ADDRESS_REGEX_PATTERN)
                    ].append((current_pmc_num, param_value))
                # CCx_PMCx_BETA_ADDRESS parameter
                elif CC_PMC_BETA_ADDRESS_REGEX_PATTERN.search(param_name) is not None:
                    current_cc_num = get_num_cc_param_name(param_name)
                    current_pmc_num = get_num_pmc_param_name(param_name)
                    ip_address_dict[line_number][train_unit_number][current_cc_num][
                        get_pattern(CC_PMC_BETA_ADDRESS_REGEX_PATTERN)
                    ].append((current_pmc_num, param_value))
                # CCx_PMCx_SSH_PUBLIC_KEY parameter
                elif CC_PMC_SSH_PUBLIC_KEY_REGEX_PATTERN.search(param_name) is not None:
                    current_cc_num = get_num_cc_param_name(param_name)
                    current_pmc_num = get_num_pmc_param_name(param_name)
                    ssh_key_dict[line_number][train_unit_number][current_cc_num][
                        get_pattern(CC_PMC_SSH_PUBLIC_KEY_REGEX_PATTERN)
                    ].append((current_pmc_num, param_value))

    return ip_address_dict, ssh_key_dict
