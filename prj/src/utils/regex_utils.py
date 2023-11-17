#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


__all__ = ["get_pattern", "delete_middle_capture_group"]


def get_pattern(compiled_pattern: re.Pattern) -> str:
    pattern = compiled_pattern.pattern
    pattern = pattern.replace("^", "").replace("$", "")
    pattern = re.sub("\[.*?]", "x", pattern)
    # the '?' is to remove the greedy behavior of the '*' quantifier
    # in order to match with the smallest text inside the brackets, if there is more than one pair of brackets
    return pattern


def delete_middle_capture_group(text: str, pattern: re.Pattern):
    result = re.search(pattern, text)
    if result is not None:
        return text.replace(result.group(0), result.group(1) + result.group(3))
    return text
