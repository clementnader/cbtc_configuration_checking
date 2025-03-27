#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..database_location import *
from ..dc_sys import *
from ..foundation_data_constraints.check_offset import *
from .survey_verification import *
from .load_survey import *
from .block_definition import *
from .result_file import *

__all__ = ["check_survey", "SURVEY_CHECKING_VERSION"]


SURVEY_CHECKING_VERSION = "v2.8.1"


def check_survey():
    check_dc_sys_track_kp_definition()

    print_title(f"Correspondence with Site Survey for "
                f"{Color.cyan}{get_current_version()}{Color.reset}")

    if DATABASE_LOC.block_def is not None:
        print_section_title(f"Loading Block Def. information...")
        block_def_dict, block_definition_display_info = get_block_definition()
        print_bar(start="\n")
    else:
        block_def_dict = None
        block_definition_display_info = None
    print_section_title(f"Loading Survey information...")
    survey_info, survey_display_info_list = load_survey()
    print_bar(start="\n")

    print_section_title(f"Analyzing the Survey information and comparing them to the DC_SYS...")
    survey_verif_dict = create_verif_survey_dict(survey_info, block_def_dict)
    print_bar(start="\n")

    print_section_title(f"Creating the Result File...")
    res_file_path = create_survey_verif_file(survey_verif_dict, block_def_dict is not None, SURVEY_CHECKING_VERSION,
                                             survey_display_info_list, block_definition_display_info)
    open_excel_file(res_file_path)

    if get_ga_version() < (6, 5, 5, 0):
        print_bar(start="\n")
        print_warning(f"GA version is before v6.5.5:"
                      f"\nVerify that the objects to verify in Correspondence with Site Survey activity "
                      f"asked by the System DPSA effectively correspond to sheet \"FD - Site Survey\" "
                      f"of the result file.")

    return True
