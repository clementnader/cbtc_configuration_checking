#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


__all__ = ["print_route_overlap_results"]


def print_route_overlap_results(route_overlap_str: str, result: bool, nb_in_dc_sys: int, nb_in_control_tables: int,
                                list_missing_in_control_tables: list[str], list_missing_in_dc_sys: list[str],
                                ) -> bool:
    print()
    print_bar()
    print(f"Total number of {route_overlap_str.title()}s in DC_SYS: "
          f"{Color.yellow}{nb_in_dc_sys}{Color.reset}\n"
          f"Total number of {route_overlap_str.title()}s in Control Tables: "
          f"{Color.yellow}{nb_in_control_tables}{Color.reset}\n")
    print_bar()
    if result is True and not (list_missing_in_control_tables or list_missing_in_dc_sys):
        print_section_title(f"Result of {route_overlap_str.title()} verification:")
        print_success(f"{route_overlap_str.title()}s in DC_SYS correspond to the Control Tables.\n")
        return True
    if not list_missing_in_dc_sys and list_missing_in_control_tables:
        print_warning(f"All {route_overlap_str}s from the Control Tables are implemented, "
                      f"but extra {route_overlap_str}s appear in the DC_SYS.\n",
                      no_prefix=True)
    elif list_missing_in_dc_sys and not list_missing_in_control_tables:
        print_warning(f"All {route_overlap_str}s in the DC_SYS appear in the Control Tables, "
                      f"but extra {route_overlap_str}s in the Control Tables are missing in the DC_SYS.\n",
                      no_prefix=True)
    elif list_missing_in_dc_sys and list_missing_in_control_tables:
        print_warning(f"{route_overlap_str.title()}s are missing between the DC_SYS and the Control Tables.\n",
                      no_prefix=True)
    else:
        print_success(f"All {route_overlap_str}s have been found between the DC_SYS and the Control Tables.\n",
                      no_prefix=True)

    if list_missing_in_control_tables:
        print_section_title(f"Missing information for {route_overlap_str.title()}:")
        print_warning(f"The following {Color.yellow}{len(list_missing_in_control_tables)}{Color.reset} "
                      f"{route_overlap_str}s in the DC_SYS are missing in the Control Tables:\n"
                      f"\t{Color.yellow}" + "\n\t".join(list_missing_in_control_tables) + f"{Color.reset}\n")
    if list_missing_in_dc_sys:
        print_section_title(f"Exhaustiveness of {route_overlap_str.title()}:")
        print_warning(f"The following {Color.yellow}{len(list_missing_in_dc_sys)}{Color.reset} "
                      f"{route_overlap_str}s in the Control Tables are missing in the DC_SYS:\n"
                      f"\t{Color.yellow}" + "\n\t".join(list_missing_in_dc_sys) + f"{Color.reset}\n")

    print_section_title(f"Result of {route_overlap_str.title()} verification:")
    print_error(f"{route_overlap_str.title()}s in DC_SYS do not correspond to the Control Tables.\n",
                no_prefix=True)
    return False
