#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .utils.colors_pkg import *


class Projects:
    Ankara = "Ankara"
    Brussels = "Brussels"
    Copenhagen = "Copenhagen"
    Glasgow = "Glasgow"
    Milan = "Milan"
    Riyadh = "Riyadh"
    Thessaloniki = "Thessaloniki"

    Baltimore = "Baltimore"
    BART = "BART"
    Mock_up = "Mock-up"


# PROJECT_NAME = Projects.Ankara
# PROJECT_NAME = Projects.Brussels
# PROJECT_NAME = Projects.Copenhagen
# PROJECT_NAME = Projects.Glasgow
# PROJECT_NAME = Projects.Milan
# PROJECT_NAME = Projects.Riyadh
PROJECT_NAME = Projects.Thessaloniki

# PROJECT_NAME = Projects.BART
# PROJECT_NAME = Projects.Mock_up


class ProjectDatabaseLoc:
    class ControlTablesLoc:
        line = r""  # Main Line
        cmc = r""   # CMC: Control and Maintenance Center
        cmc2 = r""  # if CMC is split in two parts

    dc_sys_addr = r""
    dc_sys_addr_old = r""
    dc_par_addr = r""
    dc_bop_addr = r""
    kit_c11_dir = r""
    control_tables_route = ControlTablesLoc()
    control_tables_overlap = ControlTablesLoc()

    def __init__(self, project_name: str):
        print_title(f"The working project is {Color.vivid_green}{project_name}{Color.reset}.")

        # ------------------------------- Ankara -------------------------------#
        if project_name == Projects.Ankara:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\ANK_L2_C_D470_V06_00_RC3\DC_SYS.xls"
            self.dc_sys_addr = r"c:\users\naderc\desktop\ank\ank_l2_c_d470_v06_00_rc4\dc_sys.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L2_C_D470_V06_00_RC4\DC_PAR.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\Ank\ANK_L2_C11_D470_06_05_03_V07"

        # ------------------------------- Brussels -------------------------------#
        elif project_name == Projects.Brussels:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B\DC_SYS_old.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B\C64_D413\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\BXL\BXL_C11_D470_72_01_03_V07_P1B"

            self.control_tables_route.line = r"C:\Users\naderc\Desktop\BXL\Control Tables" \
                                             r"\BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_" \
                                             r"rev00.01_ERASME-ANTENNA LINE.pdf"
            self.control_tables_route.cmc = r"C:\Users\naderc\Desktop\BXL\Control Tables" \
                                            r"\BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_" \
                                            r"rev00.05_ERASME DEPOT.pdf"
            self.control_tables_overlap.line = r"C:\Users\naderc\Desktop\BXL\Control Tables" \
                                               r"\BXL_IXL_LISTE DES OVERLAP + PARAMETRES OVERLAP_FR_" \
                                               r"rev00.02_ERASME-ANTENNA LINE.pdf"
            self.control_tables_overlap.cmc = r"C:\Users\naderc\Desktop\BXL\Control Tables" \
                                              r"\BXL_IXL_LISTE DES OVERLAP + PARAMETRES OVERLAP_FR_" \
                                              r"rev00.05_ERASME DEPOT-6-91.pdf"

        # ------------------------------- Copenhagen -------------------------------#
        elif project_name == Projects.Copenhagen:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_15_00_RC5\DC_SYS.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_15_00_RC5\DC_BOP.xls"

            self.control_tables_route.line = r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES" \
                                             r"\CR-ASTS-045007-10.00 ATC Line Control Tables Routes.pdf"
            self.control_tables_route.cmc = r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES" \
                                            r"\CR-ASTS-045017-11.00 ATC CMC Control Tables Routes.pdf"
            self.control_tables_overlap.line = r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES" \
                                               r"\CR-ASTS-045009-06.00 ATC Line Control Tables Overlap.pdf"
            self.control_tables_overlap.cmc = r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES" \
                                              r"\CR-ASTS-045019-09.00 ATC CMC Control Tables Overlap.pdf"

        # ------------------------------- Glasgow -------------------------------#
        elif project_name == Projects.Glasgow:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V03\DC_SYS.xls"
            self.dc_sys_addr_old = r"C:\Users\naderc\Desktop\Glasgow\old glagow\DC_SYS_.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V03\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V03\C64_D413\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\Glasgow\GW_C11_D470_06_06_01_V03"

            self.control_tables_route.line = r"C:\Users\naderc\Desktop\Glasgow\Control Tables" \
                                             r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_" \
                                             r"Rev00-3-86-Routes.pdf"
            self.control_tables_route.cmc = r"C:\Users\naderc\Desktop\Glasgow\Control Tables" \
                                            r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_" \
                                            r"Rev00-3-81-Routes.pdf"
            self.control_tables_overlap.line = r"C:\Users\naderc\Desktop\Glasgow\Control Tables" \
                                               r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_" \
                                               r"Rev00-173-236-Overlap.pdf"
            self.control_tables_overlap.cmc = r"C:\Users\naderc\Desktop\Glasgow\Control Tables" \
                                              r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_" \
                                              r"Rev00-162-173-Overlap.pdf"

        # ------------------------------- Milan -------------------------------#
        elif project_name == Projects.Milan:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\ML4\ML4_TF3_C_D470_01_02_RC2\ML4_DC_SYS.xls"
            # self.dc_sys_addr_old = r"C:\Users\naderc\Desktop\ML4\ML4_DC_SYS_01_rc3.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\ML4\ML4_TF3_C_D470_01_02_RC2\ML4_DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\ML4\ML4_TF3_C_D470_01_02_RC2\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\ML4\ML4_TF3_C11_D470_06_05_05_V04"

            # ?????
            # self.control_tables_route.line = r"C:\Users\naderc\Desktop\ML4\Control Tables" \
            #                                  r"\M4-ST00PGRE-55129_00.01_Allegato_1_Routes.pdf"
            # self.control_tables_overlap.line = r"C:\Users\naderc\Desktop\ML4\Control Tables" \
            #                                    r"\M4-ST00PGRE-55129_00.01_Allegato_1_Overlap.pdf"
            # TF3
            self.control_tables_route.line = r"C:\Users\naderc\Desktop\ML4\Control Tables" \
                                             r"\M4-ST00PGRE-55634_01.00_Allegato_1-TF3-5-144 - Routes.pdf"
            self.control_tables_overlap.line = r"C:\Users\naderc\Desktop\ML4\Control Tables" \
                                               r"\M4-ST00PGRE-55634_01.00_Allegato_1-TF3-285-328 - Overlap.pdf"
            # DEPOT + LN01
            # self.control_tables_route.line = r"C:\Users\naderc\Desktop\ML4\Control Tables" \
            #                                  r"\M4-ST00PGRE-55047_00.03_Allegato_1-DEPOT LN01-" \
            #                                  r"4-111 - LINE - Routes.pdf"
            # self.control_tables_route.cmc = r"C:\Users\naderc\Desktop\ML4\Control Tables" \
            #                                 r"\M4-ST00PGRE-55047_00.03_Allegato_1-DEPOT LN01-" \
            #                                 r"300-484 - CMC - Routes.pdf"
            # self.control_tables_overlap.line = r"C:\Users\naderc\Desktop\ML4\Control Tables" \
            #                                    r"\M4-ST00PGRE-55047_00.03_Allegato_1-DEPOT LN01-" \
            #                                    r"220-256 - LINE - Overlap.pdf"
            # self.control_tables_overlap.cmc = r"C:\Users\naderc\Desktop\ML4\Control Tables" \
            #                                   r"\M4-ST00PGRE-55047_00.03_Allegato_1-DEPOT LN01-" \
            #                                   r"670-684 - CMC - Overlap.pdf"

        # ------------------------------- Thessaloniki -------------------------------#
        elif project_name == Projects.Riyadh:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_BOP_old.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\Riyadh\RL3_C11_D470_06_06_00_V07"

            self.control_tables_route.line = r"C:\Users\naderc\Desktop\Riyadh\Control Tables" \
                                             r"\MAIN LINE - CONTROL TABLES" \
                                             r"\Appendix B_Routes.pdf"
            self.control_tables_route.cmc = r"C:\Users\naderc\Desktop\Riyadh\Control Tables" \
                                            r"\WEST DEPOT - CONTROL TABLES (AUTOMATIC AREA)" \
                                            r"\Appendix B_Routes.pdf"
            self.control_tables_route.cmc2 = r"C:\Users\naderc\Desktop\Riyadh\Control Tables" \
                                             r"\EAST DEPOT - CONTROL TABLES (AUTOMATIC AREA)" \
                                             r"\Appendix B_Routes.pdf"
            self.control_tables_overlap.line = r"C:\Users\naderc\Desktop\Riyadh\Control Tables" \
                                               r"\MAIN LINE - CONTROL TABLES" \
                                               r"\Appendix E_Overlap.pdf"
            self.control_tables_overlap.cmc = r"C:\Users\naderc\Desktop\Riyadh\Control Tables" \
                                              r"\WEST DEPOT - CONTROL TABLES (AUTOMATIC AREA)" \
                                              r"\Appendix E_Overlap.pdf"
            self.control_tables_overlap.cmc2 = r"C:\Users\naderc\Desktop\Riyadh\Control Tables" \
                                               r"\EAST DEPOT - CONTROL TABLES (AUTOMATIC AREA)" \
                                               r"\Appendix E_Overlap.pdf"

        # ------------------------------- Thessaloniki -------------------------------#
        elif project_name == Projects.Thessaloniki:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V01_RC3\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V01_RC3\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V01_RC3\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\TSK\TSK_C11_D470_07_03_03_V02"

            self.control_tables_route.line = r"C:\Users\naderc\Desktop\TSK\Control Tables" \
                                             r"\1G00LV601R721C_EN_ANNEX_B.pdf"
            self.control_tables_route.cmc = r"C:\Users\naderc\Desktop\TSK\Control Tables" \
                                            r"\1G00LV601R722C_EN_ANNEX_B.pdf"
            self.control_tables_overlap.line = r"C:\Users\naderc\Desktop\TSK\Control Tables" \
                                               r"\1G00LV601R721C_EN_ANNEX_D.pdf"
            self.control_tables_overlap.cmc = r"C:\Users\naderc\Desktop\TSK\Control Tables" \
                                              r"\1G00LV601R722C_EN_ANNEX_D.pdf"

        # ------------------------------- Baltimore -------------------------------#
        elif project_name == Projects.Baltimore:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Baltimore\DC_SYS MTAB 721 ++.xls"

        # ------------------------------- BART -------------------------------#
        elif project_name == Projects.BART:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\BART" \
                               r"\BART_V2.3.0_SYS_1-DC_SYS-DRAGON_2.1.1 (RefSys 7.2.1.1).xls"

        # ------------------------------- Mock-up -------------------------------#
        elif project_name == Projects.Mock_up:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\BART\DC_SYS_mock-up.xls"


DATABASE_LOC = ProjectDatabaseLoc(PROJECT_NAME)
