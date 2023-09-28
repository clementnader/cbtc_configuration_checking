#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


__all__ = ["get_pattern"]


def get_pattern(compiled_pattern: re.Pattern) -> str:
    pattern = compiled_pattern.pattern
    pattern = pattern.replace("^", "").replace("$", "")
    pattern = re.sub("\[.*?]", "x", pattern)  # the '?' is to remove the greedy behavior of the '*' quantifier
    # in order to match with the smallest text inside the brackets, if there is more than one pair of brackets
    return pattern
