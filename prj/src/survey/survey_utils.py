#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ..utils import *


__all__ = ["check_polarity", "clean_track_name"]


def check_polarity(dc_sys_kp: Optional[float], surveyed_kp: Optional[float]) -> bool:
    if dc_sys_kp is None or surveyed_kp is None:
        return False
    if abs(dc_sys_kp - surveyed_kp) <= .006 or abs(dc_sys_kp - surveyed_kp) <= abs(abs(dc_sys_kp) - abs(surveyed_kp)):
        return False
    return True


def clean_track_name(original_track: str, set_to_test: set[str]):
    test_track_name = original_track.upper()
    if test_track_name in set_to_test:
        return test_track_name

    test_track_name = re.sub(r" +", r"_", test_track_name)
    test_track_name = re.sub(r"_+", r"_", test_track_name)
    if test_track_name in set_to_test:
        return test_track_name

    test_track_name_extra_underscore = re.sub(r"([A-Z])([0-9])", r"\1_\2", test_track_name)
    if test_track_name_extra_underscore in set_to_test:
        return test_track_name_extra_underscore

    if re.search(r"^TRACK_[0-9]+$", test_track_name) is not None:
        track_number = test_track_name.removeprefix("TRACK_")
        if f"T{track_number}" in set_to_test:
            return f"T{track_number}"
        if f"T{track_number.removeprefix('0')}" in set_to_test:
            return f"T{track_number.removeprefix('0')}"
        if f"TRACK{track_number}" in set_to_test:
            return f"TRACK{track_number}"
        if f"TRACK{track_number.removeprefix('0')}" in set_to_test:
            return f"TRACK{track_number.removeprefix('0')}"
        if f"TRACK_{track_number.removeprefix('0')}" in set_to_test:
            return f"TRACK_{track_number.removeprefix('0')}"

    if re.search(r"[0-9]+[A-Z]$", test_track_name) is not None:
        test_track_without_letter = test_track_name[:-1]  # without the last letter
        if test_track_without_letter in set_to_test:
            return test_track_without_letter

    if re.search(r"[0-9]+_[0-9]$", test_track_name) is not None:
        test_track_without_last_number = test_track_name[:-2]  # without the last number and the underscore
        if test_track_without_last_number in set_to_test:
            return test_track_without_last_number

    # if re.search(r"[0-9][0-9]+[0-9]$", test_track_name) is not None:
    #     test_track_without_last_number = test_track_name[:-1]  # without the last number
    #     if test_track_without_last_number in set_to_test:
    #         return test_track_without_last_number

    return original_track.upper()
