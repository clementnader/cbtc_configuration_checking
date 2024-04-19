#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..database_location import *
from ..dc_sys import *
from ..foundation_data_constraints.check_offset import *
from .survey_verification import *
from .load_survey import *
from .block_definition import *

__all__ = ["check_survey"]


SURVEY_CHECKING_VERSION = "v2.2.2"


def check_survey():
    check_offset_correctness()

    print_title(f"Correspondence with Site Survey for "
                f"{Color.cyan}{get_c_d470_version()}{Color.reset}")

    if DATABASE_LOC.block_def is not None:
        print_section_title(f"Loading Block Def. information...")
    block_def_dict = get_block_definition()
    print_section_title(f"Loading Survey information...")
    survey_info = load_survey()

    print_section_title(f"Analyzing the Survey information and comparing them to the DC_SYS...")
    survey_verif_dict = create_check_survey_dict(survey_info, block_def_dict)

    print_section_title(f"Creating the Result File...")
    res_file_path = create_survey_verif_file(survey_verif_dict, block_def_dict is not None, SURVEY_CHECKING_VERSION)
    open_excel_file(res_file_path)

    if get_ga_version() < (6, 0, 0, 0):
        print_warning(f"GA version is before v6:"
                      f"\nVerify that the objects to verify in Correspondence with Site Survey activity "
                      f"asked by the System DPSA effectively correspond to sheet \"Survey\" of the result file.")

    return True
