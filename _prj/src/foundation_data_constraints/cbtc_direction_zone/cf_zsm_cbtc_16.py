#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_get_zones import get_objects_in_zone, get_oriented_limits_of_object
from ...dc_sys_draw_path.dc_sys_path_and_distances import get_next_objects_from_a_point, get_dist_downstream


__all__ = ["cf_zsm_cbtc_16"]


def cf_zsm_cbtc_16():
    print_title("Verification of CF_ZSM_CBTC_16", color=Color.mint_green)
    print(f"{Color.white}Instead of checking with the Signalling approach of the signal, "
          f"we check with the DLT distance that is smaller than the Signalling approach."
          f"\nWhen DLT distance is 0, we check that the signal is inside the CBTC Direction Zone.{Color.reset}\n")

    no_ko = True

    cdz_list = get_objects_list(DCSYS.ZSM_CBTC)
    nb_cdz = len(cdz_list)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, cdz_name in enumerate(cdz_list):
        print_log_progress_bar(i, nb_cdz, f"checking {cdz_name} signals")
        authorized_direction = get_dc_sys_value(cdz_name, DCSYS.ZSM_CBTC.SensAutorise)
        if authorized_direction != DirectionZoneType.BLOCK_DIRECTION_LOCKING:
            # Constraint only on BLOCK_DIRECTION_LOCKING CDZ
            continue

        # Get CDZ Home Signals configured in DC_SYS
        list_exit_signals = get_dc_sys_value(cdz_name, DCSYS.ZSM_CBTC.SignauxZsm.Sigman)
        for exit_signal in list_exit_signals:
            if get_dc_sys_value(exit_signal, DCSYS.Sig.Type) != SignalType.MANOEUVRE:
                print_error(f"For CBTC Direction Zone {cdz_name}, configured signal {exit_signal} "
                            f"is not a Home Signal.")
                no_ko = False
        # Get CDZ oriented limits
        oriented_cdz_limits = get_oriented_limits_of_object(DCSYS.ZSM_CBTC, cdz_name)
        stop_exec, no_sub_ko = _check_cdz_oriented_limits(cdz_name, oriented_cdz_limits, list_exit_signals)
        if stop_exec:  # if there is a depolarization inside a CDZ
            if not no_sub_ko:  # a Home Signal is set on this CDZ while there is a depolarization
                no_ko = False
            continue
        # Get list of signals on CDZ
        list_signals_on_cdz = get_objects_in_zone(DCSYS.Sig, DCSYS.ZSM_CBTC, cdz_name)
        if list_signals_on_cdz is None:
            list_signals_on_cdz = list()
        list_signals_on_cdz = [sig_name for sig_name in list_signals_on_cdz
                               if get_dc_sys_value(sig_name, DCSYS.Sig.Type) == SignalType.MANOEUVRE]

        # Do the verification in each direction
        for direction in [Direction.CROISSANT, Direction.DECROISSANT]:
            if not _check_cdz_signal_in_direction(cdz_name, list_exit_signals, oriented_cdz_limits, list_signals_on_cdz,
                                                  direction):
                no_ko = False
    print_log_progress_bar(nb_cdz, nb_cdz, f"verification of the Home Signals of the CBTC Direction Zones "
                                           f"finished", end=True)
    if no_ko:
        print_log("No KO found on the constraint.")


def _check_cdz_oriented_limits(cdz_name: str, oriented_cdz_limits: list[tuple[str, float, str]],
                               list_exit_signals: list[str]) -> tuple[bool, bool]:
    if oriented_cdz_limits[0][2] != oriented_cdz_limits[1][2]:  # if the 2 limit directions are different
        return False, True  # expected definition, no issue
    # Else, there is a depolarization inside the CDZ
    if list_exit_signals:
        print_error(f"There is a depolarization point inside CDZ {cdz_name} and Home Signals are configured, "
                    f"tool does not manage it, verification shall be done manually.")
        return True, False
    return True, True  # we stop the execution, but there is no Home Signal configured so no need to warn the user


