#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path import *


__all__ = ["cf_walkway_2"]


def cf_walkway_2():
    print_title("Verification of CF_WALKWAY_2", color=Color.mint_green)
    no_ko = True

    walkway_dict = load_sheet(DCSYS.Walkways_Area)
    plt_dict = load_sheet(DCSYS.Quai)
    for plt_name, plt_value in plt_dict.items():
        walkway_on_plt = get_zones_intersecting_zone(DCSYS.Walkways_Area, DCSYS.Quai, plt_name)
        if not walkway_on_plt:
            print_error(f"A walkway area shall cover platform {plt_name}.")
            no_ko = False
            continue

        if len(walkway_on_plt) > 1:
            print_error(f"A single walkway area shall be defined on platform {plt_name}: {walkway_on_plt = }.")
            no_ko = False

        walkway_on_plt = walkway_on_plt[0]
        test, list_limits_not_in_big_zone = is_zone_completely_included_in_zone(DCSYS.Quai, plt_name,
                                                                                DCSYS.Walkways_Area, walkway_on_plt)
        if not test:
            print_error(f"Walkway {plt_name} shall cover entirely platform {plt_name}. "
                        f"These platform limits are not inside the walkway: {list_limits_not_in_big_zone}")
            no_ko = False

        plt_opening_side = get_dc_sys_value(plt_value, DCSYS.Quai.ExtremiteDuQuai.CoteOuvPortes)[0]
        if any(side != plt_opening_side for side in get_dc_sys_value(plt_value,
                                                                     DCSYS.Quai.ExtremiteDuQuai.CoteOuvPortes)):
            print_error(f"Doors opening side of platform {plt_name} is not the same on both limits.")
            no_ko = False

        ww_left_central, ww_left_lateral, ww_right_central, ww_right_lateral = get_dc_sys_values(
            walkway_dict[walkway_on_plt], DCSYS.Walkways_Area.ForbidEvac.LeftCentral,
            DCSYS.Walkways_Area.ForbidEvac.LeftLateral,
            DCSYS.Walkways_Area.ForbidEvac.RightCentral,
            DCSYS.Walkways_Area.ForbidEvac.RightLateral)

        if plt_opening_side == DoorsOpeningSideType.GAUCHE:
            if not (ww_left_central == YesOrNo.N and ww_left_lateral == YesOrNo.N):
                print_error(f"Doors opening side of the platform is left ({plt_opening_side}), corresponding walkway "
                            f"{walkway_on_plt} should have Forbid Evac on left side set to 'No'.\n"
                            f"{ww_left_central = }, {ww_left_lateral = }")
                no_ko = False
            if not (ww_right_central == YesOrNo.O and ww_right_lateral == YesOrNo.O):
                print_warning(f"Doors opening side of the platform is only left ({plt_opening_side}), "
                              f"but corresponding walkway {walkway_on_plt} has Forbid Evac on right side "
                              f"not set to 'No'. Verify if it's coherent.\n"
                              f"{ww_right_central = }, {ww_right_lateral = }")
                no_ko = False

        elif plt_opening_side == DoorsOpeningSideType.DROITE:
            if not (ww_right_central == YesOrNo.N and ww_right_lateral == YesOrNo.N):
                print_error(f"Doors opening side of the platform is right ({plt_opening_side}), corresponding walkway "
                            f"{walkway_on_plt} should have Forbid Evac on right side set to 'No'.\n"
                            f"{ww_right_central = }, {ww_right_lateral = }")
                no_ko = False
            if not (ww_left_central == YesOrNo.O and ww_left_lateral == YesOrNo.O):
                print_warning(f"Doors opening side of the platform is only right ({plt_opening_side}), "
                              f"but corresponding walkway {walkway_on_plt} has Forbid Evac on left side "
                              f"not set to 'No'. Verify if it's coherent.\n"
                              f"{ww_left_central = }, {ww_left_lateral = }")
                no_ko = False

        elif plt_opening_side in [DoorsOpeningSideType.GAUCHE_DROITE, DoorsOpeningSideType.DROITE_GAUCHE]:
            if not (ww_left_central == YesOrNo.N and ww_left_lateral == YesOrNo.N
                    and ww_right_central == YesOrNo.N and ww_right_lateral == YesOrNo.N):
                print_error(f"Doors opening side of the platform is both ({plt_opening_side}), corresponding walkway "
                            f"{walkway_on_plt} should have Forbid Evac on both sides set to 'No'.\n"
                            f"{ww_left_central = }, {ww_left_lateral = }, {ww_right_central = }, {ww_right_lateral = }")
                no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")
