#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


__all__ = ["check_obj_msgs"]


# ------- Common Sub Functions to test flows ------- #
def check_obj_msgs(obj_type, msg_dict: dict, obj_name: str, condition: bool, condition_str: str,
                   target_msg_types: Union[str, list[str]], shall_be_vital: bool, only_one_zc: bool = False,
                   is_flux_pas_mes: bool = True, vital_condition: bool = None, vital_condition_str: str = None,
                   obj_type_str: str = None, zc: str = None, tsr_speed: str = None,
                   tsr_area_missing_speeds: list = None):
    if not isinstance(target_msg_types, list):
        target_msg_types = [target_msg_types]
    if obj_type_str is None:
        obj_type_str = get_sh_name(obj_type)
    is_tsr_area_speed = tsr_area_missing_speeds is not None

    obj_class = DCSYS.Flux_PAS_MES if is_flux_pas_mes else DCSYS.Flux_MES_PAS

    associated_msgs = {msg_name: msg_info for msg_name, msg_info in msg_dict.items()
                       if get_dc_sys_value(msg_info, obj_class.NomObjet) == obj_name
                       and get_dc_sys_value(msg_info, obj_class.NomLogiqueInfo) in target_msg_types}

    if zc is not None:
        # We only check the messages related to this ZC
        associated_msgs = {msg_name: msg_info for msg_name, msg_info in associated_msgs.items()
                           if get_dc_sys_value(msg_info, obj_class.PasUtilisateur1) == zc}

    success = True
    if not condition:
        if associated_msgs:
            for target_msg_type in target_msg_types:
                associated_msg = {msg_name: msg_info for msg_name, msg_info in associated_msgs.items()
                                  if get_dc_sys_value(msg_info, obj_class.NomLogiqueInfo) == target_msg_type}
                if zc is None:
                    _check_message_zc(obj_type, obj_name, associated_msg, obj_type_str, target_msg_type,
                                      condition, condition_str, shall_be_vital, is_flux_pas_mes, only_one_zc)
            print_warning(f"Useless flow(s) to be removed as the condition for the message {Color.white}"
                          f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} "
                          f"is not met for {obj_type_str} {Color.blue}{obj_name}{Color.reset}.")
            for msg_name, msg_info in associated_msgs.items():
                print(f"\t{Color.beige}{msg_name}{Color.reset}", end="\n\t\t")
                print(msg_info)
            success = False
        return success

    for target_msg_type in target_msg_types:
        associated_msg = {msg_name: msg_info for msg_name, msg_info in associated_msgs.items()
                          if get_dc_sys_value(msg_info, obj_class.NomLogiqueInfo) == target_msg_type}
        if not associated_msg:
            if is_tsr_area_speed:
                tsr_area_missing_speeds.append(tsr_speed)
                success = False
                continue
            print_error(f"A flow of type {Color.yellow}{target_msg_type}{Color.reset} shall be defined for "
                        f"{obj_type_str} {Color.blue}{obj_name}{Color.reset} "
                        f"as the condition for the message {Color.white}"
                        f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} is met.")
            success = False
            continue
        if zc is None:
            if _check_message_zc(obj_type, obj_name, associated_msg, obj_type_str, target_msg_type,
                                 condition, condition_str, shall_be_vital, is_flux_pas_mes, only_one_zc) is False:
                success = False
        # In ZC Overlay, there would be a message for each ZC
        for associated_msg_name, associated_msg_info in associated_msg.items():
            is_msg_vital = get_dc_sys_value(associated_msg_info, obj_class.TypeInfo) == VitalOrNotType.SECU
            if is_msg_vital != shall_be_vital:
                print_error(f"Flow {Color.beige}{associated_msg_name}{Color.reset} "
                            f"for {obj_type_str} {Color.blue}{obj_name}{Color.reset} "
                            f"of type {Color.yellow}{target_msg_type}{Color.reset} "
                            f"shall be of type {Color.orange}"
                            f"{VitalOrNotType.SECU if shall_be_vital else VitalOrNotType.FONC}{Color.reset} "
                            f"instead of {VitalOrNotType.SECU if is_msg_vital else VitalOrNotType.FONC}\n" +
                            (f"as the vital condition {Color.light_blue}{vital_condition_str}{Color.reset} is "
                             f"{'not ' if not vital_condition else ''}met\n"
                             if vital_condition is not None else "") +
                            f"(the condition for the message {Color.white}"
                            f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} is met):",
                            end="\n\t\t")
                print(associated_msg_info)
                success = False
    return success


