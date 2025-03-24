#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["DATABASE_LOC"]


class Projects:
    Ankara_L1 = "Ankara_L1"
    Ankara_L2 = "Ankara_L2"
    Brussels_P1B0 = "Brussels_P1B0"
    Brussels_P1B2 = "Brussels_P1B2"
    Copenhagen = "Copenhagen"
    Glasgow_IATP = "Glasgow_IATP"
    Glasgow_CBTC = "Glasgow_CBTC"
    Lima = "Lima"
    Milan = "Milan"
    Panama = "Panama"
    Riyadh = "Riyadh"
    Thessaloniki = "Thessaloniki"

    OCTYS_L6 = "OCTYS_L6"

    Baltimore = "Baltimore"
    BART = "BART"
    Chennai_CMRL = "Chennai_CMRL"
    Hurontario = "Hurontario"
    MSH = "MSH"
    KMRC = "KMRC"
    NMML1 = "NMML1"
    Noida = "Noida"
    Shenyang = "Shenyang"
    Taipei = "Taipei"
    Wenzhou = "Wenzhou"
    Mock_up = "Mock-up"
    Mock_up_2 = "Mock-up 2"
    Mock_up_3 = "Mock-up 3"
    Mock_up_4 = "Mock-up 4"
    Mock_up_5 = "Mock-up 5"


# --- Main projects --- #
# PROJECT_NAME = Projects.Ankara_L1
# PROJECT_NAME = Projects.Ankara_L2
# PROJECT_NAME = Projects.Brussels_P1B0
# PROJECT_NAME = Projects.Brussels_P1B2
# PROJECT_NAME = Projects.Copenhagen
# PROJECT_NAME = Projects.Glasgow_IATP
# PROJECT_NAME = Projects.Glasgow_CBTC
# PROJECT_NAME = Projects.Lima
# PROJECT_NAME = Projects.Milan  # TODO manage R_S01_0102_202 in route verif
# PROJECT_NAME = Projects.Panama
# PROJECT_NAME = Projects.Riyadh
PROJECT_NAME = Projects.Thessaloniki

# --- OCTYS --- #
# PROJECT_NAME = Projects.OCTYS_L6

# --- USA --- #
# PROJECT_NAME = Projects.Baltimore
# PROJECT_NAME = Projects.BART
# PROJECT_NAME = Projects.Hurontario
# PROJECT_NAME = Projects.MSH

# --- India --- #
# PROJECT_NAME = Projects.Chennai_CMRL
# PROJECT_NAME = Projects.KMRC
# PROJECT_NAME = Projects.NMML1
# PROJECT_NAME = Projects.Noida

# --- China --- #
# PROJECT_NAME = Projects.Shenyang
# PROJECT_NAME = Projects.Taipei
# PROJECT_NAME = Projects.Wenzhou

# --- Mock-up --- #
# PROJECT_NAME = Projects.Mock_up
# PROJECT_NAME = Projects.Mock_up_2
# PROJECT_NAME = Projects.Mock_up_3
# PROJECT_NAME = Projects.Mock_up_4
# PROJECT_NAME = Projects.Mock_up_5


