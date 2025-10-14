#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from _prj.src import *


# ------------------------------------------------------------------------------------------------------ #


def main():
    """
    Select the function you want to launch by removing the '#' symbol in front of the line to uncomment it.
    It uses the information configured in file "config.ini".
    For each function, comments are written above the function to explain its use and in the last line starting
     by "@inputs:", it is written what inputs are needed to be specified in the "config.ini" file to run the function.
    """

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Global DC_SYS consistency checks ---------- #
    """Uncomment next line to check the global coherence of the object names in all sheets in the DC_SYS.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #check_dc_sys_global_definition()

    """Uncomment next line to check the coherence of all zones defined in the DC_SYS.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #check_dc_sys_zones_definition()

    """Uncomment next line to check the correspondence between (track, KP) and (segment, offset)
     of all objects defined in the DC_SYS.
    @inputs: DC_SYS"""
    #check_dc_sys_track_kp_definition()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- DC_PAR Checking Customer Data computations ---------- #
    """Uncomment next line to compute the minimal length of a multiple path configuration (trapezoid or rhombus)
     used for Customer Data CD_min_length_multiple_path in DC_PAR_Checking tool.
    It corresponds to trapezoid_length in SA_Parameters file.
    You can use argument in_cbtc=True to limit the function to inside CBTC Territory instead of the whole line.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #min_length_multiple_path(in_cbtc=False)

    """Uncomment next line to calculate the smallest size of a switch block heel
     used for Customer Data CD_smallest_size_of_a_switch_block_heel in DC_PAR_Checking tool.
    You can use argument in_cbtc=True to limit the function to inside CBTC Territory instead of the whole line.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #pretty_print_dict(smallest_size_of_a_switch_block_heel(in_cbtc=False))

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Constraints and Rules: zones definition ---------- #
    """Uncomment one of next lines to verify some constraints and rules about zone objects definition in DC_SYS.
    @inputs: DC_SYS and CCTool-OO Schema"""
    # --- Block zone definition constraints --- #
    #r_cdv_10()
    #cf_ivb_1_2()
    #cf_ivb_2()
    #cc_cv_16()
    #cc_cv_18()

    # --- CBTC Direction Zone constraints --- #
    #cf_zsm_cbtc_4()
    #cf_zsm_cbtc_10()

    # --- Floor Level constraints --- #
    #cf_flr_lvl_1()

    # --- MAZ constraints --- #
    #cf_zaum_1()
    #cf_zaum_11()

    # --- Walkway constraints --- #
    #cf_walkway_2()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Constraints and Rules: VSP on Virtual Blocks constraints ---------- #
    """Uncomment one of next lines to verify some constraints about VSP on Virtual Blocks.
    @inputs: DC_SYS, CCTool-OO Schema and DC_PAR"""
    #cc_cv_19()
    #cc_cv_20()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Constraints and Rules: CF_SIGNAL_7 Signal VSP protects Switch Point or Fouling Point ---------- #
    """Uncomment next line to verify CF_SIGNAL_7. It checks that the VSP of a signal is correctly placed before
     the Switch Point or Fouling Point that the signal protects.
    @inputs: DC_SYS, CCTool-OO Schema and Fouling Point"""
    #cf_signal_7()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Constraints and Rules: Signal Approach Zone at IXL level ---------- #
    """Uncomment one of next lines to verify some constraints and rules about the IXL Signal Approach Zone:
        CF_SIGNAL_12
        R_ZSM_3
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

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Constraints and Rules: CBTC Direction Zones Home Signals (Non Vital) ---------- #
    """Uncomment next line to verify CF_ZSM_CBTC_16. It checks that the Home Signals of CBTC Direction Zones (of type
     BLOCK_DIRECTION_LOCKING) are correctly configured: either they are on the CDZ or their distance to the CDZ is
     lower than the DLT distance of the signal, so that the turnback can be performed.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #cf_zsm_cbtc_16()  # Non-Vital, verification of Home Signals of CBTC Direction Zones

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Constraints and Rules: messages ---------- #
    """Uncomment one of next lines to verify some constraints and rules about the flows:
        CF_DG_1 about HF General Data, sheet "Flux_Variant_HF"
        CF_DG_2 about LF General Data, sheet "Flux_Variant_BF"
        R_MES_PAS_ITF_1 about IXL -> ZC Interface, sheet "Flux_MES_PAS"
        R_MES_PAS_ITF_3 about ZC -> IXL Interface, sheet "Flux_PAS_MES"
        ATS_ATC sheet verification (Non Vital) FRONTAM <-> ZC Interface, sheet "ATS_ATC"
        R_TM_ATS_ITF_1 (Non Vital) Wayside Remote supervision, ZC <-> ATS Interface, sheet "TM_PAS_ATS"
    You can use argument in_cbtc=True to limit the function to inside CBTC Territory instead of the whole line.
    @inputs: DC_SYS, CCTool-OO Schema and DC_PAR"""
    #cf_dg_1()  # HF General Data, sheet "Flux_Variant_HF"
    #cf_dg_2()  # LF General Data, sheet "Flux_Variant_BF"
    #r_mes_pas_itf_1(in_cbtc=False)  # IXL -> ZC Interface, sheet "Flux_MES_PAS"
    #r_mes_pas_itf_3(in_cbtc=False)  # ZC -> IXL Interface, sheet "Flux_PAS_MES"
    #ats_atc_sheet_verif(in_cbtc=False)  # Non-Vital, FRONTAM <-> ZC Interface, sheet "ATS_ATC"
    #r_tm_ats_itf_1(in_cbtc=False)  # Non-Vital, Wayside Remote supervision, ZC <-> ATS Interface, sheet "TM_PAS_ATS"

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Foundation Data: CBTC Protecting Switch Area ---------- #
    """Uncomment next line to verify the CBTC protecting switch area so that it contains all IVB that are at a distance
     lower than the distance travelled during oc_zc_data_freshness_threshold + ixl_cycle_time, from the motor part of
     the switch (between the switch and the fouling points). The tool uses the local max speed for the computation.
    This list can be empty if the [switch block locking area] is empty.
    @inputs: DC_SYS, CCTool-OO Schema, Fouling Point and DC_PAR"""
    #check_cbtc_protecting_switch_area()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Constraints and Rules: Allow Accel Calibration at OSP ---------- #
    """Uncomment one of next lines to verify constraints and rules about flag [Allow Accel Calibration] of OSP (either
     platform OSP or OSP not platform related). It checks that the slope is constant under the car with accelerometer
     whatever the train polarity and considering the train stopped at +/- the tolerance at OSP.
    @inputs: DC_SYS, CCTool-OO Schema and DC_PAR"""
    #cc_quai_6(in_cbtc=False)  # Allow Accel Calibration at platform OSPs
    #r_point_arret_ato_10(in_cbtc=False)  # Allow Accel Calibration at not platform related OSPs

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Foundation Data: Sieving Limits ---------- #
    """Uncomment next line to check the definition of the Sieving Limits, and in particular the associated block.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #check_sieving_limit_definition()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Constraints and Rules: R_CDV_5 and R_IVB_1 ---------- #
    """Uncomment one of next lines to verify rules R_CDV_5 and R_IVB_1.
    @inputs: DC_SYS, CCTool-OO Schema, Fouling Point, DC_PAR and C11_D470"""
    #r_cdv_5()
    #r_ivb_1()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Foundation Data: Platform Related Overlaps (Non Vital) ---------- #
    """Uncomment next line to verify the attribute [Platform Related] of the Overlaps.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #ixl_overlap_platform_related()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Constraints and Rules: Signal Approach Zone at CBTC level (Non Vital) ---------- #
    """Uncomment next line to verify the CBTC Signal Approach Zone so that it is greater than parameter
     train_to_home_signal_max_dist so to respect R_ZSM_3 at CBTC level.
    @inputs: DC_SYS, CCTool-OO Schema and DC_PAR"""
    #check_cbtc_sig_apz()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Functions about DC_SYS zones that are configurable using DC_SYS sheet names ---------- #
    """Uncomment one of next lines to get from what KP to what KP each track is covered by each object of the
     specified type (examples below are for GES and Protection_Zone sheets).
    You have to specify the sheet name from DC_SYS as the argument to select the object type.
    The tool figures the zone path and will display multiple rows for a same track if there are multiple section of
     a same track covered by a same zone.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #get_zones_kp_limits("GES")
    #get_zones_kp_limits("Protection_Zone")

    """Uncomment one of next lines to get from what KP to what KP each track is covered by the union of specified type 
     (examples below are for CDV and CV sheets).
    You have to specify the sheet name from DC_SYS as the argument to select the object type.
    The tool figures the zone path and will display multiple rows for a same track if there are multiple section of
     a same track covered by a same zone.
    For objects that overlap, the tool will return multiple rows where the end KP may be inside another from/to KP row.
    @inputs: DC_SYS and CCTool-OO Schema"""
    # get_whole_object_type_kp_limits("CDV")
    # get_whole_object_type_kp_limits("CV")

    """Uncomment next line to get list of objects of a specified type intersecting a specified zone (example below is
     to print the list of MAZ (sheet Zaum) intersecting the ZC (sheet PAS) called "ZC_02").
    You have to specify the sheet names from DC_SYS as the arguments to select the object types.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #print(get_objects_in_zone("Zaum", "PAS", "ZC_02"))

    """Uncomment next line to get list of zones covering the specified object (example below is to print the list of ZC
     (sheet PAS) covering the MAZ (sheet Zaum) called "MAZ_STB_110").
    You have to specify the sheet names from DC_SYS as the arguments to select the object types.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #print(get_zones_on_object("PAS", "Zaum", "MAZ_STB_110"))

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Additional Verification about slope at platforms ---------- #
    """Uncomment next line to get the slope at all platforms, and in particular the smallest and the greatest slope.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #pretty_print_dict(get_min_and_max_slope_at_all_platforms(in_cbtc=False))

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- ZC APPLI IF: ZE_IMPACTE_FU ---------- #
    """Uncomment next line to compute the ZC APPLI IF "ZE_IMPACTE_FU". Take into account that the directions are
    computed by the tool according to the segments direction, so if there is a depolarization point inside the ZC,
    the directions will not match.
    @inputs: DC_SYS, CCTool-OO Schema and DC_PAR"""
    #create_computed_result_file_ze_impacte_fu()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Wayside Additional Verification for v6.3.5 ---------- #
    """Uncomment next line to help for the verifications of ADD_VERIF_001 and ADD_VERIF_002 of Wayside DPSA Additional
     Verifications in v6.3.5.
    @inputs: DC_SYS and CCTool-OO Schema"""
    # --- Min (sum of the length of all physical block of the route) --- #
    #get_sum_len_route_physical_blocks()
    # --- Min (length of the first physical block of routes that are in a ZC overlay) --- #
    #get_first_zc_overlay_route_physical_blocks()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Survey Checking ---------- #
    """Uncomment next line to use the survey checking tool.
    @inputs: DC_SYS, CCTool-OO Schema, optionally Block Definition and Survey information"""
    #check_survey()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Onboard Additional Verification about DC_TU files ---------- #
    """Uncomment next line to verify the unicity of the IP addresses and of the SSH keys of the DC_TU files
     from every Train Unit (TU) folder of the C11.
    @inputs: C11_D470"""
    #dc_tu_verification()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Onboard Additional Verification about md5sum regeneration ---------- #
    """Uncomment next line to regenerate the C11 MD5 Checksum and compare it to the one already present in the C11.
    @inputs: C11_D470"""
    #verification_of_the_md5_checksum()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Foundation Data: Distance from signal to joint ---------- #
    """Uncomment next line to get for all signals the distance from the signal to the IVB joint downstream the signal.
    It can be useful to check the position of the signals.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #get_signals_distance_to_joint()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Foundation Data: Distance from OSP to joints and signals ---------- #
    """Uncomment next line to get for all OSPs not platform related the distance from the OSP to next IVB joint
     in both directions, and to next signal in both directions.
    It can be useful to check the position of the OSPs.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #get_osp_not_platform_related_distance_to_joints_and_signals()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------- Fouling Point template file ---------- #
    """Uncomment next line to create an empty Fouling Points template file with the list of switches from DC_SYS,
     to be filled with the Signalling Plan.
    @inputs: DC_SYS and CCTool-OO Schema"""
    #create_fouling_points_template_file()

    return


# ------------------------------------------------------------------------------------------------------ #
""" This part shall not be updated. """

if __name__ == "__main__":
    # Create a log file to store the info printed in the cmd window.
    log_file_name, args = init_log()

    with open(log_file_name, "a", buffering=1, encoding="utf-8") as log_file:
        # Use the Logger class to overwrite the default sys.stdout so that the prints are displayed both in the cmd
        # window using the default sys.stdout and written inside the log_file.
        sys.stdout = Logger(log_file)

        # Initialization function to regenerate the CCTool-OO Schema Python files (in _prj/src/cctool_oo_schema folder)
        # and re-launch a Python instance if needed to take these newly generated files into account.
        init(args, main_file=__file__, log_file_instance=log_file, log_file_name=log_file_name)

        # Main function defined above in this file to launch the selected functions
        main()
