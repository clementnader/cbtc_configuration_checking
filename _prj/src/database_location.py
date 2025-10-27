#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["DATABASE_LOCATION"]


class Projects:
    Ankara_L1 = "Ankara_L1"
    Ankara_L2 = "Ankara_L2"
    Brussels_P1B0 = "Brussels_P1B0"
    Brussels_P1B2 = "Brussels_P1B2"
    Copenhagen_KCR = "Copenhagen_KCR"
    Glasgow_IATP = "Glasgow_IATP"
    Glasgow_CBTC = "Glasgow_CBTC"
    Lima_ML2 = "Lima_ML2"
    Milan_ML4 = "Milan_ML4"
    Panama = "Panama"
    Riyadh_RL3 = "Riyadh_RL3"
    Stockholm_Red_Line = "Stockholm_Red_Line"
    Thessaloniki_TSK = "Thessaloniki_TSK"

    OCTYS_L3 = "OCTYS_L3"
    OCTYS_L6 = "OCTYS_L6"

    Baltimore_MTA = "Baltimore_MTA"
    BART = "BART"
    Hurontario_HLR = "Hurontario_HLR"
    Ontario_OL_RSSOM = "Ontario_OL_RSSOM"
    SEPTA_MSH = "SEPTA_MSH"

    Chennai_CMRL = "Chennai_CMRL"
    Kolkata_KMRC = "Kolkata_KMRC"
    NaviMumbai_NMML1 = "NaviMumbai_NMML1"
    Noida_NS01 = "Noida_NS01"

    Sanying_SYL = "Sanying_SYL"
    Taipei_TC1 = "Taipei_TC1"
    Wenzhou_WZS1 = "Wenzhou_WZS1"

    Chengdu_CDL1 = "Chengdu_CDL1"
    Chengdu_CDL2 = "Chengdu_CDL2"
    Chengdu_CDL6 = "Chengdu_CDL6"
    Chengdu_CDL10 = "Chengdu_CDL10"
    Dalian_DLL1 = "Dalian_DLL1"
    Dalian_DLL2 = "Dalian_DLL2"
    Dalian_DLL3 = "Dalian_DLL3"
    Dalian_JinPu_DLJP = "Dalian_JinPu_DLJP"
    HangShao_HSL = "HangShao_HSL"
    Hangzhou_HZL1 = "Hangzhou_HZL1"
    Hangzhou_HZL2 = "Hangzhou_HZL2"
    Hangzhou_HZL4 = "Hangzhou_HZL4"
    Hangzhou_HZL9 = "Hangzhou_HZL9"
    Shaoxing_SXL1 = "Shaoxing_SXL1"
    Shenyang_SHYL1 = "Shenyang_SHYL1"
    Shenyang_SHYL2 = "Shenyang_SHYL2"
    Shenyang_SHYL10 = "Shenyang_SHYL10"
    Tianjin_TJL5 = "Tianjin_TJL5"
    Xian_XAL2 = "Xian_XAL2"
    Zhengzhou_ZZL1 = "Zhengzhou_ZZL1"

    DB_CORE_4_8_0_0 = "DB_CORE_4_8_0_0"
    DB_CORE_6_3_5_0 = "DB_CORE_6_3_5_0"
    DB_CORE_6_6_0_2 = "DB_CORE_6_6_0_2"
    DB_CORE_7_3_3_0 = "DB_CORE_7_3_3_0"
    DB_CORE_7_4_0_0 = "DB_CORE_7_4_0_0"
    DB_CORE_72_1_4_0 = "DB_CORE_72_1_4_0"
    DB_CORE_72_2_1_0 = "DB_CORE_72_2_1_0"
    DB_CORE_8_3_1_0 = "DB_CORE_8_3_1_0"

    Mock_up = "Mock-up"
    Mock_up_2 = "Mock-up 2"
    Mock_up_3 = "Mock-up 3"
    Mock_up_4 = "Mock-up 4"
    Mock_up_5 = "Mock-up 5"
    Mock_up_6 = "Mock-up 6"


# --- Main projects --- #
# PROJECT_NAME = Projects.Ankara_L1
# PROJECT_NAME = Projects.Ankara_L2
# PROJECT_NAME = Projects.Brussels_P1B0
# PROJECT_NAME = Projects.Brussels_P1B2
# PROJECT_NAME = Projects.Copenhagen_KCR
# PROJECT_NAME = Projects.Glasgow_IATP
# PROJECT_NAME = Projects.Glasgow_CBTC
# PROJECT_NAME = Projects.Lima_ML2
# PROJECT_NAME = Projects.Milan_ML4  # TODO manage R_S01_0102_202 in route verif
PROJECT_NAME = Projects.Panama
# PROJECT_NAME = Projects.Riyadh_RL3
# PROJECT_NAME = Projects.Stockholm_Red_Line
# PROJECT_NAME = Projects.Thessaloniki_TSK

# --- OCTYS --- #
# PROJECT_NAME = Projects.OCTYS_L3
# PROJECT_NAME = Projects.OCTYS_L6

# --- USA --- #
# PROJECT_NAME = Projects.Baltimore_MTA
# PROJECT_NAME = Projects.BART
# PROJECT_NAME = Projects.Hurontario_HLR
# PROJECT_NAME = Projects.Ontario_OL_RSSOM
# PROJECT_NAME = Projects.SEPTA_MSH

# --- India --- #
# PROJECT_NAME = Projects.Chennai_CMRL
# PROJECT_NAME = Projects.Kolkata_KMRC
# PROJECT_NAME = Projects.NaviMumbai_NMML1
# PROJECT_NAME = Projects.Noida_NS01

# --- China --- #
# PROJECT_NAME = Projects.Sanying_SYL
# PROJECT_NAME = Projects.Taipei_TC1
# PROJECT_NAME = Projects.Wenzhou_WZS1
# --- China V4 --- #
# PROJECT_NAME = Projects.Chengdu_CDL1
# PROJECT_NAME = Projects.Chengdu_CDL2
# PROJECT_NAME = Projects.Chengdu_CDL6
# PROJECT_NAME = Projects.Chengdu_CDL10
# PROJECT_NAME = Projects.Dalian_DLL1
# PROJECT_NAME = Projects.Dalian_DLL2
# PROJECT_NAME = Projects.Dalian_DLL3
# PROJECT_NAME = Projects.Dalian_JinPu_DLJP
# PROJECT_NAME = Projects.HangShao_HSL
# PROJECT_NAME = Projects.Hangzhou_HZL1
# PROJECT_NAME = Projects.Hangzhou_HZL2
# PROJECT_NAME = Projects.Hangzhou_HZL4
# PROJECT_NAME = Projects.Hangzhou_HZL9
# PROJECT_NAME = Projects.Shaoxing_SXL1
# PROJECT_NAME = Projects.Shenyang_SHYL1
# PROJECT_NAME = Projects.Shenyang_SHYL2
# PROJECT_NAME = Projects.Shenyang_SHYL10
# PROJECT_NAME = Projects.Tianjin_TJL5
# PROJECT_NAME = Projects.Xian_XAL2
# PROJECT_NAME = Projects.Zhengzhou_ZZL1

# --- DB CORE --- #
# PROJECT_NAME = Projects.DB_CORE_4_8_0_0
# PROJECT_NAME = Projects.DB_CORE_6_3_5_0
# PROJECT_NAME = Projects.DB_CORE_6_6_0_2
# PROJECT_NAME = Projects.DB_CORE_7_3_3_0
# PROJECT_NAME = Projects.DB_CORE_7_4_0_0
# PROJECT_NAME = Projects.DB_CORE_72_1_4_0
# PROJECT_NAME = Projects.DB_CORE_72_2_1_0
# PROJECT_NAME = Projects.DB_CORE_8_3_1_0

# --- Mock-up --- #
# PROJECT_NAME = Projects.Mock_up
# PROJECT_NAME = Projects.Mock_up_2
# PROJECT_NAME = Projects.Mock_up_3
# PROJECT_NAME = Projects.Mock_up_4
# PROJECT_NAME = Projects.Mock_up_5
# PROJECT_NAME = Projects.Mock_up_6


