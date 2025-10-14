#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


__all__ = ["DC_TU_FILE", "TRAIN_UNIT_ID",
           "CC_ID_REGEX_PATTERN", "CC_PMC_ALPHA_ADDRESS_REGEX_PATTERN", "CC_PMC_BETA_ADDRESS_REGEX_PATTERN",
           "CC_PMC_SSH_PUBLIC_KEY_REGEX_PATTERN",
           "get_num_cc_parameter_name", "get_num_pmc_parameter_name"]


DC_TU_FILE = "DC_TU.csv"

TRAIN_UNIT_ID = "TRAIN_UNIT_ID"

CC_ID_REGEX_PATTERN = re.compile(r"^CC[12]_ID$")
CC_PMC_ALPHA_ADDRESS_REGEX_PATTERN = re.compile(r"^CC[12]_PMC[1-3]_ALPHA_IP_ADDRESS$")
CC_PMC_BETA_ADDRESS_REGEX_PATTERN = re.compile(r"^CC[12]_PMC[1-3]_BETA_IP_ADDRESS$")
CC_PMC_SSH_PUBLIC_KEY_REGEX_PATTERN = re.compile(r"^CC[12]_PMC[1-3]_SSH_RSA_PUBLIC_KEY$")


def get_num_cc_parameter_name(parameter_name: str) -> int:
    cc_name = parameter_name.split("_", 1)[0]
    num_cc = int(cc_name.removeprefix("CC"))
    return num_cc


def get_num_pmc_parameter_name(parameter_name: str) -> int:
    pmc_name = parameter_name.split("_", 2)[1]
    num_pmc = int(pmc_name.removeprefix("PMC"))
    return num_pmc
