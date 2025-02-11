#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_par import *
from ...dc_par_add_on_parameters import *
from ...dc_sys_draw_path.dc_sys_path_and_distances import get_dist_between_objects
from ...dc_sys_sheet_utils.psr_utils import get_max_psr_speed_on_zone


__all__ = ["check_cbtc_protecting_switch_area"]


def check_cbtc_protecting_switch_area(do_print_warning: bool = True) -> dict[str, dict[str, Any]]:
    max_speed = get_max_speed()
    sw_dict = load_sheet(DCSYS.Aig)
    ivb_dict = load_sheet(DCSYS.IVB)

    nb_sw = len(sw_dict)
    info_dict = dict()
    progress_bar(1, 1, end=True)  # reset progress bar
    for i, (sw_name, sw_val) in enumerate(sw_dict.items()):
        print_log(f"\r{progress_bar(i, nb_sw)} verification of CBTC protecting switch area "
                  f"of {sw_name}...", end="")
        sw_block_locking_area = get_dc_sys_value(sw_val, DCSYS.Aig.SwitchBlockLockingArea.Ivb)
        cbtc_protecting_switch_area = get_dc_sys_value(sw_val, DCSYS.Aig.CbtcProtectingSwitchArea.Ivb)
        if not sw_block_locking_area:
            continue  # This list can be empty if the [switch block locking area] is empty.
        list_ivb_to_protect = set()
        local_speed = get_local_speed(sw_block_locking_area, max_speed)
        dist_to_protect = get_dist_to_protect(local_speed)
        for sw_locked_ivb in sw_block_locking_area:
            list_ivb_to_protect.update(get_ivb_to_protect(sw_locked_ivb, sw_block_locking_area,
                                                          ivb_dict, dist_to_protect, sw_name))

        new_local_speed = get_local_speed(list(list_ivb_to_protect), max_speed)
        nb_ite = 1
        while new_local_speed > local_speed:  # redo the computation
            nb_ite += 1
            local_speed = new_local_speed
            dist_to_protect = get_dist_to_protect(local_speed)
            for sw_locked_ivb in sw_block_locking_area:
                list_ivb_to_protect.update(get_ivb_to_protect(sw_locked_ivb, sw_block_locking_area,
                                                              ivb_dict, dist_to_protect, sw_name))
            new_local_speed = get_local_speed(list(list_ivb_to_protect), max_speed)

        local_speed_km_per_h = local_speed * 3.6
        info_dict[sw_name] = {
            "local_speed_km_per_h": local_speed_km_per_h,
            "dist_to_protect": dist_to_protect,
            "sw_block_locking_area": sw_block_locking_area,
            "cbtc_protecting_switch_area": cbtc_protecting_switch_area,
            "list_ivb_to_protect": list_ivb_to_protect,
        }
        if set(cbtc_protecting_switch_area) == list_ivb_to_protect:
            continue  # OK
        elif list_ivb_to_protect.issubset(set(cbtc_protecting_switch_area)):
            # too many IVB defined inside CBTC -> no safety issue
            if not do_print_warning:
                continue
            print_func = print_warning
        else:
            print_func = print_error

        cbtc_protecting_switch_area_to_print = Color.white + ", ".join([
            f"{ivb}" if ivb in list_ivb_to_protect
            else f"{csi_bg_color(Color.yellow)}{Color.black}{ivb}{Color.reset}{Color.white}"
            for ivb in cbtc_protecting_switch_area
        ]) + Color.reset
        list_ivb_to_protect_to_print = Color.white + ", ".join([
            f"{ivb}" if ivb in cbtc_protecting_switch_area
            else f"{csi_bg_color(Color.yellow)}{Color.black}{ivb}{Color.reset}{Color.white}"
            for ivb in sorted(list_ivb_to_protect)
        ]) + Color.reset

        print_func(f"For switch {Color.blue}{sw_name}{Color.reset}, the CBTC Protecting Switch Area List is "
                   f"different from the one computed by the tool:")
        print(f"{local_speed_km_per_h = :.3f} km/h")
        print(f"{dist_to_protect = :.3f} m")
        print(f"{sw_block_locking_area = }")
        print(f"cbtc_protecting_switch_area = {cbtc_protecting_switch_area_to_print}")
        print(f"list_ivb_to_protect = {list_ivb_to_protect_to_print}")

    print_log(f"\r{progress_bar(nb_sw, nb_sw, end=True)} verification of CBTC protecting switch area "
              f"finished.")

    return info_dict


def get_local_speed(list_ivb: list[str], max_speed: float) -> float:
    local_speed = None
    for ivb_name in list_ivb:
        psr_speed = get_max_psr_speed_on_zone(DCSYS.IVB, ivb_name)
        if psr_speed is not None and (local_speed is None or local_speed < psr_speed):
            local_speed = psr_speed  # get max speed in the zone

    if local_speed is None:
        return max_speed  # by default if no PSR, return max speed
    return local_speed


def get_dist_to_protect(local_speed: Optional[float]) -> float:
    oc_zc_data_freshness_threshold = get_param_value("oc_zc_data_freshness_threshold")
    ixl_cycle_time = get_param_value("ixl_cycle_time")

    dist_to_protect_line = local_speed * (oc_zc_data_freshness_threshold + ixl_cycle_time)

    return dist_to_protect_line


def get_ivb_to_protect(sw_locked_ivb: str, sw_block_locking_area: list[str],
                       ivb_dict: dict[str, Any], dist_to_protect: float, sw_name: str) -> list[str]:
    list_ivb_to_protect = list()
    for ivb_name in ivb_dict.keys():
        if ivb_name in sw_block_locking_area:  # block already protected
            continue
        dist = get_dist_between_objects(DCSYS.IVB, ivb_name, DCSYS.IVB, sw_locked_ivb)
        if dist is not None and dist < dist_to_protect:
            dist_to_sw = get_dist_between_objects(DCSYS.IVB, ivb_name, DCSYS.Aig, sw_name)
            if dist_to_sw is not None and dist_to_sw < 1000:  # taking into account only IVB that can lead to the switch
                # the second test is to avoid taking account the ones accessible through a ring,
                # 1000 m is large compared to the distance to protect and is often lower than the ring length
                list_ivb_to_protect.append(ivb_name)
    return list_ivb_to_protect
