#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_par_customer_data import cd_alpha
from ..dc_par_customer_data import g


__all__ = ["get_par_gamma_slope"]


def get_par_gamma_slope(local_slope, variables: dict = None):
    value = g(variables) * local_slope / (1 + cd_alpha(variables))
    if variables is not None:
        variables.update({"local_slope": f"{local_slope}"})
    return value
