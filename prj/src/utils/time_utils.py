#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime


__all__ = ["time", "format_timespan", "format_timespan_simple", "get_today_date", "get_timestamp"]


def format_timespan(seconds: float) -> str:
    hr, mn, s, ms = split_time(seconds)
    list_time_str = list()
    if hr > 0:
        list_time_str.append(f"{hr} hour{'s' if hr > 1 else ''}")
    if mn > 0:
        list_time_str.append(f"{mn} minute{'s' if mn > 1 else ''}")
    if s > 0:
        list_time_str.append(f"{s} second{'s' if s > 1 else ''}")
    if ms > 0:
        list_time_str.append(f"{ms} millisecond{'s' if ms > 1 else ''}")
    if not list_time_str:
        return "0 second"
    if len(list_time_str) == 1:
        return list_time_str[0]
    return ", ".join(list_time_str[:-1]) + " and " + list_time_str[-1]


def format_timespan_simple(seconds: float) -> str:
    hr, mn, s, ms = split_time(seconds)
    list_time_str = list()
    if hr > 0:
        list_time_str.append(f"{hr} hr")
    if mn > 0:
        list_time_str.append(f"{mn} mn")
    if s > 0:
        list_time_str.append(f"{s} s")
    if ms > 0:
        list_time_str.append(f"{ms} ms")
    if not list_time_str:
        return "0 s"
    return " ".join(list_time_str)


def split_time(seconds: float):
    s = int(seconds)
    ms = round(1000 * (seconds - s))
    mn, s = divmod(s, 60)
    hr, mn = divmod(mn, 60)
    return hr, mn, s, ms


def get_today_date() -> str:
    today = datetime.date.today()
    date = f"{today:%d/%m/%Y}"
    return date


def get_timestamp() -> str:
    timestamp = datetime.datetime.now()
    return f"{timestamp:%Y_%m_%d__%H_%M_%S}"
