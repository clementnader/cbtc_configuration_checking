#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import configparser
from ..utils import *
from ..database_location import DATABASE_LOCATION
from ..control_tables.control_tables_utils import *


__all__ = ["update_cctool_oo", "update_config_info"]


CONFIG_INI_FILE_NAME = "config.ini"
CONFIG_INI_FILE = os.path.join(LAUNCH_FUNCTION_DIRECTORY, "config.ini")


def update_cctool_oo():
    print_section_title(f"Read \"{CONFIG_INI_FILE_NAME}\" file to set up the CCTool-OO Schema file used by the tool:")
    print(CONFIG_INI_FILE)
    DATABASE_LOCATION.reset()
    config = configparser.ConfigParser()
    config.read(CONFIG_INI_FILE, encoding="utf-8")

    ini_cctool_oo_schema = config["database"].get("cctool_oo_schema", "").strip()
    if ini_cctool_oo_schema:
        print_log(f"CCTool-OO Schema file is {Color.default}\"{ini_cctool_oo_schema}\"{Color.reset}.")
        DATABASE_LOCATION.cctool_oo_schema = ini_cctool_oo_schema
    else:
        print_log(f"No CCTool-OO Schema file provided.")



def update_config_info():
    print_section_title(f"Read \"{CONFIG_INI_FILE_NAME}\" file to set up the database files used by the tool:")
    print(CONFIG_INI_FILE)
    DATABASE_LOCATION.reset()
    config = configparser.ConfigParser()
    config.read(CONFIG_INI_FILE, encoding="utf-8")

    ini_cctool_oo_schema = config["database"].get("cctool_oo_schema", "").strip()
    if ini_cctool_oo_schema:
        DATABASE_LOCATION.cctool_oo_schema = ini_cctool_oo_schema

    ini_dc_sys = config["database"].get("dc_sys", "").strip()
    if ini_dc_sys:
        print_log(f"DC_SYS file is {Color.default}\"{ini_dc_sys}\"{Color.reset}.")
        DATABASE_LOCATION.dc_sys_addr = ini_dc_sys

    ini_dc_par = config["database"].get("dc_par", "").strip()
    if ini_dc_par:
        print_log(f"DC_PAR file is {Color.default}\"{ini_dc_par}\"{Color.reset}.")
        DATABASE_LOCATION.dc_par_addr = ini_dc_par

    ini_dc_bop = config["database"].get("dc_bop", "").strip()
    if ini_dc_bop:
        print_log(f"DC_BOP file is {Color.default}\"{ini_dc_bop}\"{Color.reset}.")
        DATABASE_LOCATION.dc_bop_addr = ini_dc_bop

    ini_fouling_point = config["database"].get("fouling_point", "").strip()
    if ini_fouling_point:
        print_log(f"Fouling Point file is {Color.default}\"{ini_fouling_point}\"{Color.reset}.")
        DATABASE_LOCATION.fouling_point_addr = ini_fouling_point

    ini_block_definition = config["database"].get("block_definition", "").strip()
    if ini_block_definition:
        print_log(f"Block Definition file is {Color.default}\"{ini_block_definition}\"{Color.reset}.")
        DATABASE_LOCATION.block_def = ini_block_definition

    ini_kit_c11_dir = config["database"].get("c11_d470", "").strip()
    if ini_kit_c11_dir:
        print_log(f"C11_D470 folder is {Color.default}\"{ini_kit_c11_dir}\"{Color.reset}.")
        DATABASE_LOCATION.kit_c11_dir = ini_kit_c11_dir

    _update_survey_info(config)
    _update_apz_ixl_info(config)
    _update_control_tables_config_ini_file(config)
    _update_control_tables_info(config, ct_type=CONTROL_TABLE_TYPE.route)
    _update_control_tables_info(config, ct_type=CONTROL_TABLE_TYPE.overlap)

    print_bar(start="\n")


