#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["g"]


def g(variables: dict = None):
    value = 9.81
    if variables is not None:
        variables.update({"G": f"{value} m/s^2"})
    return value
