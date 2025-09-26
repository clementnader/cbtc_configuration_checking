#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_path_and_distances import is_seg_downstream, get_dist_downstream
from ...dc_par import *


__all__ = ["r_dyntag_3"]


def r_dyntag_3():
    print_title(f"Verification of R_DYNTAG_3", color=Color.mint_green)
    res_dict = dict()
    dyn_tag_dict = load_sheet(DCSYS.IATPM_tags)
    if not dyn_tag_dict:
        print("No Dynamic Tag.")
        return None
    nb_dyn_tags = len(dyn_tag_dict.keys())
    block_laying_uncertainty = get_param_value("block_laying_uncertainty")

    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (dyn_tag, dyn_tag_val) in enumerate(dyn_tag_dict.items()):
        print_log_progress_bar(i, nb_dyn_tags, f"processing DMC timeout distance of {dyn_tag}")
        res_dict[dyn_tag] = get_tag_to_last_route_distance(dyn_tag_val)
        calc_dmc_timeout_dist = round(res_dict[dyn_tag]["tag_to_last_route_distance"] + block_laying_uncertainty, 3)
        dc_sys_dmc_timeout_dist = round(get_dc_sys_value(dyn_tag_val, DCSYS.IATPM_tags.DmcTimeout.Distance), 3)
        res_dict[dyn_tag]["calc_dmc_timeout_dist"] = calc_dmc_timeout_dist
        res_dict[dyn_tag]["dc_sys_dmc_timeout_dist"] = dc_sys_dmc_timeout_dist

        if dc_sys_dmc_timeout_dist < calc_dmc_timeout_dist:
            print_error(f"{Color.underline}R_DYNTAG_3{Color.no_underline} is not respected for "
                        f"{Color.blue}{dyn_tag}{Color.reset}:")
            print(f"{calc_dmc_timeout_dist=}")
            print(f"{dc_sys_dmc_timeout_dist=}")
            pretty_print_dict(res_dict[dyn_tag])
    print_log_progress_bar(nb_dyn_tags, nb_dyn_tags, "verification of DMC timeout distance of dynamic "
                           "tags finished", end=True)

    return res_dict


def get_tag_to_last_route_distance(dyn_tag):
    route_dict = load_sheet(DCSYS.Iti)
    list_routes = get_dc_sys_value(dyn_tag, DCSYS.IATPM_tags.Routes.Route)
    if not list_routes:
        return dict()
    last_route = list_routes[-1]
    list_route_ivb = get_dc_sys_value(route_dict[last_route], DCSYS.Iti.RouteIvb.Ivb)
    dest_ivb = get_dc_sys_value(route_dict[last_route], DCSYS.Iti.DestinationIvb)
    first_route_ivb = list_route_ivb[0] if list_routes else dest_ivb
    res_dict = {"last_route": last_route, "first_ivb": first_route_ivb}
    res_dict.update(get_dist_dyn_tag_to_joint(dyn_tag, first_route_ivb))
    return res_dict


def get_dist_dyn_tag_to_joint(dyn_tag, ivb):
    sig_dict = load_sheet(DCSYS.Sig)
    ivb_dict = load_sheet(DCSYS.IVB)
    associated_sig = get_dc_sys_value(dyn_tag, DCSYS.IATPM_tags.Signal)
    sig_direction = get_dc_sys_value(sig_dict[associated_sig], DCSYS.Sig.Sens)
    downstream = True if sig_direction == Direction.CROISSANT else False

    dyn_tag_seg = get_dc_sys_value(dyn_tag, DCSYS.IATPM_tags.Seg)
    dyn_tag_x = get_dc_sys_value(dyn_tag, DCSYS.IATPM_tags.X)

    dist_list = list()
    for i, (seg, x) in enumerate(get_dc_sys_zip_values(ivb_dict[ivb], DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X), start=1):
        if is_seg_downstream(dyn_tag_seg, seg, dyn_tag_x, x, downstream):
            dist = get_dist_downstream(dyn_tag_seg, dyn_tag_x, seg, x, downstream)
            dist_list.append({"ivb_limit": f"IVB Limit {i}", "tag_to_last_route_distance": dist})

    return min(dist_list, key=lambda t: t["tag_to_last_route_distance"])
