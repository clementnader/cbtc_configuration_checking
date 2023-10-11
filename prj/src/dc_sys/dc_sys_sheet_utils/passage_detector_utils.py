#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


__all__ = ["get_passage_detectors_in_cbtc_ter"]


def get_passage_detectors_in_cbtc_ter():
    pass_det_dict = load_sheet(DCSYS.Passage_Detector)

    within_cbtc_pass_det_dict = dict()
    for pass_det_name, pass_det_value in pass_det_dict.items():
        seg = get_dc_sys_value(pass_det_value, DCSYS.Passage_Detector.Seg)
        x = float(get_dc_sys_value(pass_det_value, DCSYS.Passage_Detector.X))
        if is_point_in_cbtc_ter(seg, x) is not False:
            within_cbtc_pass_det_dict[pass_det_name] = pass_det_value
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Discrete Detector {pass_det_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
    return within_cbtc_pass_det_dict
