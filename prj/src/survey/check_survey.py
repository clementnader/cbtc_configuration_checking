#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from .survey_verification import *
from .load_survey import *


__all__ = ["check_survey"]


def check_survey():
    print_title(f"Correspondence with site survey for "
                f"{Color.cyan}{get_c_d470_version()}{Color.reset}.")
    print_section_title(f"Loading survey information...")
    survey_info = load_survey()
    print_section_title(f"Analyzing the survey information and comparing them to the DC_SYS...")
    survey_verif_dict = create_check_survey_dict(survey_info)
    print_section_title(f"Creating the result file...")
    res_file_path = create_survey_verif_file(survey_verif_dict)
    open_excel_file(res_file_path)
