#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


__all__ = ["get_pattern"]


def get_pattern(compiled_pattern: re.Pattern) -> str:
    pattern_str: str
    pattern_str = compiled_pattern.pattern
    pattern_str = pattern_str.replace("^", "").replace("$", "")
    pattern_str = re.sub(r"\[.*?]", r"x", pattern_str)
    # the '?' is to remove the greedy behavior of the '*' quantifier
    # in order to match with the smallest text inside the brackets, if there is more than one pair of brackets
    return pattern_str
