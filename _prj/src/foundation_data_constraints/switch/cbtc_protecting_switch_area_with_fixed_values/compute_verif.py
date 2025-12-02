#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_par import *
from ....dc_sys_draw_path.dc_sys_path_and_distances import get_dist_between_objects
from ....dc_sys_sheet_utils.psr_utils import get_max_psr_speed_on_zone


__all__ = ["compute_verif"]


def compute_verif(train_travel_distance_during_transmission_delay: float,
                  moving_part_of_the_switch_distance: float) -> dict[str, dict[str, Any]]:
    sw_dict = load_sheet(DCSYS.Aig)
    ivb_dict = load_sheet(DCSYS.IVB)

    nb_sw = len(sw_dict)
    info_dict = dict()
    progress_bar(1, 1, end=True)  # reset progress bar
    for i, (sw_name, sw_value) in enumerate(sw_dict.items()):
        print_log_progress_bar(i, nb_sw, f"CBTC protecting switch area of {sw_name}")
        sw_block_locking_area = get_dc_sys_value(sw_value, DCSYS.Aig.SwitchBlockLockingArea.Ivb)
        cbtc_protecting_switch_area = get_dc_sys_value(sw_value, DCSYS.Aig.CbtcProtectingSwitchArea.Ivb)

        if not sw_block_locking_area:
            # This list can be empty if the [Switch block locking area] is empty.
            comments = "[Switch block locking area] is empty, so [CBTC Protecting Switch Area] can be empty."
            info_dict[sw_name] = {
                "sw_block_locking_area": sw_block_locking_area,
                "cbtc_protecting_switch_area": cbtc_protecting_switch_area,
                "comments": comments,
                "status": "NA",
            }
            continue

        list_ivb_to_protect = set()
        dist_to_protect = train_travel_distance_during_transmission_delay
        list_ivb_to_protect.update(_get_ivb_to_protect_with_fp(moving_part_of_the_switch_distance, sw_block_locking_area,
                                                               ivb_dict, dist_to_protect, sw_name))

        ivb_that_shall_be_added = [ivb for ivb in list_ivb_to_protect if ivb not in cbtc_protecting_switch_area]
        ivb_that_can_be_removed = [ivb for ivb in cbtc_protecting_switch_area if ivb not in list_ivb_to_protect]
        info_dict[sw_name] = {
            "sw_block_locking_area": sw_block_locking_area,
            "cbtc_protecting_switch_area": cbtc_protecting_switch_area,
            "moving_part_of_the_switch_distance": moving_part_of_the_switch_distance,
            "dist_to_protect": dist_to_protect,
            "list_ivb_to_protect": list_ivb_to_protect,
            "ivb_that_shall_be_added": ivb_that_shall_be_added,
            "ivb_that_can_be_removed": ivb_that_can_be_removed,
            "comments": None,
        }

        if not ivb_that_shall_be_added and not ivb_that_can_be_removed:
            info_dict[sw_name]["status"] = "OK"
        else:
            if any(ivb_name in sw_block_locking_area for ivb_name in cbtc_protecting_switch_area):
                info_dict[sw_name]["status"] = "KO"
                info_dict[sw_name]["comments"] = ("IVB appearing in [Switch block locking area] shall not appear in "
                                                  "[CBTC protecting switch area].")
            elif not ivb_that_shall_be_added:
                # no IVB to add, only too many IVBs defined inside CBTC -> no safety issue
                info_dict[sw_name]["status"] = "Warning"
                new_comments = "No IVB to add, there are only too many IVBs defined, no safety issue."
                info_dict[sw_name]["comments"] = (new_comments if info_dict[sw_name]["comments"] is None
                                                  else (info_dict[sw_name]["comments"] + "\n\n" + new_comments))
            else:
                # IVBs are missing
                info_dict[sw_name]["status"] = "KO"

    print_log_progress_bar(nb_sw, nb_sw, "verification of CBTC protecting switch area finished", end=True)

    return info_dict


def _get_ivb_to_protect_with_fp(fouling_point_distance: float, sw_block_locking_area: list[str],
                                ivb_dict: dict[str, Any], dist_to_protect: float, sw_name: str) -> list[str]:

    list_ivb_to_protect = list()
    for ivb_name in ivb_dict:
        if ivb_name in sw_block_locking_area:  # block already protected
            continue

        divergent_switch = is_switch_point_upstream_heels(sw_name)

        dist_downstream_switch = get_dist_between_objects(DCSYS.Aig, sw_name, DCSYS.IVB, ivb_name,
                                                          downstream=divergent_switch)

        if dist_downstream_switch is not None and dist_downstream_switch - fouling_point_distance < dist_to_protect:
            # taking into account only IVB that can lead to the switch,
            # the second test is to avoid taking account the ones accessible through a ring,
            # 1000 m is large compared to the distance to protect and is often lower than the ring length
            list_ivb_to_protect.append(ivb_name)

        dist_upstream_switch = get_dist_between_objects(DCSYS.Aig, sw_name, DCSYS.IVB, ivb_name,
                                                        downstream=not divergent_switch)

        if dist_upstream_switch is not None and dist_upstream_switch < dist_to_protect:
            # taking into account only IVB that can lead to the switch,
            # the second test is to avoid taking account the ones accessible through a ring,
            # 1000 m is large compared to the distance to protect and is often lower than the ring length
            list_ivb_to_protect.append(ivb_name)

    return list_ivb_to_protect
