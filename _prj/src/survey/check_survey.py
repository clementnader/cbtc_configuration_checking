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


SURVEY_CHECKING_VERSION = "v2.9.2"


def check_survey():
    check_dc_sys_track_kp_definition()

    print_title(f"Correspondence with Site Survey for "
                f"{Color.cyan}{get_current_version()}{Color.reset}")

    if DATABASE_LOCATION.block_def is not None:
        print_section_title(f"Loading Block Definition information...")
        block_def_dict, block_definition_display_info = get_block_definition()
        print_bar(start="\n")
    else:
        block_def_dict = None
        block_definition_display_info = None
    print_section_title(f"Loading Survey information...")
    survey_info, survey_display_info_list, missing_types = load_survey()
    print_bar(start="\n")

    print_section_title(f"Analyzing the Survey information and comparing them to the DC_SYS...")
    survey_verif_dict, middle_platforms_exist_bool = create_verif_survey_dict(survey_info, block_def_dict)
    print_bar(start="\n")

    print_section_title(f"Creating the Result File...")
    res_file_path = create_survey_verif_file(survey_verif_dict, block_def_dict is not None, middle_platforms_exist_bool,
                                             SURVEY_CHECKING_VERSION, survey_display_info_list,
                                             block_definition_display_info)
    open_excel_file(res_file_path)

    print_bar(start="\n")
    print_warning(f"Verify that the objects to verify in Correspondence with Site Survey activity "
                  f"asked by the System DPSA effectively correspond to sheet \"FD - Site Survey\" "
                  f"of the result file.")

    if missing_types:
        print_bar(start="\n")
        print(f"{Color.white}"
              f"As a reminder, the following type{'s' if len(missing_types) > 1 else ''} in the different surveys "
              f"{'are' if len(missing_types) > 1 else 'is'} not loaded by the tool: "
              f"{Color.yellow}{', '.join(missing_types)}{Color.reset}{Color.white}{Color.reset}.")

    if middle_platforms_exist_bool:
        print_bar(start="\n")
        print(f"{Color.white}Platform extremities are computed from Middle Platforms from survey. "
              f"{Color.yellow}You need to fill the \"Length of the platforms\" cell in the \"Platform\" sheet."
              f"{Color.reset}")

    return True
