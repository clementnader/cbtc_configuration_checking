#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_path_and_distances import *


__all__ = ["cf_pente_3"]


def cf_pente_3():
    print_title(f"Verification of CF_PENTE_3", color=Color.mint_green)
    no_ko = True
    for sw_name in get_objects_list(DCSYS.Aig):
        sw_seg, sw_x = get_object_position(DCSYS.Aig, sw_name)
        ref_slope = None
        upstream_slopes = get_next_objects_from_a_point(sw_seg, sw_x, Direction.DECROISSANT, DCSYS.Profil)
        downstream_slopes = get_next_objects_from_a_point(sw_seg, sw_x, Direction.CROISSANT, DCSYS.Profil)
        for upstream_slope, upstream_polarity, _ in upstream_slopes:
            upstream_slope_value = (get_dc_sys_value(upstream_slope, DCSYS.Profil.Pente)
                                    * (-1 if not upstream_polarity else 1))
            if ref_slope is None:
                ref_slope = upstream_slope_value
            if upstream_slope_value != ref_slope:
                print_error(f"CF_PENTE_3 is KO for {sw_name}: {upstream_slope_value = } is different from "
                            f"{ref_slope = } ({upstream_slope = })")
                no_ko = False
        for downstream_slope, downstream_polarity, _ in downstream_slopes:
            downstream_slope_value = (get_dc_sys_value(downstream_slope, DCSYS.Profil.Pente)
                                    * (-1 if not downstream_polarity else 1))
            if ref_slope is None:
                ref_slope = downstream_slope_value
            if downstream_slope_value != ref_slope:
                print_error(f"CF_PENTE_3 is KO for {sw_name}: {downstream_slope_value = } is different from "
                            f"{ref_slope = } ({downstream_slope = })")
                no_ko = False
    if no_ko:
        print_log("No KO found.")