class ProjectDatabaseLoc:
    class ControlTablesLoc:
        control_tables_addr = []
        all_pages = []
        specific_pages = []

    class SurveyLoc:
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
    survey_loc = SurveyLoc()
    kit_c11_dir = r""
    kit_c11_sp_dir = r""
    kit_c121_d470_dir = r""
    control_tables_route = ControlTablesLoc()
    control_tables_overlap = ControlTablesLoc()
    control_tables_config_ini_file = r"control_tables_configuration.ini"
    ixl_apz = IxlApz()
    fouling_point_addr = r""

    def __init__(self, project_name: str):

        # ------------------------------- Ankara_L1 -------------------------------#
        if project_name == Projects.Ankara_L1:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L1\ANK_L1_C_D470_V12_05_RC2\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L1\ANK_L1_C_D470_V12_05_RC2\DC_PAR.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\Ank\ANK_L1\circuitdevoie.xlsx"
            self.survey_loc.survey_addr = (
                r"C:\Users\naderc\Desktop\Ank\SURVEY\ANK_L1_C_D932_14_00_RC1.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # ------------------------------- Ankara_L2 -------------------------------#
        if project_name == Projects.Ankara_L2:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L2\ANK_L2_C_D470_V06_00_RC4\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L2\ANK_L2_C_D470_V06_00_RC4\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L2\ANK_L2_C_D470_V06_00_RC4\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\Ank\ANK_L2\ANK_L2_C11_D470_06_05_03_V07"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\Ank\ANK_L2\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = [
                r"C:\Users\naderc\Desktop\Ank\SURVEY\ANK_L2_C_D932_01_00_RC2.xlsx",
                r"C:\Users\naderc\Desktop\Ank\SURVEY"
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
                r"C:\Users\naderc\Desktop\Ank\Control Tables\B20AC0500161315E_04_01 - Route L2.pdf"]
            self.control_tables_route.all_pages = [False]
            self.control_tables_route.specific_pages = [(24, 104)]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\Users\naderc\Desktop\Ank\Control Tables\B20AC0500161316E_04_01 - Overlap L2.pdf"]
            self.control_tables_overlap.all_pages = [False]
            self.control_tables_overlap.specific_pages = [(18, 93)]

        # ------------------------------- Brussels -------------------------------#
        elif project_name.startswith("Brussels"):
            phase_1b0 = project_name == Projects.Brussels_P1B0
            phase_1b2 = project_name == Projects.Brussels_P1B2
            if phase_1b0:
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_04_V09_P1B0_R2\DC_SYS.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_04_V09_P1B0_R2\DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_04_V09_P1B0_R2\C64_D413\DC_BOP.xls"
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\BXL\BXL_C11_D470_72_01_04_V09_P1B0_R2"
                self.fouling_point_addr = r"C:\Users\naderc\Desktop\BXL\fouling_point_fd_checking_1b0.xlsx"
                # -- Survey -- #
                self.survey_loc.survey_addr = [
                    r"C:\Users\naderc\Desktop\BXL\BXL_Photobook_survey.xlsx",
                    r"C:\Users\naderc\Desktop\BXL\AFS_BXL_1B0.xlsx"]
                # -- Control Tables -- #
                self.control_tables_config_ini_file = "control_tables_configuration_bxl.ini"
                self.control_tables_route.control_tables_addr = [
                    r"C:\Users\naderc\Desktop\BXL\CONTROL TABLES\Control Tables Erasme Antenna 90000534.L02.FR 04.00"
                    r"\90000536.L02.FR-BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_rev03.01.pdf",
                    r"C:\Users\naderc\Desktop\BXL\CONTROL TABLES\Control Tables Erasme Depot 90000527.L02.FR 04.00"
                    r"\90000528.L02.FR-BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_rev03.00.pdf"]
                self.control_tables_route.all_pages = [True, True]
                self.control_tables_route.specific_pages = [None, None]
                self.control_tables_overlap.control_tables_addr = [
                    r"C:\Users\naderc\Desktop\BXL\CONTROL TABLES\Control Tables Erasme Antenna 90000534.L02.FR 04.00"
                    r"\90000537.L02.FR-BXL_IXL_ LISTE DES OVERLAP + PARAMÈTRES OVERLAP_FR_rev03.01.pdf",
                    r"C:\Users\naderc\Desktop\BXL\CONTROL TABLES\Control Tables Erasme Depot 90000527.L02.FR 04.00"
                    r"\90000530.L02.FR-BXL_IXL_LISTE DES OVERLAP + PARAMÈTRES OVERLAP_FR_rev02.00.pdf"]
                self.control_tables_overlap.all_pages = [True, True]
                self.control_tables_overlap.specific_pages = [None, None]
                # -- IXL Approach Zone -- #
                self.ixl_apz.ixl_apz_file = r"C:\Users\naderc\Desktop\BXL\BXL_IXL_APZ.xlsx"
                self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
                self.ixl_apz.start_line = 2
                self.ixl_apz.sig_column = "A"
                self.ixl_apz.apz_start_column = 9
                self.ixl_apz.apz_nb_columns = 5
            elif phase_1b2:
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\BXL\PHASE 1B2\BXL_C_D470_72_02_01_V01_P1B2_R2\DC_SYS.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\BXL\PHASE 1B2\BXL_C_D470_72_02_01_V01_P1B2_R2\DC_PAR.xls"
                self.dc_bop_addr = (r"C:\Users\naderc\Desktop\BXL\PHASE 1B2\BXL_C_D470_72_02_01_V01_P1B2_R2"
                                    r"\C64_D413\DC_BOP.xls")
                # -- Survey -- #
                self.survey_loc.survey_addr = [
                    r"C:\Users\naderc\Desktop\BXL\BXL_Photobook_survey_1B2.xlsx",
                    r"C:\Users\naderc\Desktop\BXL\AFS_BXL_1B0.xlsx"]
                # -- Control Tables -- #
                self.control_tables_config_ini_file = "control_tables_configuration_bxl.ini"
                self.control_tables_route.control_tables_addr = [
                    r"C:\Users\naderc\Desktop\BXL\PHASE 1B2\CONTROL TABLES"
                    r"\90000528.L02.FR-BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_rev03.00.pdf",
                    r"C:\Users\naderc\Desktop\BXL\PHASE 1B2\CONTROL TABLES"
                    r"\90000559.L02.FR-BXL_IXL_L1-5_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_rev00.00.pdf"]
                self.control_tables_route.all_pages = [True, True]
                self.control_tables_route.specific_pages = [None, None]
                self.control_tables_overlap.control_tables_addr = [
                    r"C:\Users\naderc\Desktop\BXL\PHASE 1B2\CONTROL TABLES"
                    r"\90000530.L02.FR-BXL_IXL_LISTE DES OVERLAP + PARAMÈTRES OVERLAP_FR_rev02.00.pdf",
                    r"C:\Users\naderc\Desktop\BXL\PHASE 1B2\CONTROL TABLES"
                    r"\90000560.L02.FR-BXL_IXL_L1-5_LISTE DES OVERLAP + PARAMÈTRES OVERLAP_FR_rev00.00.pdf"]
                self.control_tables_overlap.all_pages = [True, True]
                self.control_tables_overlap.specific_pages = [None, None]
            # -- Survey -- #
            self.survey_loc.survey_sheet = [r"PhotoBook", r"Export_travaillé"]
            self.survey_loc.all_sheets = [False, False]
            self.survey_loc.start_row = [2, 13]
            self.survey_loc.ref_col = [1, 1]
            self.survey_loc.type_col = [2, 2]
            self.survey_loc.track_col = [3, 3]
            self.survey_loc.survey_kp_col = [4, 11]

        # ------------------------------- Copenhagen -------------------------------#
        elif project_name == Projects.Copenhagen:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_06_06_01_V04_R4\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_06_06_01_V04_R4\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_06_06_01_V04_R4\C64_D413\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\KCR\KCR_C11_D470_06_06_01_V04_R4"
            self.fouling_point_addr = r"C:\Users\naderc\Desktop\KCR\Fouling point data_KCR_V06_06_01_v03_récollé.xlsx"
            # -- Survey -- #
            # self.block_def = r"C:\Users\naderc\Desktop\KCR\CIRCUIT_DE_VOIE_patch_12_01_RC2.xls"
            self.survey_loc.survey_addr = [
                r"C:\Users\naderc\Desktop\KCR"
                r"\CR-ASTS-042189 - 15.00_ATT002 - ATC- KCR C_D932 - Field Survey report.xlsx",
                r"C:\Users\naderc\Desktop\KCR"
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
                r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES\CR-ASTS-045007-11.00-ATT001- Line CT Routes.pdf",
                r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES\CR-ASTS-045017-12.00-ATT001- CMC CT Routes.pdf"]
            self.control_tables_route.all_pages = [True, True]
            self.control_tables_route.specific_pages = [None, None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES\CR-ASTS-045009-07.00-ATT001- Line CT Overlap.pdf",
                r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES\CR-ASTS-045019-09.00 ATC CMC Control Tables Overlap.pdf"]
            self.control_tables_overlap.all_pages = [True, True]
            self.control_tables_overlap.specific_pages = [None, None]
            # -- IXL Approach Zone -- #
            self.ixl_apz.ixl_apz_file = (r"C:\Users\naderc\Desktop\KCR\CR-ASTS-GEN=Gen-PS=ATC=GEN-IFM-ICD-042155_14.00"
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
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V05\DC_SYS_IATPM.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V05\DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V05\C64_D413\DC_BOP.xls"
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\Glasgow\GW_C11_D470_06_06_01_V05"
            elif cbtc:
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_07_03_03_V02_R3\DC_SYS.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_07_03_03_V02_R3\DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_07_03_03_V02_R3\C64_D413\DC_BOP.xls"
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\Glasgow\GW_C11_D470_07_03_03_V02_R3"
            # -- Survey -- #
            self.survey_loc.survey_addr = (
                r"C:\Users\naderc\Desktop\Glasgow\SURVEY\2025_01_15 Survey Data and Input Sheet.xlsx")
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
                    r"C:\Users\naderc\Desktop\Glasgow\Control Tables\IATP"
                    r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_Rev00-3-86-Routes.pdf",
                    r"C:\Users\naderc\Desktop\Glasgow\Control Tables\IATP"
                    r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_Rev00-3-81-Routes.pdf"]
                self.control_tables_route.all_pages = [True, True]
                self.control_tables_route.specific_pages = [None, None]
                self.control_tables_overlap.control_tables_addr = [
                    r"C:\Users\naderc\Desktop\Glasgow\Control Tables\IATP"
                    r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_Rev00-173-236-Overlap.pdf",
                    r"C:\Users\naderc\Desktop\Glasgow\Control Tables\IATP"
                    r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_Rev00-162-173-Overlap.pdf"]
                self.control_tables_overlap.all_pages = [True, True]
                self.control_tables_overlap.specific_pages = [None, None]
            elif cbtc:
                self.control_tables_config_ini_file = "control_tables_configuration_gw.ini"
                self.control_tables_route.control_tables_addr = [
                    r"C:\Users\naderc\Desktop\Glasgow\Control Tables\CBTC\rev 03.00"
                    r"\GWISIGIXL0400-03.00-ATT002 - Appendix B_Routes_Rev00.pdf",
                    r"C:\Users\naderc\Desktop\Glasgow\Control Tables\CBTC\rev 03.00"
                    r"\GWISIGIXL0401-03.00-ATT002 - Appendix L_Routes_Rev00.pdf"]
                self.control_tables_route.all_pages = [True, True, True]
                self.control_tables_route.specific_pages = [None, None, None]
                self.control_tables_overlap.control_tables_addr = [
                    r"C:\Users\naderc\Desktop\Glasgow\Control Tables\CBTC\rev 03.00"
                    r"\GWISIGIXL0400-03.00-ATT006 - Appendix F_Overlap_Rev00.pdf"]
                self.control_tables_overlap.all_pages = [True]
                self.control_tables_overlap.specific_pages = [None]
            # -- IXL Approach Zone -- #
            if cbtc:
                self.ixl_apz.ixl_apz_file = r"C:\Users\naderc\Desktop\Glasgow\IXL_APZ.xlsx"
                self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
                self.ixl_apz.start_line = 2
                self.ixl_apz.sig_column = "B"
                self.ixl_apz.apz_start_column = 3
                self.ixl_apz.apz_nb_columns = 6

        # ------------------------------- Lima -------------------------------#
        elif project_name == Projects.Lima:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\LIMA\ML2_C_D470_DB0402RC1\DC_SYS_0402RC1.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\LIMA\ML2_C_D470_DB0403RC1\DC_SYS_0403RC1.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\LIMA\ML2_C_D470_DB0403RC1\DC_PAR_0402RC1.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\LIMA\ML2_C_D470_DB0403RC1\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\LIMA\ML2_C11_D470_06_06_00_V04_DB0403RC1"
            # -- Survey -- #
            # self.survey_loc.survey_addr = [
            #     r"C:\Users\naderc\Desktop\LIMA\[B20] AFS Survey - Medicion de puntos topograficos en rieles- ML-L2"
            #     r"\Depot\Anexos de Informe 02-012021\METRO_LINEA2 DIC. 2020_modified.xls",
            #     r"C:\Users\naderc\Desktop\LIMA\[B20] AFS Survey - Medicion de puntos topograficos en rieles- ML-L2"
            #     r"\MainLine\Anexos de informe 03-022021\LIMA L2 E1A - OBJECTS LIST-ENERO 2021.xls",
            #     r"C:\Users\naderc\Desktop\LIMA\[B20] AFS Survey - Medicion de puntos topograficos en rieles- ML-L2"
            #     r"\Objects_List - v3 Rev 01.xlsx"]
            self.survey_loc.survey_addr = [
                r"C:\Users\naderc\Desktop\LIMA\[B20] AFS Survey - Medicion de puntos topograficos en rieles- ML-L2"
                r"\Depot\Anexos de Informe 02-012021\METRO_LINEA2 DIC. 2020_modified.xls",
                r"C:\Users\naderc\Desktop\LIMA\[B20] AFS Survey - Medicion de puntos topograficos en rieles- ML-L2"
                r"\MainLine\Anexos de informe 03-022021\LIMA L2 E1A - OBJECTS LIST-ENERO 2021_via_reversed.xls",
                r"C:\Users\naderc\Desktop\LIMA\[B20] AFS Survey - Medicion de puntos topograficos en rieles- ML-L2"
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
                r"C:\Users\naderc\Desktop\LIMA\CONTROL TABLES"
                r"\B20X.0100002.L02.01ES-03.00-LINE 2 CONTROL TABLES - PHASE 1A"
                r"\ML2-AST-01A-A-025-GRAL-SSIXL-DIS-CD-4125-51-002.pdf",
                r"C:\Users\naderc\Desktop\LIMA\CONTROL TABLES"
                r"\B20X.0100002.L02.00ES-03.00-DEPOT CONTROL TABLES - PHASE 1A"
                r"\ML2-AST-01A-A-025-GRAL-SSIXL-DIS-CD-4126-51-002.pdf"]
            self.control_tables_route.all_pages = [True, True]
            self.control_tables_route.specific_pages = [None, None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\Users\naderc\Desktop\LIMA\CONTROL TABLES"
                r"\B20X.0100002.L02.01ES-03.00-LINE 2 CONTROL TABLES - PHASE 1A"
                r"\ML2-AST-01A-A-025-GRAL-SSIXL-DIS-CD-4125-51-006.pdf",
                r"C:\Users\naderc\Desktop\LIMA\CONTROL TABLES"
                r"\B20X.0100002.L02.00ES-03.00-DEPOT CONTROL TABLES - PHASE 1A"
                r"\ML2-AST-01A-A-025-GRAL-SSIXL-DIS-CD-4126-51-006.pdf"]
            self.control_tables_overlap.all_pages = [True, True]
            self.control_tables_overlap.specific_pages = [None, None]

        # ------------------------------- Milan -------------------------------#
        elif project_name == Projects.Milan:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_03_RC2\ML4_DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_03_RC2\ML4_DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_03_RC2\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C11_D470_06_06_02_V08"
            self.fouling_point_addr = (
                r"C:\Users\naderc\Desktop\ML4\4. WHOLE\Fouling Point ML4_WH_C_D470_V03_01_RC3.xlsx")
            # -- Survey -- #
            self.survey_loc.survey_addr = [
                r"C:\Users\naderc\Desktop\ML4\SURVEY\(ML4) LN04_Object_List_01_return28.03.24.xlsx",
                r"C:\Users\naderc\Desktop\ML4\SURVEY\ML4_TF2 REPORT OBJECT_AFS_REV_5.1.xlsx",
                r"C:\Users\naderc\Desktop\ML4\SURVEY\ML4_TF3 AFS DB integration template.xlsx",
                r"C:\Users\naderc\Desktop\ML4\SURVEY\ml4 tki_depot_ln01_object.xlsx",
                r"C:\Users\naderc\Desktop\ML4\SURVEY\ML4_LN02 - Coni Zugna to Sforza AFS Object List.xlsx"]
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
                r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf",
                r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf",
                r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf"]
            self.control_tables_route.all_pages = [False, False, False]
            self.control_tables_route.specific_pages = [(6, 160), (368, 521), (794, 935)]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf",
                r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf",
                r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE\M4-ST00PGRE-55047_05.00_Allegato_1.pdf"]
            self.control_tables_overlap.all_pages = [False, False, False]
            self.control_tables_overlap.specific_pages = [(316, 324), (676, 731), (1078, 1124)]
            # -- IXL Approach Zone -- #
            self.ixl_apz.ixl_apz_file = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_IXL_APZ.xlsx"
            self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
            self.ixl_apz.start_line = 2
            self.ixl_apz.sig_column = "B"
            self.ixl_apz.apz_start_column = 6
            self.ixl_apz.apz_nb_columns = 3

        # ------------------------------- Panama -------------------------------#
        elif project_name == Projects.Panama:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\Panama\PAN_C_D470_08_03_00_V03\DC_SYS.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Panama\PAN_C_D470_08_03_00_V03\DC_SYS_route.xls"
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\Panama\PAN_C_D470_08_03_00_V03\DC_SYS_patch_track.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Panama\PAN_C_D470_08_03_00_V03\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\Panama\PAN_C_D470_08_03_00_V03\C64_D413\DC_BOP.xls"
            # -- Control Tables -- #
            self.control_tables_route.control_tables_addr = [
                r"C:\Users\naderc\Desktop\Panama\CONTROL TABLES\PAN.SIG.IXL.A07.56EN_02.00 – Annex2.pdf"]
            self.control_tables_route.all_pages = [True]
            self.control_tables_route.specific_pages = [None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\Users\naderc\Desktop\Panama\CONTROL TABLES\PAN.SIG.IXL.A07.56EN_02.00 – Annex4.pdf"]
            self.control_tables_overlap.all_pages = [True]
            self.control_tables_overlap.specific_pages = [None]

        # ------------------------------- Riyadh -------------------------------#
        elif project_name == Projects.Riyadh:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_BOP_old.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\Riyadh\RL3_C11_D470_06_06_00_V07"
            self.kit_c121_d470_dir = r"C:\Users\naderc\Desktop\Riyadh\RL3_C121_D470_06_06_00_V04_20230327_165125"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\Riyadh\CIRCUIT_DE_VOIE RL3.xls"
            self.survey_loc.survey_addr = r"C:\Users\naderc\Desktop\Riyadh\Appendix K - RL3_D932_ed14.xls"
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
                r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                r"\MAIN LINE - CONTROL TABLES\Appendix B_Routes.pdf",
                r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                r"\WEST DEPOT - CONTROL TABLES (AUTOMATIC AREA)\Appendix B_Routes.pdf",
                r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                r"\EAST DEPOT - CONTROL TABLES (AUTOMATIC AREA)\Appendix B_Routes.pdf"]
            self.control_tables_route.all_pages = [True, True, True]
            self.control_tables_route.specific_pages = [None, None, None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                r"\MAIN LINE - CONTROL TABLES\Appendix E_Overlap.pdf",
                r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                r"\WEST DEPOT - CONTROL TABLES (AUTOMATIC AREA)\Appendix E_Overlap.pdf",
                r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                r"\EAST DEPOT - CONTROL TABLES (AUTOMATIC AREA)\Appendix E_Overlap.pdf"]
            self.control_tables_overlap.all_pages = [True, True, True]
            self.control_tables_overlap.specific_pages = [None, None, None]

        # ------------------------------- Thessaloniki -------------------------------#
        elif project_name == Projects.Thessaloniki:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V06_RC1\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V06_RC1\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V06_RC1\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\TSK\TSK_C11_D470_07_03_03_V13"
            # self.kit_c11_sp_dir = r"C:\Users\naderc\Desktop\TSK\TSK_C11_D470_07_03_03_V12_SP1"
            self.fouling_point_addr = r"C:\Users\naderc\Desktop\TSK\Fouling Points TSK_C_D470_07_03_03_V02_RC3.xlsx"
            # -- Survey -- #
            self.survey_loc.survey_addr = [
                r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_A.xlsx",
                r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_B.xls",
                r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_C.xlsx",
                r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_D.xlsx"]
            self.survey_loc.survey_sheet = [r"TSK_Object_list_310720_ro", r"TSK_Object_list_REV.3",
                                            r"Φύλλο1", r"Φύλλο1"]
            self.survey_loc.all_sheets = [False, False, False, False]
            self.survey_loc.start_row = [2, 2, 3, 3]
            self.survey_loc.ref_col = [1, 1, 13, 13]
            self.survey_loc.type_col = [2, 2, 14, 14]
            self.survey_loc.track_col = [3, 3, 15, 15]
            self.survey_loc.survey_kp_col = [7, 7, 17, 17]
            # -- Control Tables -- #
            self.control_tables_config_ini_file = r"control_tables_configuration_tsk.ini"
            self.control_tables_route.control_tables_addr = [
                r"C:\Users\naderc\Desktop\TSK\Control Tables rev 05.00\1G00LV601R721B_EN_ANNEX_B.pdf",
                r"C:\Users\naderc\Desktop\TSK\Control Tables rev 05.00\1G00LV601R722B_EN_ANNEX_B.pdf",
                r"C:\Users\naderc\Desktop\TSK\Control Tables KLM rev 02.00\1GE0LV601R721A_EN_ANNEX_B_KLM_rev02.00.pdf"]
            self.control_tables_route.all_pages = [True, True, True]
            self.control_tables_route.specific_pages = [None, None, None]
            self.control_tables_overlap.control_tables_addr = [
                r"C:\Users\naderc\Desktop\TSK\Control Tables rev 05.00\1G00LV601R721B_EN_ANNEX_D.pdf",
                r"C:\Users\naderc\Desktop\TSK\Control Tables rev 05.00\1G00LV601R722B_EN_ANNEX_D.pdf",
                r"C:\Users\naderc\Desktop\TSK\Control Tables KLM rev 02.00\1GE0LV601R721A_EN_ANNEX_D_KLM_rev02.00.pdf"]
            self.control_tables_overlap.all_pages = [True, True, True]
            self.control_tables_overlap.specific_pages = [None, None, None]
            # -- IXL Approach Zone -- #
            self.ixl_apz.ixl_apz_file = r"C:\Users\naderc\Desktop\TSK\TSK_IXL_APZ.xlsx"
            self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
            self.ixl_apz.start_line = 2
            self.ixl_apz.sig_column = "E"
            self.ixl_apz.apz_start_column = 6
            self.ixl_apz.apz_nb_columns = 2

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------- Other projects -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

        # --- OCTYS --- #

        # ------------------------------- OCTYS_L6 -------------------------------#
        elif project_name == Projects.OCTYS_L6:
            self.dc_sys_addr = (r"C:\Users\naderc\Desktop\OCTYS\Ligne 6\OCTYS_L6C_D405-6_0502"
                                r"\DC_SYS_OCTYS_L6C_D405-6_0502.xls")
            self.dc_par_addr = (r"C:\Users\naderc\Desktop\OCTYS\Ligne 6\OCTYS_L6C_D405-6_0502"
                                r"\DC_PAR_OCTYS_L6C_D405-6_0502.xls")
            # -- Survey -- #
            self.block_def = r""
            self.survey_loc.survey_addr = r""
            self.survey_loc.survey_sheet = r""
            self.survey_loc.all_sheets = True
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # --- USA --- #

        # ------------------------------- Baltimore -------------------------------#
        elif project_name == Projects.Baltimore:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\Baltimore MTA\MTA_C_D470_02_00_RC10\DC_SYS.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\Baltimore MTA\MTA_C_D470_V_02_01_RC2\DC_SYS.xls"
            # self.block_def = r"C:\Users\naderc\Desktop\USA\Baltimore MTA\CIRCUIT_DE_VOIE.xls"
            self.block_def = r"C:\Users\naderc\Desktop\USA\Baltimore MTA\CIRCUIT_DE_VOIE (12).xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = r"C:\Users\naderc\Desktop\USA\Baltimore MTA\MTA_D932.xlsx"
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- BART -------------------------------#
        elif project_name == Projects.BART:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\BART\BART_C_D470_08_02_00_V00\DC_SYS_BART.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\USA\BART\BART_C_D470_08_02_00_V00\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\USA\BART\BART_C_D470_08_02_00_V00\DC_BOP.xls"

        # ------------------------------- Hurontario -------------------------------#
        elif project_name == Projects.Hurontario:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\Hurontario\HLR_C_D470_V_7_3_3_0_RC1\DC_SYS.xls"

        # ------------------------------- MSH -------------------------------#
        elif project_name == Projects.MSH:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\MSH\MSH_C_D470_V09_02_RC1\DC_SYS.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\MSH\MSH_C_D470_06_06_01_V00\DC_SYS.xls"
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\MSH\MSH_C_D470_V09_02_RC1\DC_SYS_patch_slopes.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\USA\MSH\MSH_C11_D470_06_06_03_V00"
            # -- Survey -- #
            self.survey_loc.survey_addr = r"C:\Users\naderc\Desktop\USA\MSH\Topo_V_06_00.xlsx"
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
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\INDIA\CHENNAI - CMRL\CMRL_C_D470_S1_08_03_00_V01_01\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\INDIA\CHENNAI - CMRL\CMRL_C_D470_S1_08_03_00_V01_01\DC_PAR.xls"
            self.dc_bop_addr = (r"C:\Users\naderc\Desktop\INDIA\CHENNAI - CMRL\CMRL_C_D470_S1_08_03_00_V01_01"
                                r"\C64_D413\DC_BOP.xls")
            # -- Control Tables -- #
            self.control_tables_route.control_tables_addr = [
                (r"C:\Users\naderc\Desktop\INDIA\CHENNAI - CMRL\CONTROL TABLES"
                 r"\CMRL-14057_01.03 Annexure B_Route_Control_Table.pdf")]
            self.control_tables_route.all_pages = [True]
            self.control_tables_route.specific_pages = [None]

        # ------------------------------- KMRC Kolkata -------------------------------#
        elif project_name == Projects.KMRC:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\INDIA\KMRC Kolkata\KMRC_PH2_C_D470_00_RC07\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\INDIA\KMRC Kolkata\KMRC_PH2_C_D470_00_RC07\DC_PAR.xls"
            self.block_def = r"C:\Users\naderc\Desktop\INDIA\KMRC Kolkata\CIRCUIT_DE_VOIE_KMRC_PH2.xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = [
                r"C:\Users\naderc\Desktop\INDIA\KMRC Kolkata"
                r"\KMRC-76054_Rev01_C_D932 - Advanced field survey report.xlsm",
                r"C:\Users\naderc\Desktop\INDIA\KMRC Kolkata"
                r"\KMRC-26054_Rev09_C_D932 - Advanced field survey report.xlsm"]
            self.survey_loc.survey_sheet = [r"Result Final", r"KMRC-PH2A"]
            self.survey_loc.all_sheets = [False, False]
            self.survey_loc.start_row = [2, 2]
            self.survey_loc.ref_col = [1, 2]
            self.survey_loc.type_col = [4, 6]
            self.survey_loc.track_col = [2, 4]
            self.survey_loc.survey_kp_col = [3, 5]

        # ------------------------------- NMML1 -------------------------------#
        elif project_name == Projects.NMML1:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\INDIA\NMML1\NMML1_PH2_C_D470_00_00_RC5\DC_SYS.xls"
            self.block_def = r"C:\Users\naderc\Desktop\INDIA\NMML1\CIRCUIT_DE_VOIE_NMML1.xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = (
                r"C:\Users\naderc\Desktop\INDIA\NMML1\NMML1_C_D932_Line1_Advanced_field_survey_report.xlsm")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 5

        # ------------------------------- NOIDA -------------------------------#
        elif project_name == Projects.Noida:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\INDIA\NOIDA\NS01_C_D470_18_00_RC1\DC_SYS.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\INDIA\NOIDA\NS01_C_D470_18_00_RC1\DC_SYS_patch_ZC04.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\INDIA\NOIDA\NS01_C_D470_18_00_RC1\DC_PAR.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\INDIA\NOIDA\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (
                r"C:\Users\naderc\Desktop\INDIA\NOIDA"
                r"\NS01-L-SIG-9-0001 NS01_C_D932 - Advanced field survey report_06.00.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # --- China --- #

        # ------------------------------- Shenyang -------------------------------#
        elif project_name == Projects.Shenyang:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\CHINA\CHINA V4\Shenyang\SHYL1_10_00\DC_SYS_SHYL1_10_00.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\CHINA\CHINA V4\Shenyang\SHYL1_10_00\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (
                r"C:\Users\naderc\Desktop\CHINA\CHINA V4\Shenyang\SY_L1_SIG_DB_D932_1409_V3.3_2016_5_11.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # ------------------------------- Taipei -------------------------------#
        elif project_name == Projects.Taipei:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\CHINA\TAIPEI CLP1\TC1_C_D470_06_00_RC14\DC_SYS.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\CHINA\TAIPEI CLP1\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = [
                r"C:\Users\naderc\Desktop\CHINA\TAIPEI CLP1\Survey\TC1_D932_Depot_20190221.xlsx",
                r"C:\Users\naderc\Desktop\CHINA\TAIPEI CLP1\Survey"
                r"\TC1_Mainline_AFS_object_list_draft_J20180720_vs_cmts_20180817_R1_vs_mod_20181212.xlsx",
                r"C:\Users\naderc\Desktop\CHINA\TAIPEI CLP1\Survey\901_軌.xlsx"]
            self.survey_loc.survey_sheet = [r"Depot", r"Mainline ", r"工作表1"]
            self.survey_loc.all_sheets = [False, False, False]
            self.survey_loc.start_row = [2, 2, 2]
            self.survey_loc.ref_col = [1, 1, 7]
            self.survey_loc.type_col = [4, 5, 9]
            self.survey_loc.track_col = [2, 2, 8]
            self.survey_loc.survey_kp_col = [3, 3, 11]

        # ------------------------------- Wenzhou -------------------------------#
        elif project_name == Projects.Wenzhou:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\CHINA\WENZHOU\WZS1_C_D470_08_01\DC_SYS_0801.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\CHINA\WENZHOU\WZS1_C_D470_08_04\DC_SYS_0804.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\CHINA\WENZHOU\WZS1_C_D470_08_01\CIRCUIT_DE_VOIE_Corrected.xls"
            self.survey_loc.survey_addr = (
                r"C:\Users\naderc\Desktop\CHINA\WENZHOU\WZ_S1P1_SIG_DB_D932_1409_D932_V1.8_modified.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # --- Mock-up --- #

        # ------------------------------- Mock-up -------------------------------#
        elif project_name == Projects.Mock_up:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up.xls"

        # ------------------------------- Mock-up 2 -------------------------------#
        elif project_name == Projects.Mock_up_2:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up2.xls"

        # ------------------------------- Mock-up 3 -------------------------------#
        elif project_name == Projects.Mock_up_3:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up3.xls"

        # ------------------------------- Mock-up 4 -------------------------------#
        elif project_name == Projects.Mock_up_4:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up4.xls"

        # ------------------------------- Mock-up 5 -------------------------------#
        elif project_name == Projects.Mock_up_5:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up5.xls"

    def reset(self):
        self.cctool_oo_schema = r""
        self.dc_sys_addr = r""
        self.dc_sys_addr_old = r""
        self.dc_par_addr = r""
        self.dc_bop_addr = r""
        self.block_def = None
        self.survey_loc = self.SurveyLoc()
        self.kit_c11_dir = r""
        self.kit_c11_sp_dir = r""
        self.kit_c121_d470_dir = r""
        self.control_tables_route = self.ControlTablesLoc()
        self.control_tables_overlap = self.ControlTablesLoc()
        self.control_tables_config_ini_file = r"control_tables_configuration.ini"
        self.ixl_apz = self.IxlApz()
        self.fouling_point_addr = r""


DATABASE_LOC = ProjectDatabaseLoc(PROJECT_NAME)