def _check_cdz_signal_in_direction(cdz_name: str, list_exit_signals: list[str],
                                   oriented_cdz_limits: list[tuple[str, float, str]],
                                   list_signals_on_cdz: list[str], direction: str) -> bool:
    no_ko = True

    # Get CDZ Home Signals in the corresponding direction
    corresponding_exit_signals = [sig_name for sig_name in list_exit_signals
                                  if get_dc_sys_value(sig_name, DCSYS.Sig.Sens) == direction]
    if len(corresponding_exit_signals) > 1:
        print_error(f"For CBTC Direction Zone {cdz_name}, there are two signals in direction {direction} "
                    f"configured as CDZ Home Signals.")
        no_ko = False
    dc_sys_cdz_signal = corresponding_exit_signals[0] if corresponding_exit_signals else None
    # Get CDZ limit at the end in the corresponding direction, that is the limit in opposite direction
    corresponding_cdz_limit = [(lim_seg, lim_x, lim_direction)
                               for lim_seg, lim_x, lim_direction in oriented_cdz_limits
                               if lim_direction == get_opposite_direction(direction)][0]
    # Get signal on the CDZ in the corresponding direction
    signals_on_cdz = [sig_name for sig_name in list_signals_on_cdz
                      if get_dc_sys_value(sig_name, DCSYS.Sig.Sens) == direction]
    if len(signals_on_cdz) > 1:
        print_error(f"There are multiple signals in direction {direction} on CBTC Direction Zone {cdz_name}.")
        no_ko = False
        signals_on_cdz.sort(key=lambda sig_name: get_dist_downstream(
            get_dc_sys_value(sig_name, DCSYS.Sig.Seg), get_dc_sys_value(sig_name, DCSYS.Sig.X),
            corresponding_cdz_limit[0], corresponding_cdz_limit[1],
            downstream=direction == Direction.CROISSANT))
    # Get next Home Signal from the CDZ limit at the end in the corresponding direction
    next_signals_after_cdz = get_next_objects_from_a_point(
        corresponding_cdz_limit[0], corresponding_cdz_limit[1], direction, DCSYS.Sig, direction)
    if len(next_signals_after_cdz) > 1:  # A switch is reached, these signals shall not be considered.
        next_signals_after_cdz = list()
    next_signals_after_cdz = [(sig_name, polarity, distance)
                              for sig_name, polarity, distance in next_signals_after_cdz
                              if get_dc_sys_value(sig_name, DCSYS.Sig.Type) == SignalType.MANOEUVRE]

    # Get CDZ Home Signal: if there is a signal on the CDZ it is it else we take the next signal if it exists.
    next_signal, on_cdz, distance = (
        (signals_on_cdz[0], True, None) if signals_on_cdz
        else (next_signals_after_cdz[0][0], False, next_signals_after_cdz[0][2]) if next_signals_after_cdz
        else (None, None, None))

    # Separated function to verify the correspondence between DC_SYS and tool results
    if not _do_the_checks(cdz_name, direction, dc_sys_cdz_signal, next_signal, on_cdz, distance):
        no_ko = False
    return no_ko


def _do_the_checks(cdz_name: str, direction: str, dc_sys_cdz_signal: Optional[str],
                   next_signal: Optional[str], on_cdz: Optional[bool], distance: Optional[float]) -> bool:
    # If tool has not found a CDZ Home Signal in this direction
    if next_signal is None:
        # But there is one configured in DC_SYS
        if dc_sys_cdz_signal:
            print_error(f"For CBTC Direction Zone {cdz_name}, in direction {direction}, "
                        f"signal {dc_sys_cdz_signal} shall not be configured as CDZ Home Signal.")
            return False
        return True

    # If tool has found a CDZ Home Signal in this direction that is on the CDZ
    if on_cdz:
        # If a signal is configured in DC_SYS but not the one found by the tool
        if dc_sys_cdz_signal is not None and dc_sys_cdz_signal != next_signal:
            print_error(f"For CBTC Direction Zone {cdz_name}, in direction {direction}, "
                        f"signal {dc_sys_cdz_signal} shall not be configured as CDZ Home Signal, "
                        f"it should be signal {next_signal} instead that is on the CDZ.")
            return False
        # If no signal is configured in DC_SYS
        if dc_sys_cdz_signal is None:
            print_warning(f"For CBTC Direction Zone {cdz_name}, in direction {direction}, "
                          f"there is no signal configured as CDZ Home Signal, "
                          f"signal {next_signal} that is on the CDZ could be configured.")
            return False
    # If tool has found a CDZ Home Signal in this direction that is after the CDZ
    else:
        # We get the DLT distance of this signal
        dlt_distance = get_dc_sys_value(next_signal, DCSYS.Sig.DelayedLtDistance)
        # If DLT distance is larger than the distance from the CDZ to the signal,
        # the signal allows turnback on this CDZ and could be configured.
        test = dlt_distance >= distance

        # If a signal is configured in DC_SYS but not the one found by the tool
        if dc_sys_cdz_signal is not None and dc_sys_cdz_signal != next_signal:
            if not test:
                print_error(f"For CBTC Direction Zone {cdz_name}, in direction {direction}, "
                            f"signal {dc_sys_cdz_signal} shall not be configured as CDZ Home Signal, "
                            f"next signal is {next_signal}, but its DLT distance ({dlt_distance}) "
                            f"is lower than the distance from the CDZ to the signal ({distance}). "
                            f"So, this signal will not permit turnback on this CDZ "
                            f"and should not be configured anyway.")
            else:
                print_error(f"For CBTC Direction Zone {cdz_name}, in direction {direction}, "
                            f"signal {dc_sys_cdz_signal} shall not be configured as CDZ Home Signal, "
                            f"it should be signal {next_signal} instead, which DLT distance ({dlt_distance}) "
                            f"is larger than the distance from the CDZ to the signal ({distance}). "
                            f"So, this signal permits turnback on this CDZ.")
            return False
        # If no signal is configured in DC_SYS, but the test is passed
        if dc_sys_cdz_signal is None and test:
            print_warning(f"For CBTC Direction Zone {cdz_name}, in direction {direction}, "
                          f"there is no signal configured as CDZ Home Signal, "
                          f"signal {next_signal} could be configured. Its DLT distance ({dlt_distance}) "
                          f"is larger than the distance from the CDZ to the signal ({distance}). "
                          f"So, this signal permits turnback on this CDZ.")
            return False
        # If a signal is configured in DC_SYS, and it matches one found by the tool but the test is failed
        if dc_sys_cdz_signal == next_signal and not test:
            print_error(f"For CBTC Direction Zone {cdz_name}, in direction {direction}, "
                        f"signal {dc_sys_cdz_signal} shall not be configured as CDZ Home Signal, "
                        f"it is correctly the next signal, but its DLT distance ({dlt_distance}) "
                        f"is lower than the distance from the CDZ to the signal ({distance}). "
                        f"So, this signal will not permit turnback on this CDZ "
                        f"and should not be configured.")
            return False

    return True
