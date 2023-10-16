#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from ..load_parameters import *
from ..customer_data import *
from .get_gamma_slope import get_par_gamma_slope
from .get_par_coast_time import par_coast_time
from .get_par_traction_cut_time import par_traction_cut_time


def get_at_rollback_dist(local_slope, mtc: bool = False, variables: dict = None):
    gamma_eb = get_param_value("gamma_eb", variables)
    if not mtc:
        at_max_rollback_dist_authorized = get_param_value("at_max_rollback_dist_authorized", variables)
    else:
        at_max_rollback_dist_authorized = get_param_value("mt_max_rollback_dist_authorized", variables)
    par_gamma_slope = get_par_gamma_slope(local_slope, variables)
    par_v1_at_rollback_dist_v = get_par_v1_at_rollback_dist_v(local_slope, mtc, variables)
    par_v2_at_rollback_dist_v = get_par_v2_at_rollback_dist_v(local_slope, mtc, variables)
    par_v3_at_rollback_dist_v = get_par_v3_at_rollback_dist_v(local_slope, mtc, variables)

    value = (at_max_rollback_dist_authorized
             + (par_v1_at_rollback_dist_v * par_traction_cut_time(variables)
                + (par_gamma_traction_max(variables) + par_gamma_slope) * par_traction_cut_time(variables)**2/2) +
             + (par_v2_at_rollback_dist_v * par_coast_time(variables)
                + par_gamma_slope * par_coast_time(variables)**2/2)
             + (par_v3_at_rollback_dist_v**2/(gamma_eb - par_gamma_slope)/2)
             )
    if variables is not None:
        par_v1_str = "par_v1_mtc_rollback_dist_v" if mtc else "par_v1_at_rollback_dist_v"
        par_v2_str = "par_v2_mtc_rollback_dist_v" if mtc else "par_v2_at_rollback_dist_v"
        par_v3_str = "par_v3_mtc_rollback_dist_v" if mtc else "par_v3_at_rollback_dist_v"
        variables.update({
            "par_gamma_slope": f"{par_gamma_slope} m/s^2",
            par_v1_str: f"{par_v1_at_rollback_dist_v} m/s",
            par_v2_str: f"{par_v2_at_rollback_dist_v} m/s",
            par_v3_str: f"{par_v3_at_rollback_dist_v} m/s",
        })
    return value


def par_eb_trigger_speed_in_rollback(variables: dict = None):
    max_speed_authorized_in_rollback = get_param_value("max_speed_authorized_in_rollback", variables)
    margin_c = get_param_value("margin_c", variables)
    value = max_speed_authorized_in_rollback + margin_c
    if variables is not None:
        variables.update({"par_eb_trigger_speed_in_rollback": f"{value} m/s"})
    return value


def get_par_v1_at_rollback_dist_v(local_slope, mtc: bool = False, variables: dict = None):
    par_gamma_slope = get_par_gamma_slope(local_slope, variables)
    if not mtc:
        at_max_rollback_dist_authorized = get_param_value("at_max_rollback_dist_authorized", variables)
    else:
        at_max_rollback_dist_authorized = get_param_value("mt_max_rollback_dist_authorized", variables)
    par_eb_trigger_speed_in_rollback_val = par_eb_trigger_speed_in_rollback(variables)
    value = min(numpy.sqrt(2 * (par_gamma_traction_max(variables) + par_gamma_slope) * at_max_rollback_dist_authorized),
                par_eb_trigger_speed_in_rollback_val)
    if variables is not None:
        variables.update({"par_gamma_slope": f"{par_gamma_slope} m/s^2"})
    return value


def get_par_v2_at_rollback_dist_v(local_slope, mtc: bool = False, variables: dict = None):
    par_gamma_slope = get_par_gamma_slope(local_slope, variables)
    par_v1_at_rollback_dist_v = get_par_v1_at_rollback_dist_v(local_slope, mtc, variables)
    value = (par_v1_at_rollback_dist_v
             + (par_gamma_traction_max(variables) + par_gamma_slope) * par_traction_cut_time(variables))
    if variables is not None:
        par_v1_str = "par_v1_mtc_rollback_dist_v" if mtc else "par_v1_at_rollback_dist_v"
        variables.update({
            "par_gamma_slope": f"{par_gamma_slope} m/s^2",
            par_v1_str: f"{par_v1_at_rollback_dist_v} m/s",
        })
    return value


def get_par_v3_at_rollback_dist_v(local_slope, mtc: bool = False, variables: dict = None):
    par_gamma_slope = get_par_gamma_slope(local_slope, variables)
    par_v2_at_rollback_dist_v = get_par_v2_at_rollback_dist_v(local_slope, mtc, variables)
    value = par_v2_at_rollback_dist_v + par_gamma_slope * par_coast_time(variables)
    if variables is not None:
        par_v2_str = "par_v2_mtc_rollback_dist_v" if mtc else "par_v2_at_rollback_dist_v"
        variables.update({
            "par_gamma_slope": f"{par_gamma_slope} m/s^2",
            par_v2_str: f"{par_v2_at_rollback_dist_v} m/s",
        })
    return value
