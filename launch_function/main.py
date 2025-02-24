#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from prj.src import *


# ------------------------------------------------------------------------------------------------------ #

def main():
    """
    Select the function you want to launch by removing the '#' symbol in front of the line to uncomment it.
    It uses the information configured in file "config.ini".
    It is specified in last line of the comments above the function what inputs are needed to be specified in the
     config.ini file.
    """

    """Uncomment next line to check the coherence of all zones defined in the DC_SYS.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #check_all_zones()

    """Uncomment next line to check the correspondence between (track, KP) and (segment, offset)
    of all objects defined in the DC_SYS.
    @inputs: DC_SYS"""
    #check_offset_correctness()

    """Uncomment next line to use the survey checking tool.
    @inputs: DC_SYS, CCTool-OO Schema, optionally Block Definition, and Survey information"""
    #check_survey()

    """Uncomment next line to compute the minimal length of a multiple path configuration (trapezoid or rhombus)
    used for Customer Data CD_min_length_multiple_path in DC_PAR_Checking tool.
    It corresponds to trapezoid_length in SA_Parameters file.
    You can use argument in_cbtc=True to limit the function to inside CBTC Territory instead of the whole line.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #min_length_multiple_path(in_cbtc=False)

    """Uncomment one of next lines to verify some constraints and rules about the flows.
    You can use argument in_cbtc=True to limit the function to inside CBTC Territory instead of the whole line.
    @inputs: DC_SYS, CCTool-OO Schema and DC_PAR"""
    #cf_dg_1()  # HF General Data, sheet "Flux_Variant_HF"
    #cf_dg_2()  # LF General Data, sheet "Flux_Variant_BF"
    #r_mes_pas_itf_1(in_cbtc=False)  # IXL -> ZC Interface, sheet "Flux_MES_PAS"
    #r_mes_pas_itf_3(in_cbtc=False)  # ZC -> IXL Interface, sheet "Flux_PAS_MES"
    #ats_atc_sheet_verif(in_cbtc=False)  # NV, FRONTAM <-> ZC Interface, sheet "ATS_ATC"
    #r_tm_ats_itf_1(in_cbtc=False)  # NV, Wayside Remote supervision, ZC <-> ATS Interface, sheet "TM_PAS_ATS"

    """Uncomment next line to verify the CBTC Signal Approach Zone so that it is greater than parameter 
     train_to_home_signal_max_dist so to respect R_ZSM_3 at CBTC level.
    @inputs: DC_SYS, CCTool-OO Schema, DC_PAR"""
    #check_cbtc_sig_apz()

    """Uncomment one of next lines to verify some constraints and rules about the IXL Signal Approach Zone.
    You can use argument apz_with_tc=True to consider than the default IXL approach zone is the physical Track Circuit
     containing the signal and not simply the IVB. It needs to be stated in the ZC-IXL ICDD that the IXL will lock the
     physical block by default, else the tool considers only the IVB containing the signal, which is the default case
     if no precision is given.
    You can use as optional input an Excel file defining the IXL Approach Zone, it can only contain the signals where
     the IXL extends the APZ, the signals not present in the file will follow the rule of APZ is composed of the first
     IVB (or TC) upstream the signal. Indeed, it can be specified in the ZC-IXL ICDD that for some signals the
     APZ is extended to more IVB/TC.
    @inputs: DC_SYS, CCTool-OO Schema, DC_PAR and optionally IXL Approach Zone file"""
    #cf_signal_12(apz_with_tc=False)  # DLT distance
    #r_zsm_3(apz_with_tc=False)

    """Uncomment next line to verify the unicity of the IP addresses and of the SSH keys of the DC_TU files
    from every Train Unit (TU) folder of the C11.
    @inputs: C11_D470"""
    #dc_tu_verification()

    """Uncomment next line to regenerate the C11 MD5 Checksum and compare it to the one already present in the C11.
    @inputs: C11_D470"""
    #verification_of_the_md5_checksum()

    """Uncomment next line to get slope at platform.
    You can use argument in_cbtc=True to limit the function to inside CBTC Territory instead of the whole line.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #pretty_print_dict(get_slope_at_plt(in_cbtc=False))

    """Uncomment next line to calculate the smallest size of a switch block heel
    used for Customer Data CD_smallest_size_of_a_switch_block_heel in DC_PAR_Checking tool.
    You can use argument in_cbtc=True to limit the function to inside CBTC Territory instead of the whole line.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #smallest_size_of_a_switch_block_heel(in_cbtc=False)

    """Initialize an empty Fouling Points file with the list of switches from DC_SYS.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #init_fouling_points_file()
    return


# ------------------------------------------------------------------------------------------------------ #
""" This part does not have to be updated. """

if __name__ == "__main__":
    # Create a log file to store the info displayed in the cmd window
    log_file_name, args = init_log()

    with open(log_file_name, "a", encoding="utf-8") as log_file:
        sys.stdout = Logger(log_file)
        # Initialization Functions
        init(args, main_file=__file__, log_file_instance=log_file, log_file_name=log_file_name)

        # Main Functions
        main()
