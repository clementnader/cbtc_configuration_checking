#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_basic_utils import *


__all__ = ["get_track_limits", "get_sorted_track_list", "split_track_to_order_them"]


def get_track_limits(track: str) -> tuple[float, float]:
    track_dict = load_sheet(DCSYS.Voie)
    start_kp = float(get_dc_sys_value(track_dict[track], DCSYS.Voie.PkDebut))
    end_kp = float(get_dc_sys_value(track_dict[track], DCSYS.Voie.PkFin))
    return start_kp, end_kp


def get_sorted_track_list() -> list[str]:
    track_dict = load_sheet(DCSYS.Voie)
    sorted_track_list = sorted(track_dict.keys(), key=lambda x: (split_track_to_order_them(x)))
    return sorted_track_list


def split_track_to_order_them(track: str) -> tuple[Union[str, int], ...]:
    """ Split track into a tuple to separate the numeric and the alphabetic words.
    For example, TRACK_2 and TRACK_11 would become ("TRACK_", 2) and ("TRACK_", 11),
     so that the TRACK_2 would be ordered before the 11. If doing a simple sort, the 11 is taken as a string
     and is ordered before the 2. """
    if all(not c.isnumeric() for c in track):  # no number if the track name
        return (track.lower(),)
    list_words = list()
    pos = 0
    char_type = "num" if track[pos].isnumeric() else "other"
    if char_type == "num":
        list_words.append("")
    current_word = track[pos]
    while pos < len(track) - 1:
        pos += 1
        new_char_type = "num" if track[pos].isnumeric() else "other"
        if new_char_type == char_type:
            current_word += track[pos]
        else:
            if char_type == "num":
                current_word = int(current_word)
            else:
                current_word = current_word.lower()
            list_words.append(current_word)
            current_word = track[pos]
        char_type = new_char_type
    if char_type == "num":
        current_word = int(current_word)
    else:
        current_word = current_word.lower()
    list_words.append(current_word)
    return tuple(list_words)