def _update_survey_info(config: configparser.ConfigParser):
    ini_survey_address = config["survey"].get("survey_address", "").strip()
    if ini_survey_address:
        ini_survey_address_list = [info.strip() for info in ini_survey_address.split(",")]
        print_log(f"Survey file is {Color.default}\"{ini_survey_address_list}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.survey_addr = ini_survey_address_list

    ini_survey_sheet = config["survey"].get("survey_sheet_name", "").strip()
    if ini_survey_sheet:
        ini_survey_sheet_list = [info.strip() for info in ini_survey_sheet.split(",")]
        print_log(f"\tCorresponding survey sheet is {Color.default}\"{ini_survey_sheet_list}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.survey_sheet = ini_survey_sheet_list

    ini_all_sheets = config["survey"].get("all_sheets", "").strip()
    if ini_all_sheets:
        ini_all_sheets_list = [True if info.strip() == "True" else False for info in ini_all_sheets.split(",")]
        print_log(f"\tCorresponding all_sheets flag is {Color.default}\"{ini_all_sheets_list}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.all_sheets = ini_all_sheets_list

    ini_start_row = config["survey"].get("start_row", "").strip()
    if ini_start_row:
        ini_start_row_list = [int(info.strip()) for info in ini_start_row.split(",")]
        print_log(f"\tCorresponding start row is {Color.default}\"{ini_start_row_list}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.start_row = ini_start_row_list

    ini_reference_column = config["survey"].get("reference_column", "").strip()
    if ini_reference_column:
        ini_reference_column_list = [get_xl_column_from_number_or_letter(info.strip())
                                     for info in ini_reference_column.split(",")]
        print_log(f"\tCorresponding reference column is {Color.default}\"{ini_reference_column_list}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.ref_col = ini_reference_column_list

    ini_type_column = config["survey"].get("type_column", "").strip()
    if ini_type_column:
        ini_type_column_list = [get_xl_column_from_number_or_letter(info.strip())
                                for info in ini_type_column.split(",")]
        print_log(f"\tCorresponding type column is {Color.default}\"{ini_type_column_list}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.type_col = ini_type_column_list

    ini_track_column = config["survey"].get("track_column", "").strip()
    if ini_track_column:
        ini_track_column_list = [get_xl_column_from_number_or_letter(info.strip())
                                 for info in ini_track_column.split(",")]
        print_log(f"\tCorresponding track column is {Color.default}\"{ini_track_column_list}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.track_col = ini_track_column_list

    ini_surveyed_kp_column = config["survey"].get("surveyed_kp_column", "").strip()
    if ini_surveyed_kp_column:
        ini_surveyed_kp_column_list = [get_xl_column_from_number_or_letter(info.strip())
                                       for info in ini_surveyed_kp_column.split(",")]
        print_log(f"\tCorresponding surveyed KP column is {Color.default}\"{ini_surveyed_kp_column_list}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.survey_kp_col = ini_surveyed_kp_column_list

    list_nb_survey_info = [len(info) for info in (DATABASE_LOCATION.survey_loc.survey_addr,
                                                  DATABASE_LOCATION.survey_loc.survey_sheet,
                                                  DATABASE_LOCATION.survey_loc.all_sheets,
                                                  DATABASE_LOCATION.survey_loc.start_row,
                                                  DATABASE_LOCATION.survey_loc.ref_col,
                                                  DATABASE_LOCATION.survey_loc.type_col,
                                                  DATABASE_LOCATION.survey_loc.track_col,
                                                  DATABASE_LOCATION.survey_loc.survey_kp_col)]
    if min(list_nb_survey_info) != max(list_nb_survey_info):
        print_warning(f"The survey information does not match the number of surveys: "
                      f"only the first {min(list_nb_survey_info)} will be considered.")


def _update_apz_ixl_info(config: configparser.ConfigParser):
    ini_ixl_apz_address = config["ixl_apz"].get("ixl_apz_address", "").strip()
    if ini_ixl_apz_address:
        print_log(f"IXL Approach Zone file is {Color.default}\"{ini_ixl_apz_address}\"{Color.reset}.")
        DATABASE_LOCATION.ixl_apz.ixl_apz_file = ini_ixl_apz_address

    ini_ixl_apz_sheet_name = config["ixl_apz"].get("ixl_apz_sheet_name", "").strip()
    if ini_ixl_apz_sheet_name:
        print_log(f"\tCorresponding IXL APZ sheet is {Color.default}\"{ini_ixl_apz_sheet_name}\"{Color.reset}.")
        DATABASE_LOCATION.ixl_apz.ixl_apz_sheet_name = ini_ixl_apz_sheet_name

    ini_start_row = config["ixl_apz"].get("start_row", "").strip()
    if ini_start_row:
        ini_start_row = int(ini_start_row)
        print_log(f"\tCorresponding start row is {Color.default}\"{ini_start_row}\"{Color.reset}.")
        DATABASE_LOCATION.ixl_apz.start_line = ini_start_row

    ini_sig_column = config["ixl_apz"].get("signal_column", "").strip()
    if ini_sig_column:
        ini_sig_column = get_xl_column_from_number_or_letter(ini_sig_column)
        print_log(f"\tCorresponding signal column is {Color.default}\"{ini_sig_column}\"{Color.reset}.")
        DATABASE_LOCATION.ixl_apz.sig_column = ini_sig_column

    ini_apz_start_column = config["ixl_apz"].get("apz_start_column", "").strip()
    if ini_apz_start_column:
        ini_apz_start_column = get_xl_column_from_number_or_letter(ini_apz_start_column)
        print_log(f"\tCorresponding APZ start column is {Color.default}\"{ini_apz_start_column}\"{Color.reset}.")
        DATABASE_LOCATION.ixl_apz.apz_start_column = ini_apz_start_column

    ini_apz_nb_columns = config["ixl_apz"].get("apz_number_of_columns", "").strip()
    if ini_apz_nb_columns:
        ini_apz_nb_columns = int(ini_apz_nb_columns)
        print_log(f"\tCorresponding APZ number of columns is {Color.default}\"{ini_apz_nb_columns}\"{Color.reset}.")
        DATABASE_LOCATION.ixl_apz.apz_nb_columns = ini_apz_nb_columns

    list_info_not_present = [not value for value in [DATABASE_LOCATION.ixl_apz.ixl_apz_file,
                                                     DATABASE_LOCATION.ixl_apz.ixl_apz_sheet_name,
                                                     DATABASE_LOCATION.ixl_apz.start_line,
                                                     DATABASE_LOCATION.ixl_apz.sig_column,
                                                     DATABASE_LOCATION.ixl_apz.apz_start_column,
                                                     DATABASE_LOCATION.ixl_apz.apz_nb_columns]]
    if all(list_info_not_present):
        # No IXL APZ specified
        return
    if any(list_info_not_present):
        print_warning(f"The IXL Approach Zone file information is not coherent, some info is missing.")


def _update_control_tables_config_ini_file(config: configparser.ConfigParser):
    ini_ct_configuration_ini_file = config["control_tables_configuration"].get(
        "control_tables_configuration_ini_file", "").strip()
    if ini_ct_configuration_ini_file:
        print_log(f"Control Tables Configuration .ini file is "
                  f"{Color.default}\"{ini_ct_configuration_ini_file}\"{Color.reset}.")
        DATABASE_LOCATION.control_tables_config_ini_file = ini_ct_configuration_ini_file


def _update_control_tables_info(config: configparser.ConfigParser, ct_type: str):
    control_tables_type = f"{ct_type.lower()}_control_tables"
    database_ct_loc = (DATABASE_LOCATION.control_tables_route if ct_type == CONTROL_TABLE_TYPE.route
                       else DATABASE_LOCATION.control_tables_overlap)

    ini_ct_address = config[control_tables_type].get("control_tables_address", "").strip()
    if ini_ct_address:
        ini_ct_address_list = [info.strip() for info in ini_ct_address.split(",")]
        print_log(f"{ct_type} Control Tables file is {Color.default}\"{ini_ct_address_list}\"{Color.reset}.")
        database_ct_loc.control_tables_addr = ini_ct_address_list

    ini_all_pages = config[control_tables_type].get("all_pages", "").strip()
    if ini_all_pages:
        ini_all_pages_list = [True if info.strip() == "True" else False for info in ini_all_pages.split(",")]
        print_log(f"\t{ct_type} Control Tables all_pages flag is {Color.default}\"{ini_all_pages_list}\"{Color.reset}.")
        database_ct_loc.all_pages = ini_all_pages_list

    ini_specific_pages = config[control_tables_type].get("specific_pages", "").strip()
    if ini_specific_pages:
        ini_specific_pages_list = [(int(num_page.strip()) for num_page in info.strip().split("-")) if "-" in info
                                   else int(info.strip())
                                   for info in ini_specific_pages.split(",")]
        print_log(f"\t{ct_type} Control Tables specific_pages is "
                  f"{Color.default}\"{ini_specific_pages_list}\"{Color.reset}.")
        database_ct_loc.specific_pages = ini_specific_pages_list

    list_nb_ct_info = [len(info) for info in (database_ct_loc.control_tables_addr,
                                              database_ct_loc.all_pages,
                                              database_ct_loc.specific_pages)]
    if min(list_nb_ct_info) != max(list_nb_ct_info):
        print_warning(f"The {ct_type} Control Tables information does not match the number of Control Tables: "
                      f"only the first {min(list_nb_ct_info)} will be considered.")
