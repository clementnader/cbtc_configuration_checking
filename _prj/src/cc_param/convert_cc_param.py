#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import argparse
from ..utils import *
from .cc_param_utils import *


__all__ = ["convert_cc_param"]


def convert_cc_param():
    """ Convert the CCParameter.csv file from UNIX newline character (\n) and Windows newline character (\r\n). """
    parser = argparse.ArgumentParser(
        add_help=True,
        description=f"Convert CCParameter.csv files in kit C11_D470 from Unix to Windows.",
    )
    parser.add_argument("-i", "--input_kit_c11_dir", dest="input_dir", action="store", type=str, required=True,
                        metavar=f"{Color.turquoise}Kit_C11_D470{Color.reset}",
                        help=f"path to the kit C11_D470 folder where the TrainUnit files are stored, "
                             f"which contains the CCParameter files "
                             f"{Color.dark_grey}(put it between quotes){Color.reset}")
    parser.add_argument("-d", "--destination_folder", dest="dest_dir", action="store", type=str, required=False,
                        metavar=f"{Color.turquoise}Destination_Root_Folder{Color.reset}",
                        default=".",
                        help=f"root folder where the result converted directory will be stored, "
                             f"default is the current folder")
    args = vars(parser.parse_args())
    input_dir = args["input_dir"]
    dest_dir = args["dest_dir"]
    _copy_kit_c11_d470(input_dir, dest_dir)


def _copy_kit_c11_d470(input_dir, dest_dir):
    result_dir = f"{os.path.split(input_dir)[-1]}_converted"
    full_res_dir = os.path.join(dest_dir, result_dir)
    print(f"\nConverting the CCParameter.csv files from:\n"
          f"\t{Color.yellow}{input_dir}{Color.reset}\n"
          f"to\n"
          f"\t{Color.yellow}{full_res_dir}{Color.reset}\n")
    _create_result_dir(full_res_dir)
    for train_dir in os.listdir(input_dir):
        full_path = os.path.join(input_dir, train_dir)
        dest_path = os.path.join(full_res_dir, train_dir)
        if os.path.isdir(full_path) and train_dir.startswith(TRAIN_UNIT_PREFIX):
            _create_dir(dest_path)
            _copy_converted_train_unit(full_path, dest_path, input_dir)
        else:
            _copy_file_or_dir(full_path, dest_path)
    print(f"\nConversion is done, the result folder can be found at:\n"
          f"\t{Color.light_green}{full_res_dir}{Color.reset}")


def _create_result_dir(full_res_dir: str) -> None:
    if os.path.exists(full_res_dir):
        print_warning(f"The result folder already exists"
                      f"\n at {full_res_dir}.")
        if not ask_question_yes_or_no("Do you want to overwrite it?"):
            print_error(f"Process aborted.")
            exit(1)
        shutil.rmtree(full_res_dir)
    os.makedirs(full_res_dir)


def _create_dir(dir_path):
    os.mkdir(dir_path)


def _copy_file_or_dir(input_path, dest_path):
    if os.path.isdir(input_path):
        shutil.copytree(input_path, dest_path)
    elif os.path.isfile(input_path):
        shutil.copy(input_path, dest_path)


def _copy_converted_train_unit(input_path, dest_path, input_dir):
    for cab_dir in os.listdir(input_path):
        cab_full_path = os.path.join(input_path, cab_dir)
        cab_dest_path = os.path.join(dest_path, cab_dir)
        if os.path.isdir(cab_full_path) and cab_dir.startswith(CAB_DIR_PREFIX):
            _create_dir(cab_dest_path)
            _copy_converted_cab(cab_full_path, cab_dest_path, input_dir)
        else:
            _copy_file_or_dir(cab_full_path, cab_dest_path)


def _copy_converted_cab(input_path, dest_path, input_dir):
    for ccparam_dir in os.listdir(input_path):
        ccparam_dir_full_path = os.path.join(input_path, ccparam_dir)
        ccparam_dir_dest_path = os.path.join(dest_path, ccparam_dir)
        if os.path.isdir(ccparam_dir_full_path) and ccparam_dir == CC_PARAM_DIR:
            _create_dir(ccparam_dir_dest_path)
            _copy_converted_ccparam(ccparam_dir_full_path, ccparam_dir_dest_path, input_dir)
        else:
            _copy_file_or_dir(ccparam_dir_full_path, ccparam_dir_dest_path)


def _copy_converted_ccparam(input_path, dest_path, input_dir):
    for ccparam in os.listdir(input_path):
        ccparam_full_path = os.path.join(input_path, ccparam)
        ccparam_dest_path = os.path.join(dest_path, ccparam)
        if os.path.isfile(ccparam_full_path) and ccparam == CC_PARAM_FILE:
            _convert_ccparam_file_unix_to_windows(ccparam_full_path, ccparam_dest_path, input_dir)
        else:
            _copy_file_or_dir(ccparam_full_path, ccparam_dest_path)


UNIX_LINE_END = b"\n"
WINDOWS_LINE_END = b"\r\n"


def _convert_ccparam_file_unix_to_windows(ccparam_full_path, ccparam_dest_path, input_dir):
    print(f"{Color.blue}Converting file \"{ccparam_full_path.removeprefix(input_dir)}\"...{Color.reset}")
    with open(ccparam_full_path, "rb") as f:
        with open(ccparam_dest_path, "wb") as dest_f:
            dest_f.write(f.read().replace(UNIX_LINE_END, WINDOWS_LINE_END))