def _check_message_zc(obj_type, obj_name: str, associated_msg, obj_type_str, target_msg_type,
                      condition: bool, condition_str: str, shall_be_vital: bool, is_flux_pas_mes: bool,
                      only_one_zc: bool):
    obj_class = DCSYS.Flux_PAS_MES if is_flux_pas_mes else DCSYS.Flux_MES_PAS
    success = True

    expected_zc_list = get_zc_of_obj(obj_type, obj_name)
    related_obj = None
    managed = False
    do_print_warning = True
    if not is_flux_pas_mes and (
            ("GES" in get_class_attr_dict(DCSYS)
             and get_sh_name(obj_type) == get_sh_name(DCSYS.GES))
            or ("Protection_Zone" in get_class_attr_dict(DCSYS)
                and get_sh_name(obj_type) == get_sh_name(DCSYS.Protection_Zone))):
        # for GES and Protection Zone, we need vitally at least that the message is received by
        # the ZC managing the MAZ intersecting the zone
        expected_zc_list, related_obj = get_zc_managing_obj(obj_type, obj_name)
        managed = True  # boolean to tell we are not using all the ZC containing the object but only the one managing it
        do_print_warning = False

    if only_one_zc:
        expected_zc_list, related_obj = get_zc_managing_obj(obj_type, obj_name)

    # if not is_flux_pas_mes and (
    #             # (only_one_zc and get_sh_name(obj_type) == get_sh_name(DCSYS.Sig)) or
    #             ("GES" in get_class_attr_dict(DCSYS)
    #                 and get_sh_name(obj_type) == get_sh_name(DCSYS.GES))
    #             or ("Protection_Zone" in get_class_attr_dict(DCSYS)
    #                 and get_sh_name(obj_type) == get_sh_name(DCSYS.Protection_Zone))
    #         ) or is_flux_pas_mes and (
    #             only_one_zc and get_sh_name(obj_type) == get_sh_name(DCSYS.IVB)
    #             # or get_sh_name(obj_type) == get_sh_name(DCSYS.Sig)
    #             or ("CBTC_Protection_Zone" in get_class_attr_dict(DCSYS)
    #                 and get_sh_name(obj_type) == get_sh_name(DCSYS.CBTC_Protection_Zone))
    #         ):
    #     expected_zc_list, related_obj = get_zc_managing_obj(obj_type, obj_name)
    #     managed = True
    #     if (("GES" in get_class_attr_dict(DCSYS)
    #          and get_sh_name(obj_type) == get_sh_name(DCSYS.GES))
    #             or ("CBTC_Protection_Zone" in get_class_attr_dict(DCSYS)
    #                 and get_sh_name(obj_type) == get_sh_name(DCSYS.CBTC_Protection_Zone))
    #             or ("Protection_Zone" in get_class_attr_dict(DCSYS)
    #                 and get_sh_name(obj_type) == get_sh_name(DCSYS.Protection_Zone))):
    #         do_print_warning = False
    # else:
    #     managed = False
    #     related_obj = None

    msg_zc_dict = dict()
    for associated_msg_name, associated_msg_info in associated_msg.items():
        zc_name = get_dc_sys_value(associated_msg_info, obj_class.PasUtilisateur1)
        if zc_name in msg_zc_dict:
            print_error(f"The flow of type {Color.yellow}{target_msg_type}{Color.reset} for "
                        f"{obj_type_str} {Color.blue}{obj_name}{Color.reset} is defined multiple times "
                        f"for the same ZC {zc_name}.\n"
                        f"(The condition for the message {Color.white}*"
                        f"{condition_str.replace(Color.reset, Color.reset + Color.white)}"
                        f"{Color.reset} is {'not ' if condition else ''}met.)")
            print(msg_zc_dict[zc_name])
            print(associated_msg_name)
            success = False
        msg_zc_dict[zc_name] = associated_msg_name
    extra_msg_zc = {zc_name: info for zc_name, info in msg_zc_dict.items() if zc_name not in expected_zc_list}
    missing_zc = [zc_name for zc_name in expected_zc_list if zc_name not in msg_zc_dict]

    if only_one_zc:
        if len(expected_zc_list) != 1:
            print_warning(f"Tool was unable to find the correct ZC the message has to be configured with:")
            print(f"{expected_zc_list = }"
                  f"\nCurrent configuration:")
            for zc, msg in msg_zc_dict.items():
                print(f"\tfor {Color.beige}{zc = }{Color.reset}: {msg}")
            if len(msg_zc_dict) > 1:
                print_error(f"The flows of {obj_type_str} of type {Color.yellow}{target_msg_type}{Color.reset} "
                            f"shall be sent by a sole ZC in ZC overlay.")
                print_error(f"More than one ZC:")
                for zc, msg in msg_zc_dict.items():
                    print(f"\tfor {Color.beige}{zc = }{Color.reset}: {msg}")

        elif extra_msg_zc or missing_zc:
            print_error(f"The flows of {obj_type_str} of type {Color.yellow}{target_msg_type}{Color.reset} "
                        f"shall be sent by a sole ZC in ZC overlay.")
            print_error(f"Flow(s) of {obj_type_str} {Color.blue}{obj_name}{Color.reset} "
                        f"have to be configured with {Color.pink}{expected_zc_list}{Color.reset}" +
                        (f" <--> {related_obj}" if related_obj is not None else "") +
                        "\nCurrent configuration:", no_pretext=True)
            for zc, msg in msg_zc_dict.items():
                print(f"\tfor {Color.beige}{zc = }{Color.reset}: {msg}")
            success = False

    else:
        if extra_msg_zc and do_print_warning:
            print_warning(f"Useless flow(s) to be removed as {obj_type_str} {Color.blue}{obj_name}{Color.reset} "
                          f"is not {'in' if not managed else 'managed by'} this ZC\n(but "
                          f"{'in' if not managed else 'by'} {expected_zc_list}" +
                          (f" <--> {related_obj}" if related_obj is not None else "") + "):")
            for zc, msg in extra_msg_zc.items():
                print(f"\tfor {Color.beige}{zc = }{Color.reset}: {msg}")
            success = False

        if missing_zc:
            # In case of ZC overlay, we often need that only one of the two ZC sends the signal.
            # Don't know when it is required that both sends the signal (maybe it is only when receiving from the IXL).
            print_error(f"A flow of type {Color.yellow}{target_msg_type}{Color.reset} shall be defined for "
                        f"{obj_type_str} {Color.blue}{obj_name}{Color.reset} "
                        f"for ZC {Color.pink}{missing_zc}{Color.reset} "
                        f"(object is {'in' if not managed else 'managed by'} {expected_zc_list}" +
                        (f" <--> {related_obj}" if related_obj is not None else "") + ").\n"
                        f"It shall be of type {Color.orange}"
                        f"{VitalOrNotType.SECU if shall_be_vital else VitalOrNotType.FONC}{Color.reset}.\n"
                        f"(The condition for the message {Color.white}"
                        f"{condition_str.replace(Color.reset, Color.reset + Color.white)}"
                        f"{Color.reset} is {'not ' if not condition else ''}met.)"
                        "\nCurrent configuration:")
            for zc, msg in msg_zc_dict.items():
                print(f"\tfor {Color.beige}{zc = }{Color.reset}: {msg}")
            success = False

    return success
