#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .create_check_survey_dict import *
from .create_survey_verif_file import *


__all__ = ["check_survey"]


def check_survey():
    survey_verif_dict = create_check_survey_dict()
    res_file_path = create_survey_verif_file(survey_verif_dict)
    open_excel_file(res_file_path)
