#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["DatabaseLocation", "Projects"]


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
    OCTYS_L12 = "OCTYS_L12"

    Baltimore_MTA = "Baltimore_MTA"
    BART = "BART"
    Hurontario_HLR = "Hurontario_HLR"
    MSH_SEPTA = "MSH_SEPTA"
    Ontario_OL_RSSOM = "Ontario_OL_RSSOM"

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


class DatabaseLocation:
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
