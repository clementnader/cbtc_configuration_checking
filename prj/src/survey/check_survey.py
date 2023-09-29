#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from .check_d932 import *
from .load_d932 import *


__all__ = ["check_survey"]


def check_survey():
    survey_info = load_survey()
    survey_verif_dict = create_check_survey_dict(survey_info)
    res_file_path = create_survey_verif_file(survey_verif_dict)
    open_excel_file(res_file_path)
