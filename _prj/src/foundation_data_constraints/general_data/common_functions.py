#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


__all__ = ["check_object_msgs"]


# ------- Common Sub Functions to test flows ------- #
def check_object_msgs(object_type, msg_dict: dict, object_name: str, condition: bool, condition_str: str,
                   target_msg_types: Union[str, list[str]], shall_be_vital: bool,
                   is_hf: bool = True) -> bool:
    if not isinstance(target_msg_types, list):
        target_msg_types = [target_msg_types]
    object_type_str = get_sheet_name(object_type)

    object_class = DCSYS.Flux_Variant_HF if is_hf else DCSYS.Flux_Variant_BF

    associated_msgs = {msg_name: msg_info for msg_name, msg_info in msg_dict.items()
                       if get_dc_sys_value(msg_info, object_class.NomObjet) == object_name
                       and get_dc_sys_value(msg_info, object_class.NomLogiqueInfo) in target_msg_types}

    success = True
    if not condition:
        if associated_msgs:
            print_warning(f"Useless flow(s) to be removed as the condition {Color.white}"
                          f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} "
                          f"is not met for {object_type_str} {Color.blue}{object_name}{Color.reset}:")
            for msg_name, msg_info in associated_msgs.items():
                print(f"\t{Color.beige}{msg_name}{Color.reset}", end="\n\t\t")
                print(msg_info)
            success = False
        return success

    for target_msg_type in target_msg_types:
        associated_msg = {msg_name: msg_info for msg_name, msg_info in associated_msgs.items()
                          if get_dc_sys_value(msg_info, object_class.NomLogiqueInfo) == target_msg_type}
        if not associated_msg:
            print_error(f"A flow of type {Color.yellow}{target_msg_type}{Color.reset} shall be defined for "
                        f"{object_type_str} {Color.blue}{object_name}{Color.reset} "
                        f"as the condition {Color.white}{condition_str.replace(Color.reset, Color.reset + Color.white)}"
                        f"{Color.reset} is met.")
            success = False
            continue
        # The constraint does not specify if the message shall be vital or not.
        for associated_msg_name, associated_msg_info in associated_msg.items():
            is_msg_vital = (get_dc_sys_value(associated_msg_info, object_class.TypeFoncSecu)
                            == VitalOrNotType.SECU)
            if is_msg_vital != shall_be_vital:
                print_error(f"Flow {Color.beige}{associated_msg_name}{Color.reset} "
                            f"for {object_type_str} {Color.blue}{object_name}{Color.reset} "
                            f"of type {Color.yellow}{target_msg_type}{Color.reset} "
                            f"shall be of type {Color.orange}"
                            f"{VitalOrNotType.SECU if shall_be_vital else VitalOrNotType.FONC}{Color.reset} "
                            f"instead of {VitalOrNotType.SECU if is_msg_vital else VitalOrNotType.FONC}\n"
                            f"(the condition {Color.white}"
                            f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} is met):",
                            end="\n\t\t")
                print(associated_msg_info)
                success = False
    return success
