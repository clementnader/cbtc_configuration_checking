#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..d932_utils import *


__all__ = ["create_check_survey_dict"]


def create_check_survey_dict(survey_info):
    survey_verif_dict = dict()
    for survey_type, survey_type_value in SURVEY_TYPES_DICT.items():
        res_sheet = survey_type_value["res_sheet"]
        dcsys_sh = survey_type_value["dcsys_sh"]
        func = survey_type_value["func"]
        survey_verif_dict[res_sheet] = _order_survey_verif_dict(func(dcsys_sh, res_sheet, survey_info.get(survey_type)))
    return survey_verif_dict


def _order_survey_verif_dict(verif_dict: dict):
    """ Order by track then KP """
    verif_dict = {key: verif_dict[key] for key in sorted(verif_dict.keys(),
                  key=lambda x: (_get_track_to_order_dict(x, verif_dict), _get_kp_to_order_dict(x, verif_dict)))}
    return verif_dict


def _get_track_to_order_dict(x, verif_dict):
    """ Get track name inside the verif dict dictionary, according to which one exists. """
    return verif_dict[x]["track"].lower() if verif_dict[x]["track"] is not None \
        else verif_dict[x]["survey_track"].lower()


def _get_kp_to_order_dict(x, verif_dict):
    """ Get KP value inside the verif dict dictionary, with the different KP values according to which one exists.
        If none, put a dummy large value, for the object to be at the end of the order. """
    return verif_dict[x]["dc_sys_kp"] if verif_dict[x]["dc_sys_kp"] is not None \
        else verif_dict[x]["surveyed_kp"] if verif_dict[x]["surveyed_kp"] is not None \
        else 1E20