class ProjectDatabaseLocation:
    class ControlTablesLocation:
        control_tables_addr = []
        all_pages = []
        specific_pages = []

    class SurveyLocation:
        survey_addr = []
        survey_sheet = []
        all_sheets = []
        start_row = []
        ref_col = []
        type_col = []
        track_col = []
        survey_kp_col = []

    class IxlApz:
        ixl_apz_file = None
        ixl_apz_sheet_name = None
        start_line = None
        sig_column = None
        apz_start_column = None
        apz_nb_columns = None

    cctool_oo_schema = r""
    dc_sys_addr = r""
    dc_sys_addr_old = r""
    dc_par_addr = r""
    dc_bop_addr = r""
    block_def = None
    survey_loc = SurveyLocation()
    kit_c11_dir = r""
    kit_c11_sp_dir = r""
    kit_c121_d470_dir = r""
    control_tables_route = ControlTablesLocation()
    control_tables_overlap = ControlTablesLocation()
    control_tables_config_ini_file = r"control_tables_configuration.ini"
    ixl_apz = IxlApz()
    fouling_point_addr = r""

    def __init__(self, project_name: str):

        # ------------------------------- Ankara L1 -------------------------------#
        if project_name == Projects.Ankara_L1:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Ankara\ANK_L1\ANK_L1_C_D470_V12_05_RC2\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\Ankara\ANK_L1\ANK_L1_C_D470_V12_05_RC2\DC_PAR.xls"
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\Ankara\ANK_L1\circuitdevoie.xlsx"
            self.survey_loc.survey_addr = (
                r"C:\CBTC\PROJECTS\Ankara\SURVEY\ANK_L1_C_D932_14_00_RC1.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # ------------------------------- Ankara L2 -------------------------------#
        if project_name == Projects.Ankara_L2:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Ankara\ANK_L2\ANK_L2_C_D470_V06_00_RC4\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\Ankara\ANK_L2\ANK_L2_C_D470_V06_00_RC4\DC_PAR.xls"
            self.dc_bop_addr = r"C:\CBTC\PROJECTS\Ankara\ANK_L2\ANK_L2_C_D470_V06_00_RC4\DC_BOP.xls"
            self.kit_c11_dir = r"C:\CBTC\PROJECTS\Ankara\ANK_L2\ANK_L2_C11_D470_06_05_03_V07"
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\Ankara\ANK_L2\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = [
                r"C:\CBTC\PROJECTS\Ankara\SURVEY\ANK_L2_C_D932_01_00_RC2.xlsx",
                r"C:\CBTC\PROJECTS\Ankara\SURVEY"
                r"\Metro_gzrgh_KM_SON_BufferAdded_FoulingPadded_JointAdded_rev01.xlsx"]
            self.survey_loc.survey_sheet = [r"Result Final", r"Survey_Template"]
            self.survey_loc.all_sheets = [False, False]
            self.survey_loc.start_row = [2, 2]
            self.survey_loc.ref_col = [1, 1]
            self.survey_loc.type_col = [4, 2]
            self.survey_loc.track_col = [2, 3]
            self.survey_loc.survey_kp_col = [3, 5]
            # -- Control Tables -- #
            self.control_tables_config_ini_file = "control_tables_configuration_ank.ini"
            self.control_tables_route.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Ankara\Control Tables\B20AC0500161315E_04_01 - Route L2.pdf"]
            self.control_tables_route.all_pages = [False]
            self.control_tables_route.specific_pages = [(24, 104)]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Ankara\Control Tables\B20AC0500161316E_04_01 - Overlap L2.pdf"]
            self.control_tables_overlap.all_pages = [False]
            self.control_tables_overlap.specific_pages = [(18, 93)]

        # ------------------------------- Brussels -------------------------------#
        elif project_name.startswith("Brussels"):
            phase_1b0 = project_name == Projects.Brussels_P1B0
            phase_1b2 = project_name == Projects.Brussels_P1B2
            if phase_1b0:
                self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0\BXL_C_D470_72_01_05_V09_P1B0_R5"
                                    r"\DC_SYS.xls")
                self.dc_par_addr = (r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0\BXL_C_D470_72_01_05_V09_P1B0_R5"
                                    r"\DC_PAR.xls")
                self.dc_bop_addr = (r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0\BXL_C_D470_72_01_05_V09_P1B0_R5"
                                    r"\C64_D413\DC_BOP.xls")
                self.kit_c11_dir = r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0\BXL_C11_D470_72_01_05_V09_P1B0_R5"
                self.fouling_point_addr = (r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0"
                                           r"\fouling_point_fd_checking_1b0.xlsx")
                # -- Survey -- #
                self.survey_loc.survey_addr = [
                    r"C:\CBTC\PROJECTS\Brussels\Survey\BXL_Photobook_survey.xlsx",
                    r"C:\CBTC\PROJECTS\Brussels\Survey\20220505_V4_AFS_DEP_ML_DEF_12.04.24.xlsx",
                    r"C:\CBTC\PROJECTS\Brussels\Survey\BXL_AFS_Patch.xlsx"]
                # -- Control Tables -- #
                self.control_tables_config_ini_file = "control_tables_configuration_bxl.ini"
                self.control_tables_route.control_tables_addr = [
                    r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0\CONTROL TABLES"
                    r"\Control Tables Erasme Antenna 90000534.L02.FR 04.00"
                    r"\90000536.L02.FR-BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_rev03.01.pdf",
                    r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0\CONTROL TABLES"
                    r"\Control Tables Erasme Depot 90000527.L02.FR 04.00"
                    r"\90000528.L02.FR-BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_rev03.00.pdf"]
                self.control_tables_route.all_pages = [True, True]
                self.control_tables_route.specific_pages = [None, None]
                self.control_tables_overlap.control_tables_addr = [
                    r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0\CONTROL TABLES"
                    r"\Control Tables Erasme Antenna 90000534.L02.FR 04.00"
                    r"\90000537.L02.FR-BXL_IXL_ LISTE DES OVERLAP + PARAMÈTRES OVERLAP_FR_rev03.01.pdf",
                    r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0\CONTROL TABLES"
                    r"\Control Tables Erasme Depot 90000527.L02.FR 04.00"
                    r"\90000530.L02.FR-BXL_IXL_LISTE DES OVERLAP + PARAMÈTRES OVERLAP_FR_rev02.00.pdf"]
                self.control_tables_overlap.all_pages = [True, True]
                self.control_tables_overlap.specific_pages = [None, None]
                # -- IXL Approach Zone -- #
                self.ixl_apz.ixl_apz_file = r"C:\CBTC\PROJECTS\Brussels\BXL_P1B0\BXL_IXL_APZ.xlsx"
                self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
                self.ixl_apz.start_line = 2
                self.ixl_apz.sig_column = "A"
                self.ixl_apz.apz_start_column = 9
                self.ixl_apz.apz_nb_columns = 5
            elif phase_1b2:
                self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Brussels\BXL_P1B2\BXL_C_D470_72_02_01_V02_P1B2"
                                    r"\DC_SYS.xls")
                self.dc_par_addr = (r"C:\CBTC\PROJECTS\Brussels\BXL_P1B2\BXL_C_D470_72_02_01_V02_P1B2"
                                    r"\DC_PAR.xls")
                self.dc_bop_addr = (r"C:\CBTC\PROJECTS\Brussels\BXL_P1B2\BXL_C_D470_72_02_01_V02_P1B2"
                                    r"\C64_D413\DC_BOP.xls")
                # -- Survey -- #
                self.survey_loc.survey_addr = [
                    r"C:\CBTC\PROJECTS\Brussels\Survey\BXL_Photobook_survey_1B2.xlsx",
                    r"C:\CBTC\PROJECTS\Brussels\Survey\20220505_V4_AFS_DEP_ML_DEF_12.04.24.xlsx",
                    r"C:\CBTC\PROJECTS\Brussels\Survey\BXL_AFS_Patch.xlsx"]
                # -- Control Tables -- #
                self.control_tables_config_ini_file = "control_tables_configuration_bxl.ini"
                self.control_tables_route.control_tables_addr = [
                    r"C:\CBTC\PROJECTS\Brussels\BXL_P1B2\CONTROL TABLES"
                    r"\90000559.L02.FR-BXL_IXL_L1-5_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_PHASE_1B2_rev02.00.pdf",
                    r"C:\CBTC\PROJECTS\Brussels\BXL_P1B2\CONTROL TABLES"
                    r"\90000564.L02.FE-BXL_IXL_LISTE_DES_ITINÉRAIRES+PARAMÈTRES_DES_ITINÉRAIRES_PHASE_1B2_rev00.00.pdf"]
                self.control_tables_route.all_pages = [True, True]
                self.control_tables_route.specific_pages = [None, None]
                self.control_tables_overlap.control_tables_addr = [
                    r"C:\CBTC\PROJECTS\Brussels\BXL_P1B2\CONTROL TABLES"
                    r"\90000560.L02.FR-BXL_IXL_L1-5_LISTE DES OVERLAP + PARAMÈTRES OVERLAP_PHASE_1B2_rev02.001.pdf",
                    r"C:\CBTC\PROJECTS\Brussels\BXL_P1B2\CONTROL TABLES"
                    r"\90000566.L02.FE-BXL_IXL_LISTE_DES_OVERLAP+PARAMÈTRES_DES_OVERLAP_PHASE_1B2_rev00.00.pdf"]
                self.control_tables_overlap.all_pages = [True, True]
                self.control_tables_overlap.specific_pages = [None, None]
            # -- Survey -- #
            self.survey_loc.survey_sheet = [r"PhotoBook", r"Export_travaillé", r"Survey_Patch"]
            self.survey_loc.all_sheets = [False, False, False]
            self.survey_loc.start_row = [2, 13, 7]
            self.survey_loc.ref_col = [1, 1, 1]
            self.survey_loc.type_col = [2, 2, 2]
            self.survey_loc.track_col = [3, 3, 3]
            self.survey_loc.survey_kp_col = [4, 11, 4]

        # ------------------------------- Copenhagen KCR -------------------------------#
        elif project_name == Projects.Copenhagen_KCR:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Copenhagen KCR\KCR_C_D470_06_06_01_V04_R4\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\Copenhagen KCR\KCR_C_D470_06_06_01_V04_R4\DC_PAR.xls"
            self.dc_bop_addr = r"C:\CBTC\PROJECTS\Copenhagen KCR\KCR_C_D470_06_06_01_V04_R4\C64_D413\DC_BOP.xls"
            self.kit_c11_dir = r"C:\CBTC\PROJECTS\Copenhagen KCR\KCR_C11_D470_06_06_01_V04_R4"
            self.fouling_point_addr = (r"C:\CBTC\PROJECTS\Copenhagen KCR"
                                       r"\Fouling point data_KCR_V06_06_01_v03_récollé.xlsx")
            # -- Survey -- #
            # self.block_def = r"C:\CBTC\PROJECTS\Copenhagen KCR\CIRCUIT_DE_VOIE_patch_12_01_RC2.xls"
            self.survey_loc.survey_addr = [
                r"C:\CBTC\PROJECTS\Copenhagen KCR"
                r"\CR-ASTS-042189 - 15.00_ATT002 - ATC- KCR C_D932 - Field Survey report.xlsx",
                r"C:\CBTC\PROJECTS\Copenhagen KCR"
                r"\AFS_Project_KCR_Sydhavn_survey_eng table_30.08.23.xlsx"]
            self.survey_loc.survey_sheet = [r"Result Final", r"D932"]
            self.survey_loc.all_sheets = [False, False]
            self.survey_loc.start_row = [2, 3]
            self.survey_loc.ref_col = [1, 1]
            self.survey_loc.type_col = [4, 2]
            self.survey_loc.track_col = [2, 3]
            self.survey_loc.survey_kp_col = [3, 5]
            # -- Control Tables -- #
            self.control_tables_config_ini_file = "control_tables_configuration_kcr.ini"
            self.control_tables_route.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Copenhagen KCR\CONTROL TABLES"
                r"\CR-ASTS-045007-11.00-ATT001- Line CT Routes.pdf",
                r"C:\CBTC\PROJECTS\Copenhagen KCR\CONTROL TABLES"
                r"\CR-ASTS-045017-12.00-ATT001- CMC CT Routes.pdf"]
            self.control_tables_route.all_pages = [True, True]
            self.control_tables_route.specific_pages = [None, None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Copenhagen KCR\CONTROL TABLES"
                r"\CR-ASTS-045009-07.00-ATT001- Line CT Overlap.pdf",
                r"C:\CBTC\PROJECTS\Copenhagen KCR\CONTROL TABLES"
                r"\CR-ASTS-045019-09.00 ATC CMC Control Tables Overlap.pdf"]
            self.control_tables_overlap.all_pages = [True, True]
            self.control_tables_overlap.specific_pages = [None, None]
            # -- IXL Approach Zone -- #
            self.ixl_apz.ixl_apz_file = (r"C:\CBTC\PROJECTS\Copenhagen KCR"
                                         r"\CR-ASTS-GEN=Gen-PS=ATC=GEN-IFM-ICD-042155_15.00"
                                         r"#ATT004XLSX - ATC - C12_D404  IXL APZ Rev01.xlsx")
            self.ixl_apz.ixl_apz_sheet_name = r"IXL APZ"
            self.ixl_apz.start_line = 2
            self.ixl_apz.sig_column = "A"
            self.ixl_apz.apz_start_column = 2
            self.ixl_apz.apz_nb_columns = 5

        # ------------------------------- Glasgow -------------------------------#
        elif project_name.startswith("Glasgow"):
            iatp = project_name == Projects.Glasgow_IATP
            cbtc = project_name == Projects.Glasgow_CBTC
            if iatp:
                self.dc_sys_addr = r"C:\CBTC\PROJECTS\Glasgow\GW_C_D470_06_06_01_V05\DC_SYS_IATPM.xls"
                self.dc_par_addr = r"C:\CBTC\PROJECTS\Glasgow\GW_C_D470_06_06_01_V05\DC_PAR.xls"
                self.dc_bop_addr = r"C:\CBTC\PROJECTS\Glasgow\GW_C_D470_06_06_01_V05\C64_D413\DC_BOP.xls"
                self.kit_c11_dir = r"C:\CBTC\PROJECTS\Glasgow\GW_C11_D470_06_06_01_V05"
            elif cbtc:
                self.dc_sys_addr = r"C:\CBTC\PROJECTS\Glasgow\GW_C_D470_07_03_03_V04\DC_SYS.xls"
                self.dc_par_addr = r"C:\CBTC\PROJECTS\Glasgow\GW_C_D470_07_03_03_V04\DC_PAR.xls"
                self.dc_bop_addr = r"C:\CBTC\PROJECTS\Glasgow\GW_C_D470_07_03_03_V04\C64_D413\DC_BOP.xls"
                self.kit_c11_dir = r"C:\CBTC\PROJECTS\Glasgow\GW_C11_D470_07_03_03_V04"
                self.fouling_point_addr = (r"C:\CBTC\PROJECTS\Glasgow"
                                           r"\Fouling Points - GW_C_D470_07_03_03_V02_R3.xlsx")
            # -- Survey -- #
            self.survey_loc.survey_addr = (
                r"C:\CBTC\PROJECTS\Glasgow\SURVEY\2025_01_15 Survey Data and Input Sheet.xlsx")
            self.survey_loc.survey_sheet = r"GW_ML_survey_inputs"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 2
            self.survey_loc.track_col = 3
            self.survey_loc.survey_kp_col = 5
            # -- Control Tables -- #
            if iatp:
                self.control_tables_config_ini_file = "control_tables_configuration_gw.ini"
                self.control_tables_route.control_tables_addr = [
                    r"C:\CBTC\PROJECTS\Glasgow\Control Tables\IATP"
                    r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_Rev00-3-86-Routes.pdf",
                    r"C:\CBTC\PROJECTS\Glasgow\Control Tables\IATP"
                    r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_Rev00-3-81-Routes.pdf"]
                self.control_tables_route.all_pages = [True, True]
                self.control_tables_route.specific_pages = [None, None]
                self.control_tables_overlap.control_tables_addr = [
                    r"C:\CBTC\PROJECTS\Glasgow\Control Tables\IATP"
                    r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_Rev00-173-236-Overlap.pdf",
                    r"C:\CBTC\PROJECTS\Glasgow\Control Tables\IATP"
                    r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_Rev00-162-173-Overlap.pdf"]
                self.control_tables_overlap.all_pages = [True, True]
                self.control_tables_overlap.specific_pages = [None, None]
            elif cbtc:
                self.control_tables_config_ini_file = "control_tables_configuration_gw.ini"
                self.control_tables_route.control_tables_addr = [
                    r"C:\CBTC\PROJECTS\Glasgow\Control Tables\CBTC\rev 04.00"
                    r"\GWISIGIXL0400-04.00-ATT002 - Appendix B_Routes_Rev00.pdf",
                    r"C:\CBTC\PROJECTS\Glasgow\Control Tables\CBTC\rev 05.00"
                    r"\GWISIGIXL0401-05.00-ATT002 - Appendix L_Routes_Rev00.pdf"]
                self.control_tables_route.all_pages = [True, True]
                self.control_tables_route.specific_pages = [None, None]
                self.control_tables_overlap.control_tables_addr = [
                    r"C:\CBTC\PROJECTS\Glasgow\Control Tables\CBTC\rev 04.00"
                    r"\GWISIGIXL0400-04.00-ATT006 - Appendix F_Overlap_Rev00.pdf",
                    r"C:\CBTC\PROJECTS\Glasgow\Control Tables\CBTC\rev 05.00"
                    r"\GWISIGIXL0401-05.00-ATT007 - Appendix Q_Overlap_Rev00.pdf"]
                self.control_tables_overlap.all_pages = [True, True]
                self.control_tables_overlap.specific_pages = [None, None]
            # -- IXL Approach Zone -- #
            if cbtc:
                self.ixl_apz.ixl_apz_file = r"C:\CBTC\PROJECTS\Glasgow\IXL_APZ.xlsx"
                self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
                self.ixl_apz.start_line = 2
                self.ixl_apz.sig_column = "B"
                self.ixl_apz.apz_start_column = 3
                self.ixl_apz.apz_nb_columns = 6

        # ------------------------------- Lima ML2 -------------------------------#
        elif project_name == Projects.Lima_ML2:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Lima ML2\ML2_C_D470_DB0403RC1\DC_SYS_0403RC1.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\Lima ML2\ML2_C_D470_DB0403RC1\DC_PAR_0402RC1.xls"
            self.dc_bop_addr = r"C:\CBTC\PROJECTS\Lima ML2\ML2_C_D470_DB0403RC1\DC_BOP.xls"
            self.kit_c11_dir = r"C:\CBTC\PROJECTS\Lima ML2\ML2_C11_D470_06_06_00_V04_DB0403RC1"
            # -- Survey -- #
            self.survey_loc.survey_addr = [
                r"C:\CBTC\PROJECTS\Lima ML2\[B20] AFS Survey - Medicion de puntos topograficos en rieles- ML-L2"
                r"\Depot\Anexos de Informe 02-012021\METRO_LINEA2 DIC. 2020_modified.xls",
                r"C:\CBTC\PROJECTS\Lima ML2\[B20] AFS Survey - Medicion de puntos topograficos en rieles- ML-L2"
                r"\MainLine\Anexos de informe 03-022021\LIMA L2 E1A - OBJECTS LIST-ENERO 2021_via_reversed.xls",
                r"C:\CBTC\PROJECTS\Lima ML2\[B20] AFS Survey - Medicion de puntos topograficos en rieles- ML-L2"
                r"\Objects_List - v3 Rev 01_via_reversed.xlsx"]
            self.survey_loc.survey_sheet = [r"", r"Object List", r"Object List"]
            self.survey_loc.all_sheets = [True, False, False]
            self.survey_loc.start_row = [4, 4, 2]
            self.survey_loc.ref_col = [1, 2, 1]
            self.survey_loc.type_col = [3, 4, 3]
            self.survey_loc.track_col = [4, 5, 4]
            self.survey_loc.survey_kp_col = [13, 7, 6]
            # -- Control Tables -- #
            self.control_tables_config_ini_file = "control_tables_configuration_ml2.ini"
            self.control_tables_route.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Lima ML2\CONTROL TABLES"
                r"\B20X.0100002.L02.01ES-03.00-LINE 2 CONTROL TABLES - PHASE 1A"
                r"\ML2-AST-01A-A-025-GRAL-SSIXL-DIS-CD-4125-51-002.pdf",
                r"C:\CBTC\PROJECTS\Lima ML2\CONTROL TABLES"
                r"\B20X.0100002.L02.00ES-03.00-DEPOT CONTROL TABLES - PHASE 1A"
                r"\ML2-AST-01A-A-025-GRAL-SSIXL-DIS-CD-4126-51-002.pdf"]
            self.control_tables_route.all_pages = [True, True]
            self.control_tables_route.specific_pages = [None, None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Lima ML2\CONTROL TABLES"
                r"\B20X.0100002.L02.01ES-03.00-LINE 2 CONTROL TABLES - PHASE 1A"
                r"\ML2-AST-01A-A-025-GRAL-SSIXL-DIS-CD-4125-51-006.pdf",
                r"C:\CBTC\PROJECTS\Lima ML2\CONTROL TABLES"
                r"\B20X.0100002.L02.00ES-03.00-DEPOT CONTROL TABLES - PHASE 1A"
                r"\ML2-AST-01A-A-025-GRAL-SSIXL-DIS-CD-4126-51-006.pdf"]
            self.control_tables_overlap.all_pages = [True, True]
            self.control_tables_overlap.specific_pages = [None, None]

        # ------------------------------- Milan ML4 -------------------------------#
        elif project_name == Projects.Milan_ML4:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Milan ML4\4. WHOLE\ML4_WH_C_D470_V03_03_RC2\ML4_DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\Milan ML4\4. WHOLE\ML4_WH_C_D470_V03_03_RC2\ML4_DC_PAR.xls"
            self.dc_bop_addr = r"C:\CBTC\PROJECTS\Milan ML4\4. WHOLE\ML4_WH_C_D470_V03_03_RC2\DC_BOP.xls"
            self.kit_c11_dir = r"C:\CBTC\PROJECTS\Milan ML4\4. WHOLE\ML4_WH_C11_D470_06_06_02_V08"
            self.fouling_point_addr = (
                r"C:\CBTC\PROJECTS\Milan ML4\4. WHOLE\Fouling Point ML4_WH_C_D470_V03_01_RC3.xlsx")
            # -- Survey -- #
            self.survey_loc.survey_addr = [
                r"C:\CBTC\PROJECTS\Milan ML4\SURVEY\(ML4) LN04_Object_List_01_return28.03.24.xlsx",
                r"C:\CBTC\PROJECTS\Milan ML4\SURVEY\ML4_TF2 REPORT OBJECT_AFS_REV_5.1.xlsx",
                r"C:\CBTC\PROJECTS\Milan ML4\SURVEY\ML4_TF3 AFS DB integration template.xlsx",
                r"C:\CBTC\PROJECTS\Milan ML4\SURVEY\ml4 tki_depot_ln01_object.xlsx",
                r"C:\CBTC\PROJECTS\Milan ML4\SURVEY\ML4_LN02 - Coni Zugna to Sforza AFS Object List.xlsx"]
            self.survey_loc.all_sheets = [False, False, False, False, False, False]
            self.survey_loc.survey_sheet = ["Object_List_LN04",
                                            "Foglio1",
                                            "Import",
                                            "ML4 TKI_Depot_LN01_Object_List_",
                                            "AFS Coni Zugna to Sforza"]
            self.survey_loc.start_row = [2, 3, 3, 2, 2]
            self.survey_loc.ref_col = [1, 2, 1, 1, 1]
            self.survey_loc.type_col = [2, 1, 2, 2, 2]
            self.survey_loc.track_col = [3, 4, 3, 3, 3]
            self.survey_loc.survey_kp_col = [5, 7, 4, 5, 5]
            # -- Control Tables -- #
            self.control_tables_config_ini_file = "control_tables_configuration_ml4.ini"
            self.control_tables_route.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Milan ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf",
                r"C:\CBTC\PROJECTS\Milan ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf",
                r"C:\CBTC\PROJECTS\Milan ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf"]
            self.control_tables_route.all_pages = [False, False, False]
            self.control_tables_route.specific_pages = [(6, 160), (368, 521), (794, 935)]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Milan ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf",
                r"C:\CBTC\PROJECTS\Milan ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf",
                r"C:\CBTC\PROJECTS\Milan ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf"]
            self.control_tables_overlap.all_pages = [False, False, False]
            self.control_tables_overlap.specific_pages = [(316, 324), (676, 731), (1078, 1124)]
            # -- IXL Approach Zone -- #
            self.ixl_apz.ixl_apz_file = r"C:\CBTC\PROJECTS\Milan ML4\4. WHOLE\ML4_IXL_APZ.xlsx"
            self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
            self.ixl_apz.start_line = 2
            self.ixl_apz.sig_column = "B"
            self.ixl_apz.apz_start_column = 6
            self.ixl_apz.apz_nb_columns = 3

        # ------------------------------- Panama -------------------------------#
        elif project_name == Projects.Panama:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Panama\PAN_C_D470_08_03_01_V04_R2\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\Panama\PAN_C_D470_08_03_01_V04_R2\DC_PAR.xls"
            self.dc_bop_addr = r"C:\CBTC\PROJECTS\Panama\PAN_C_D470_08_03_01_V04_R2\C64_D413\DC_BOP.xls"
            # -- Control Tables -- #
            self.control_tables_route.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Panama\CONTROL TABLES\PAN.SIG.IXL.A07.56EN_02.00 – Annex2.pdf"]
            self.control_tables_route.all_pages = [True]
            self.control_tables_route.specific_pages = [None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Panama\CONTROL TABLES\PAN.SIG.IXL.A07.56EN_02.00 – Annex4.pdf"]
            self.control_tables_overlap.all_pages = [True]
            self.control_tables_overlap.specific_pages = [None]

        # ------------------------------- Riyadh RL3 -------------------------------#
        elif project_name == Projects.Riyadh_RL3:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Riyadh RL3\RL3_C_D470_09_02_RC3\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\Riyadh RL3\RL3_C_D470_09_02_RC3\DC_PAR.xls"
            self.dc_bop_addr = r"C:\CBTC\PROJECTS\Riyadh RL3\RL3_C_D470_09_02_RC3\DC_BOP.xls"
            self.kit_c11_dir = r"C:\CBTC\PROJECTS\Riyadh RL3\RL3_C11_D470_06_06_01_V04"
            # -- Survey -- #
            # self.block_def = r"C:\CBTC\PROJECTS\Riyadh RL3\CIRCUIT_DE_VOIE RL3.xls"
            self.survey_loc.survey_addr = r"C:\CBTC\PROJECTS\Riyadh RL3\Appendix K - RL3_D932_ed14.xls"
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3
            # -- Control Tables -- #
            self.control_tables_config_ini_file = r"control_tables_configuration_rl3.ini"
            self.control_tables_route.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3A1DPW-SSXL-ESP-000002-REV_J-Appendix B_Routes.pdf",
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3A1DPW-SSXL-ESP-000001-REV_M-AUTOMATIC AREA-Appendix H_Routes.pdf",
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3A1DPW-SSXL-ESP-000001-REV_M-MANUAL AREA-Appendix B_Routes.pdf",
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3K1DPE-SSXL-ESP-000003-REV_E-AUTOMATIC AREA-Appendix B_Routes.pdf",
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3K1DPE-SSXL-ESP-000003-REV_E-MANUAL AREA-Appendix I_Routes.pdf"]
            self.control_tables_route.all_pages = [True, True, True, True, True]
            self.control_tables_route.specific_pages = [None, None, None, None, None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3A1DPW-SSXL-ESP-000002-REV_J-Appendix E_Overlap.pdf",
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3A1DPW-SSXL-ESP-000001-REV_M-AUTOMATIC AREA-Appendix N_Overlap.pdf",
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3A1DPW-SSXL-ESP-000001-REV_M-MANUAL AREA-Appendix E_Overlap.pdf",
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3K1DPE-SSXL-ESP-000003-REV_E-AUTOMATIC AREA-Appendix E_Overlap.pdf",
                r"C:\CBTC\PROJECTS\Riyadh RL3\Control Tables"
                r"\M-ANM-3K1DPE-SSXL-ESP-000003-REV_E-MANUAL AREA-Appendix O_Overlap.pdf"]
            self.control_tables_overlap.all_pages = [True, True, True, True, True]
            self.control_tables_overlap.specific_pages = [None, None, None, None, None]

        # ------------------------------- Stockholm Red Line -------------------------------#
        elif project_name == Projects.Stockholm_Red_Line:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Stockholm Red Line\SL_D470_V08_08\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\Stockholm Red Line\SL_D470_V08_08\DC_PAR.xls"
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\Stockholm Red Line\CIRCUIT_DE_VOIE_DB_V08.08.xls"
            self.survey_loc.survey_addr = r"C:\CBTC\PROJECTS\Stockholm Red Line\SL_C_D932_02_00.xlsm"  # TODO switch N/R
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- Thessaloniki TSK -------------------------------#
        elif project_name == Projects.Thessaloniki_TSK:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Thessaloniki TSK\TSK_C_D470_07_03_03_V08_KLM\DC_SYS.xls"
            # self.dc_sys_addr = r"C:\CBTC\PROJECTS\Thessaloniki TSK\TSK_C_D470_07_03_03_V08_KLM\DC_SYS_patch_route.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\Thessaloniki TSK\TSK_C_D470_07_03_03_V08_KLM\DC_PAR.xls"
            self.dc_bop_addr = r"C:\CBTC\PROJECTS\Thessaloniki TSK\TSK_C_D470_07_03_03_V08_KLM\C64_D413\DC_BOP.xls"
            self.kit_c11_dir = r"C:\CBTC\PROJECTS\Thessaloniki TSK\TSK_C11_D470_07_03_03_V13"
            # self.kit_c11_sp_dir = r"C:\CBTC\PROJECTS\Thessaloniki TSK\TSK_C11_D470_07_03_03_V12_SP1"
            self.fouling_point_addr = (r"C:\CBTC\PROJECTS\Thessaloniki TSK"
                                       r"\Fouling Points TSK_C_D470_07_03_03_V02_RC3.xlsx")
            # -- Survey -- #
            self.survey_loc.survey_addr = [
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\SURVEY\1G00LV615R808A_EN_Annex_A.xlsx",
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\SURVEY\1G00LV615R808A_EN_Annex_B.xls",
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\SURVEY\1G00LV615R808A_EN_Annex_C.xlsx",
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\SURVEY\1G00LV615R808A_EN_Annex_D.xlsx",
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\SURVEY\AFS TSK Kalamaria V01(Survey evaluation)_130325_JA.xlsx"]
            self.survey_loc.survey_sheet = [r"TSK_Object_list_310720_ro", r"TSK_Object_list_REV.3",
                                            r"Φύλλο1", r"Φύλλο1", r"To be surveyed - Input for AFS"]
            self.survey_loc.all_sheets = [False, False, False, False, False]
            self.survey_loc.start_row = [2, 2, 3, 3, 2]
            self.survey_loc.ref_col = [1, 1, 13, 13, 2]
            self.survey_loc.type_col = [2, 2, 14, 14, 3]
            self.survey_loc.track_col = [3, 3, 15, 15, 4]
            self.survey_loc.survey_kp_col = [7, 7, 17, 17, 6]
            # -- Control Tables -- #
            self.control_tables_config_ini_file = r"control_tables_configuration_tsk.ini"
            self.control_tables_route.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\Control Tables rev 05.00\1G00LV601R721B_EN_ANNEX_B.pdf",
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\Control Tables rev 05.00\1G00LV601R722B_EN_ANNEX_B.pdf",
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\Control Tables KLM rev 03.00"
                r"\1GE0LV601R721A_EN_ANNEX_B - Routes.pdf"]
            self.control_tables_route.all_pages = [True, True, True]
            self.control_tables_route.specific_pages = [None, None, None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\Control Tables rev 05.00\1G00LV601R721B_EN_ANNEX_D.pdf",
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\Control Tables rev 05.00\1G00LV601R722B_EN_ANNEX_D.pdf",
                r"C:\CBTC\PROJECTS\Thessaloniki TSK\Control Tables KLM rev 03.00"
                r"\1GE0LV601R721A_EN_ANNEX_D - Overlaps.pdf"]
            self.control_tables_overlap.all_pages = [True, True, True]
            self.control_tables_overlap.specific_pages = [None, None, None]
            # -- IXL Approach Zone -- #
            self.ixl_apz.ixl_apz_file = r"C:\CBTC\PROJECTS\Thessaloniki TSK\TSK_IXL_APZ.xlsx"
            self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
            self.ixl_apz.start_line = 2
            self.ixl_apz.sig_column = "E"
            self.ixl_apz.apz_start_column = 6
            self.ixl_apz.apz_nb_columns = 2

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------- Other projects -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

        # --- OCTYS --- #

        # ------------------------------- OCTYS_L3 -------------------------------#
        elif project_name == Projects.OCTYS_L3:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\OCTYS\Ligne 3\L3C_O_D470_0417\DC_SYS_L3_04_17.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\OCTYS\Ligne 3\L3C_O_D470_0417\DC_PAR_L3.xls"

        # ------------------------------- OCTYS_L6 -------------------------------#
        elif project_name == Projects.OCTYS_L6:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\OCTYS\Ligne 6\OCTYS_L6C_D405-6_0502"
                                r"\DC_SYS_OCTYS_L6C_D405-6_0502.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\OCTYS\Ligne 6\OCTYS_L6C_D405-6_0502"
                                r"\DC_PAR_OCTYS_L6C_D405-6_0502.xls")

        # --- USA --- #

        # ------------------------------- Baltimore MTA -------------------------------#
        elif project_name == Projects.Baltimore_MTA:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\USA\Baltimore MTA\MTA_C_D470_03_01_RC0\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\USA\Baltimore MTA\MTA_C_D470_03_01_RC0\DC_PAR.xls"
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\USA\Baltimore MTA\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = r"C:\CBTC\PROJECTS\USA\Baltimore MTA\MTA_D932.xlsx"
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- BART -------------------------------#
        elif project_name == Projects.BART:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\USA\BART\BART_C_D470_08_03_01_V00\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\USA\BART\BART_C_D470_08_03_01_V00\DC_PAR.xls"
            self.dc_bop_addr = r"C:\CBTC\PROJECTS\USA\BART\BART_C_D470_08_03_01_V00\DC_BOP.xls"

        # ------------------------------- Hurontario HLR -------------------------------#
        elif project_name == Projects.Hurontario_HLR:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\USA\Hurontario HLR\HLR_C_D470_V_03_01_RC1\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\USA\Hurontario HLR\HLR_C_D470_V_03_01_RC1\DC_PAR.xls"

        # ------------------------------- Ontario OL RSSOM -------------------------------#
        elif project_name == Projects.Ontario_OL_RSSOM:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\USA\Ontario OL RSSOM\Mainline and deport early DB 00_01"
                                r"\Ontario_DB_00_01(mainline+deport).xls")

        # ------------------------------- SEPTA MSH -------------------------------#
        elif project_name == Projects.SEPTA_MSH:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\USA\SEPTA MSH\MSH_C_D470_06_06_01_V00\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\USA\SEPTA MSH\MSH_C_D470_06_06_01_V00\DC_PAR.xls"
            self.kit_c11_dir = r"C:\CBTC\PROJECTS\USA\SEPTA MSH\MSH_C11_D470_06_06_03_V00"
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\USA\SEPTA MSH\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = r"C:\CBTC\PROJECTS\USA\SEPTA MSH\Topo_V_06_00.xlsx"
            self.survey_loc.survey_sheet = None
            self.survey_loc.all_sheets = True
            self.survey_loc.start_row = 4
            self.survey_loc.ref_col = 2
            self.survey_loc.type_col = 1
            self.survey_loc.track_col = 3
            self.survey_loc.survey_kp_col = 5

        # --- India --- #

        # ------------------------------- Chennai CMRL -------------------------------#
        elif project_name == Projects.Chennai_CMRL:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL\CMRL_S1_C_D470_08_03_01_V04_01\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL\CMRL_S1_C_D470_08_03_01_V04_01\DC_PAR.xls"
            self.dc_bop_addr = (r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL\CMRL_S1_C_D470_08_03_01_V04_01"
                                r"\C64_D413\DC_BOP.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL\C_D470_08_03_01_V04_01_Blocks_Definition_v2.xlsx"
            self.survey_loc.survey_addr = r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL\Survey\AppendixA_Input File.xlsx"
            self.survey_loc.survey_sheet = None
            self.survey_loc.all_sheets = True
            self.survey_loc.start_row = 4
            self.survey_loc.ref_col = 3
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 5
            self.survey_loc.survey_kp_col = 8
            # -- Control Tables -- #
            self.control_tables_config_ini_file = r"control_tables_configuration_cmrl.ini"
            self.control_tables_route.control_tables_addr = [
                (r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL\CONTROL TABLES"
                 r"\CMRL-14057-03.00-STAGE 1 Annexure B_Route_Control_Table.pdf"),
                (r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL\CONTROL TABLES"
                 r"\CMRL-14093-05.00-POONAMALLEE DEPOT Annexure B_Route_Control_Table.pdf"),
            ]
            self.control_tables_route.all_pages = [True, True]
            self.control_tables_route.specific_pages = [None, None]
            self.control_tables_overlap.control_tables_addr = [
                (r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL\CONTROL TABLES"
                 r"\CMRL-14057-03.00-STAGE 1 Annexure F_Overlap_Control_Table.pdf"),
                (r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL\CONTROL TABLES"
                 r"\CMRL-14093-05.00-POONAMALLEE DEPOT Annexure E_Overlap_Control_Table.pdf"),
            ]
            self.control_tables_overlap.all_pages = [True, True]
            self.control_tables_overlap.specific_pages = [None, None]
            # -- IXL Approach Zone -- #
            self.ixl_apz.ixl_apz_file = (r"C:\CBTC\PROJECTS\INDIA\Chennai CMRL"
                                         r"\IXL_APZ_CMRL-16061_INSTANTIATED CBTC - IXL ICDD_rev01.02.xlsx")
            self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
            self.ixl_apz.start_line = 2
            self.ixl_apz.sig_column = "A"
            self.ixl_apz.apz_start_column = 3
            self.ixl_apz.apz_nb_columns = 3

        # ------------------------------- Kolkata KMRC -------------------------------#
        elif project_name == Projects.Kolkata_KMRC:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\INDIA\Kolkata KMRC\KMRC_PH2_C_D470_00_RC07\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\INDIA\Kolkata KMRC\KMRC_PH2_C_D470_00_RC07\DC_PAR.xls"
            self.kit_c11_dir = (r"C:\CBTC\PROJECTS\INDIA\Kolkata KMRC"
                                r"\KMRC_PH2_C11_D470_06_03_05_V05\Project_CC_CORE")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\INDIA\Kolkata KMRC\CIRCUIT_DE_VOIE_KMRC_PH2.xls"
            self.survey_loc.survey_addr = [
                r"C:\CBTC\PROJECTS\INDIA\Kolkata KMRC"
                r"\KMRC-76054_Rev01_C_D932 - Advanced field survey report.xlsm",
                r"C:\CBTC\PROJECTS\INDIA\Kolkata KMRC"
                r"\KMRC-26054_Rev09_C_D932 - Advanced field survey report.xlsm"]
            self.survey_loc.survey_sheet = [r"Result Final", r"KMRC-PH2A"]
            self.survey_loc.all_sheets = [False, False]
            self.survey_loc.start_row = [2, 2]
            self.survey_loc.ref_col = [1, 2]
            self.survey_loc.type_col = [4, 6]
            self.survey_loc.track_col = [2, 4]
            self.survey_loc.survey_kp_col = [3, 5]

        # ------------------------------- Navi-Mumbai NMML1 -------------------------------#
        elif project_name == Projects.NaviMumbai_NMML1:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\INDIA\Navi-Mumbai NMML1\NMML1_PH2_C_D470_00_00_RC9\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\INDIA\Navi-Mumbai NMML1\NMML1_PH2_C_D470_00_00_RC9\DC_PAR.xls"
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\INDIA\Navi-Mumbai NMML1\CIRCUIT_DE_VOIE_NMML1.xls"
            self.survey_loc.survey_addr = (
                r"C:\CBTC\PROJECTS\INDIA\Navi-Mumbai NMML1\NMML1_C_D932_Line1_Advanced_field_survey_report.xlsm")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 5

        # ------------------------------- Noida NS01 -------------------------------#
        elif project_name == Projects.Noida_NS01:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\INDIA\Noida NS01\NS01_C_D470_18_00_RC1\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\INDIA\Noida NS01\NS01_C_D470_18_00_RC1\DC_PAR.xls"
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\INDIA\Noida NS01\CIRCUIT_DE_VOIE_NS01.xls"
            self.survey_loc.survey_addr = (
                r"C:\CBTC\PROJECTS\INDIA\Noida NS01"
                r"\NS01-L-SIG-9-0001 NS01_C_D932 - Advanced field survey report_06.00.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # --- China --- #

        # ------------------------------- Sanying SYL -------------------------------#
        elif project_name == Projects.Sanying_SYL:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\CHINA\Sanying SYL\SYL_C_D470_02_09\DC_SYS_02_09.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\CHINA\Sanying SYL\SYL_C_D470_02_09\DC_PAR.xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\Sanying SYL"
                                           r"\SYL_D932_export_DB0200_20250817 r1.xlsx")
            self.survey_loc.survey_sheet = r"D932"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 2
            self.survey_loc.track_col = 3
            self.survey_loc.survey_kp_col = 15

        # ------------------------------- Taipei TC1 -------------------------------#
        elif project_name == Projects.Taipei_TC1:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\CHINA\Taipei TC1\TC1_C_D470_06_00_RC14\DC_SYS.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\CHINA\Taipei TC1\TC1_C_D470_06_00_RC14\DC_PAR.xls"
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\Taipei TC1\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = [
                r"C:\CBTC\PROJECTS\CHINA\Taipei TC1\Survey\TC1_D932_Depot_20190221.xlsx",
                r"C:\CBTC\PROJECTS\CHINA\Taipei TC1\Survey"
                r"\TC1_Mainline_AFS_object_list_draft_J20180720_vs_cmts_20180817_R1_vs_mod_20181212.xlsx",
                r"C:\CBTC\PROJECTS\CHINA\Taipei TC1\Survey\901_軌.xlsx"]
            self.survey_loc.survey_sheet = [r"Depot", r"Mainline ", r"工作表1"]
            self.survey_loc.all_sheets = [False, False, False]
            self.survey_loc.start_row = [2, 2, 2]
            self.survey_loc.ref_col = [1, 1, 7]
            self.survey_loc.type_col = [4, 5, 9]
            self.survey_loc.track_col = [2, 2, 8]
            self.survey_loc.survey_kp_col = [3, 3, 11]

        # ------------------------------- Wenzhou WZS1 -------------------------------#
        elif project_name == Projects.Wenzhou_WZS1:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\CHINA\Wenzhou WZS1\WZS1_C_D470_08_07\DC_SYS_0807.xls"
            self.dc_par_addr = r"C:\CBTC\PROJECTS\CHINA\Wenzhou WZS1\WZS1_C_D470_08_07\DC_PAR_0807.xls"
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\Wenzhou WZS1\WZS1_C_D470_08_01\CIRCUIT_DE_VOIE_Corrected.xls"
            self.survey_loc.survey_addr = (
                r"C:\CBTC\PROJECTS\CHINA\Wenzhou WZS1\WZ_S1P1_SIG_DB_D932_1409_D932_V1.8_modified.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # --- China V4 --- #

        # ------------------------------- Chengdu CDL1 -------------------------------#
        elif project_name == Projects.Chengdu_CDL1:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL1"
                                r"\CDL1_C_D470_13_04\DC_SYS_CDL1_13_04.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL1"
                                r"\CDL1_C_D470_13_04\DC_PAR_CDL1_13_04.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL1\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL1\CDL1_C_D932_03_08.xlsx"
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- Chengdu CDL2 -------------------------------#
        elif project_name == Projects.Chengdu_CDL2:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL2"
                                r"\CDL2_C_D470_07_02\CDL2_DC_SYS_07_02.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL2"
                                r"\CDL2_C_D470_07_02\CDL2_DC_PAR_07_02.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL2\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL2\CDL2_C_D932_01 10.xlsx"
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- Chengdu CDL6 -------------------------------#
        elif project_name == Projects.Chengdu_CDL6:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL6"
                                r"\CDL6_C_D470_02_02\DC_SYS_CDL6_V02_02.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL6"
                                r"\CDL6_C_D470_02_02\DC_PAR_CDL6_V02_02.xls")

        # ------------------------------- Chengdu CDL10 -------------------------------#
        elif project_name == Projects.Chengdu_CDL10:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL10"
                                r"\CDL10_C_D470_05_03\DC_SYS_CDL10_05_03.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL10"
                                r"\CDL10_C_D470_05_03\DC_PAR_CDL10_05_02.xls")
            # -- Survey -- #
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Chengdu CDL10"
                                           r"\CD_L10_SIG_DB_D932_1409_V1.6_20170502.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- Dalian DLL1 -------------------------------#
        elif project_name == Projects.Dalian_DLL1:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL1"
                                r"\DLL1_C_D470_02_02\DC_SYS_02_00.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL1"
                                r"\DLL1_C_D470_02_02\DC_PAR_02_00.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL1\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL1"
                                           r"\DL_L1_SIG_DB_D932_1409_V2.1_20161204.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- Dalian DLL2 -------------------------------#
        elif project_name == Projects.Dalian_DLL2:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL2"
                                r"\DLL2_C_D470_04_04\DC_SYS_DLL2_04_04.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL2"
                                r"\DLL2_C_D470_04_04\DC_PAR_DLL2_04_04.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL2\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL2"
                                           r"\DL_L2_SIG_DB_D932_1409_V1.6_20150202.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- Dalian DLL3 -------------------------------#
        elif project_name == Projects.Dalian_DLL3:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL3"
                                r"\DLL3_C_D470_02_00\DC_SYS_DLL3_02_00.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian DLL3"
                                r"\DLL3_C_D470_02_00\DC_PAR_DLL3_02_00.xls")

        # ------------------------------- Dalian JinPu DLJP -------------------------------#
        elif project_name == Projects.Dalian_JinPu_DLJP:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian JinPu DLJP"
                                r"\DLJP_C_D470_02_00\DC_SYS_DLJP_02_00.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Dalian JinPu DLJP"
                                r"\DLJP_C_D470_02_00\DC_PAR_DLJP_02_00.xls")

        # ------------------------------- HangShao HSL -------------------------------#
        elif project_name == Projects.HangShao_HSL:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\HangShao HSL"
                                r"\HSL_C_D470_01_02\DC_SYS_HSL_0102.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\HangShao HSL"
                                r"\HSL_C_D470_01_02\DC_PAR_HSL_0102.xls")

        # ------------------------------- Hangzhou HZL1 -------------------------------#
        elif project_name == Projects.Hangzhou_HZL1:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL1"
                                r"\HZL1_C_D470_08_04\DC_SYS_HZL1_08_04.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL1"
                                r"\HZL1_C_D470_08_04\DC_PAR_HZL1_08_04.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL1\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL1"
                                           r"\HZL1_C_D932_00_10_09.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- Hangzhou HZL2 -------------------------------#
        elif project_name == Projects.Hangzhou_HZL2:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL2"
                                r"\HZL2_C_D470_07_01\DC_SYS_HZL2_0701.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL2"
                                r"\HZL2_C_D470_07_01\DC_PAR_HZL2_0701.xls")
            # -- Survey -- #
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL2"
                                           r"\HZ_L2_SIG_DB_D932_1409_V1.7_20171229.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- Hangzhou HZL4 -------------------------------#
        elif project_name == Projects.Hangzhou_HZL4:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL4"
                                r"\HZL4_C_D470_05_02\DC_SYS_HZL4_05_01.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL4"
                                r"\HZL4_C_D470_05_02\DC_PAR_HZL4_05_01.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL4\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL4"
                                           r"\HZL4_SIG_DB_D932_1409_V1.6_20171019.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- Hangzhou HZL9 -------------------------------#
        elif project_name == Projects.Hangzhou_HZL9:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL9"
                                r"\HZL9_C_D470_02_02\DC_SYS_HZL9_02_02.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Hangzhou HZL9"
                                r"\HZL9_C_D470_02_02\DC_PAR_HZL9_02_02.xls")

        # ------------------------------- Shaoxing SXL1 -------------------------------#
        elif project_name == Projects.Shaoxing_SXL1:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shaoxing SXL1"
                                r"\SXL1_C_D470_03_02\DC_SYS_SXL1_03_02.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shaoxing SXL1"
                                r"\SXL1_C_D470_03_02\DC_PAR_SXL1_03_02.xls")

        # ------------------------------- Shenyang SHYL1 -------------------------------#
        elif project_name == Projects.Shenyang_SHYL1:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL1"
                                r"\SYL1_C_D470_V10_00\DC_SYS_SHYL1_10_00.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL1"
                                r"\SYL1_C_D470_V10_00\DC_PAR_SHYL1_10_00.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL1\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL1"
                                           r"\SY_L1_SIG_DB_D932_1409_V3.3_2016_5_11.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # ------------------------------- Shenyang SHYL2 -------------------------------#
        elif project_name == Projects.Shenyang_SHYL2:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL2"
                                r"\SYL2_C_D470_08_04\DC_SYS_SYL2_V08_04.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL2"
                                r"\SYL2_C_D470_08_04\DC_PAR_SYL2_V08_04.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL2\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL2"
                                           r"\SYL2_C_D932_17_09_28.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # ------------------------------- Shenyang SHYL10 -------------------------------#
        elif project_name == Projects.Shenyang_SHYL10:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL10"
                                r"\SYL10_C_D470_01_00\DC_SYS_SYL10_01_00.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Shenyang SHYL10"
                                r"\SYL10_C_D470_01_00\DC_PAR_SYL10_01_00.xls")

        # ------------------------------- Tianjin TJL5 -------------------------------#
        elif project_name == Projects.Tianjin_TJL5:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Tianjin TJL5"
                                r"\TJL5_C_D470_02_01\DC_SYS_TJL5_02_01.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Tianjin TJL5"
                                r"\TJL5_C_D470_02_01\DC_PAR_TJL5_02_01.xls")
            # -- Survey -- #
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Tianjin TJL5"
                                           r"\TJ_L5_SIG_DB_D932_1409_V1.9_20181012.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # ------------------------------- Xian XAL2 -------------------------------#
        elif project_name == Projects.Xian_XAL2:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Xian XAL2"
                                r"\XAL2_C_D470_10_03\DC_SYS_XAL2_10_03.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Xian XAL2"
                                r"\XAL2_C_D470_10_03\DC_PAR_XAL2_10_03.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Xian XAL2\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Xian XAL2"
                                           r"\ASTS_Modified_XAL2_C_D932_2014_04_08.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # ------------------------------- Zhengzhou ZZL1 -------------------------------#
        elif project_name == Projects.Zhengzhou_ZZL1:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Zhengzhou ZZL1"
                                r"\ZZL1_C_D470_05_02\DC_SYS_ZZL1_V05_02.xls")
            self.dc_par_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Zhengzhou ZZL1"
                                r"\ZZL1_C_D470_05_02\DC_PAR_ZZL1_05_02.xls")
            # -- Survey -- #
            self.block_def = r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Zhengzhou ZZL1\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\CBTC\PROJECTS\CHINA\CHINA V4\Zhengzhou ZZL1"
                                           r"\ZZ_L1_SIG_DB_D932_1409_V2.3_20170815.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # --- DB CORE --- #

        # ------------------------------- DB_CORE_4_8_0_0 -------------------------------#
        elif project_name == Projects.DB_CORE_4_8_0_0:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\Core_C_D470"
                                r"\core_c_d470-CORE_C_D470_V_4_8_0_0\DC_SYS.xls")

        # ------------------------------- DB_CORE_6_3_5_0 -------------------------------#
        elif project_name == Projects.DB_CORE_6_3_5_0:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\Core_C_D470"
                                r"\core_c_d470-CORE_C_D470_V_6_3_5_0\DC_SYS.xls")

        # ------------------------------- DB_CORE_6_6_0_2 -------------------------------#
        elif project_name == Projects.DB_CORE_6_6_0_2:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\Core_C_D470"
                                r"\core_c_d470-CORE_C_D470_V_6_6_0_2\DC_SYS.xls")

        # ------------------------------- DB_CORE_7_3_3_0 -------------------------------#
        elif project_name == Projects.DB_CORE_7_3_3_0:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\Core_C_D470"
                                r"\core_c_d470-CORE_C_D470_V_7_3_3_0\DC_SYS.xls")

        # ------------------------------- DB_CORE_7_4_0_0 -------------------------------#
        elif project_name == Projects.DB_CORE_7_4_0_0:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\Core_C_D470"
                                r"\core_c_d470-CORE_C_D470_V_7_4_0_0\DC_SYS.xls")

        # ------------------------------- DB_CORE_72_1_4_0 -------------------------------#
        elif project_name == Projects.DB_CORE_72_1_4_0:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\Core_C_D470"
                                r"\core_c_d470-CORE_C_D470_V_72_1_4_0\DC_SYS.xls")

        # ------------------------------- DB_CORE_72_2_1_0 -------------------------------#
        elif project_name == Projects.DB_CORE_72_2_1_0:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\Core_C_D470"
                                r"\core_c_d470-CORE_C_D470_V_72_2_1_0\DC_SYS.xls")

        # ------------------------------- DB_CORE_8_3_1_0 -------------------------------#
        elif project_name == Projects.DB_CORE_8_3_1_0:
            self.dc_sys_addr = (r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\Core_C_D470"
                                r"\core_c_d470-CORE_C_D470_V_8_3_1_0\DC_SYS.xls")

        # --- Mock-up --- #

        # ------------------------------- Mock-up 1 -------------------------------#
        elif project_name == Projects.Mock_up:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\DC_SYS_mock-up.xls"

        # ------------------------------- Mock-up 2 -------------------------------#
        elif project_name == Projects.Mock_up_2:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\DC_SYS_mock-up2.xls"

        # ------------------------------- Mock-up 3 -------------------------------#
        elif project_name == Projects.Mock_up_3:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\DC_SYS_mock-up3.xls"

        # ------------------------------- Mock-up 4 -------------------------------#
        elif project_name == Projects.Mock_up_4:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\DC_SYS_mock-up4.xls"

        # ------------------------------- Mock-up 5 -------------------------------#
        elif project_name == Projects.Mock_up_5:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\DC_SYS_mock-up5.xls"

        # ------------------------------- Mock-up 6 -------------------------------#
        elif project_name == Projects.Mock_up_6:
            self.dc_sys_addr = r"C:\CBTC\PROJECTS\Mock-Up DC_SYS\DC_SYS_mock-up6.xls"

    def reset(self):
        self.cctool_oo_schema = r""
        self.dc_sys_addr = r""
        self.dc_sys_addr_old = r""
        self.dc_par_addr = r""
        self.dc_bop_addr = r""
        self.block_def = None
        self.survey_loc = self.SurveyLocation()
        self.kit_c11_dir = r""
        self.kit_c11_sp_dir = r""
        self.kit_c121_d470_dir = r""
        self.control_tables_route = self.ControlTablesLocation()
        self.control_tables_overlap = self.ControlTablesLocation()
        self.control_tables_config_ini_file = r"control_tables_configuration.ini"
        self.ixl_apz = self.IxlApz()
        self.fouling_point_addr = r""


DATABASE_LOCATION = ProjectDatabaseLocation(PROJECT_NAME)
