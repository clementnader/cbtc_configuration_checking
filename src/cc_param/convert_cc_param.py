#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import argparse
from .cc_param_utils import *
from ..colors_pkg import *

DEFAULT_RES_DIRECTORY = os.path.join(os.getenv("UserProfile"), r"Desktop")


def convert_ccparam():
    parser = argparse.ArgumentParser(
        add_help=True,
        description=f"Convert CCParameter.csv files in kit {Color.white}C11_D470{Color.end} from Unix to Windows.",
    )
    parser.add_argument("-i", "--input", dest="input_dir", action="store", type=str, required=True,
                        metavar=f"{Color.blue}Folder C11_D470{Color.end}",
                        help=f"path to the kit C11_D470 folder where the TrainUnit files are stored, "
                             f"which contains the CCParameter files "
                             f"{Color.dark_grey}(if the path contains spaces, put it between quotes){Color.end}")
    parser.add_argument("-d", "--dest", dest="dest_dir", action="store", type=str, required=False,
                        metavar=f"{Color.blue}Destination root folder{Color.end}",
                        default=DEFAULT_RES_DIRECTORY,
                        help=f"root folder where the result converted directory will be stored, "
                             f"default is the Desktop ({Color.dark_green}{DEFAULT_RES_DIRECTORY}{Color.end})")
    args = vars(parser.parse_args())
    input_dir = args["input_dir"]
    dest_dir = args["dest_dir"]
    copy_kit_c11_d470(input_dir, dest_dir)


def copy_kit_c11_d470(input_dir, dest_dir):
    result_dir = f"{os.path.split(input_dir)[-1]}_converted"
    full_res_dir = os.path.join(dest_dir, result_dir)
    print(f"\nConverting the CCparameters.csv files from:\n"
          f" {Color.dark_cyan}{input_dir}{Color.end}\n"
          f"to\n"
          f" {Color.dark_cyan}{full_res_dir}{Color.end}\n")
    create_success = create_result_dir(full_res_dir)
    if not create_success:
        print(f"{Color.red}Process aborted{Color.end}\n")
        return
    for train_dir in os.listdir(input_dir):
        full_path = os.path.join(input_dir, train_dir)
        dest_path = os.path.join(full_res_dir, train_dir)
        if os.path.isdir(full_path) and train_dir.startswith(TRAIN_UNIT_PREFIX):
            create_dir(dest_path)
            copy_converted_train_unit(full_path, dest_path)
        else:
            copy_file_or_dir(full_path, dest_path)
    print(f"\nConversion is done, the result folder can be found at:\n"
          f" {Color.green}{full_res_dir}{Color.end}")


def create_result_dir(full_res_dir):
    if os.path.exists(full_res_dir):
        print(f"{bg_color(Color.dark_yellow)}{Color.black}Warning{Color.end}"
              f"{Color.dark_yellow}: the result folder already exists"
              f"\n at {full_res_dir}{Color.end}\n")
        if input(f"{Color.white}Are you sure you want to overwrite it?{Color.end} "
                 f"{Color.dark_cyan}[y/n]{Color.end} ").capitalize() not in ["Y", "YES"]:
            return False
        shutil.rmtree(full_res_dir)
    os.makedirs(full_res_dir)
    return True


def create_dir(dir_path):
    os.mkdir(dir_path)


def copy_file_or_dir(input_path, dest_path):
    if os.path.isdir(input_path):
        shutil.copytree(input_path, dest_path)
    elif os.path.isfile(input_path):
        shutil.copy(input_path, dest_path)


def copy_converted_train_unit(input_path, dest_path):
    for cab_dir in os.listdir(input_path):
        cab_full_path = os.path.join(input_path, cab_dir)
        cab_dest_path = os.path.join(dest_path, cab_dir)
        if os.path.isdir(cab_full_path) and cab_dir.startswith(CAB_DIR_PREFIX):
            create_dir(cab_dest_path)
            copy_converted_cab(cab_full_path, cab_dest_path)
        else:
            copy_file_or_dir(cab_full_path, cab_dest_path)


def copy_converted_cab(input_path, dest_path):
    for ccparam_dir in os.listdir(input_path):
        ccparam_dir_full_path = os.path.join(input_path, ccparam_dir)
        ccparam_dir_dest_path = os.path.join(dest_path, ccparam_dir)
        if os.path.isdir(ccparam_dir_full_path) and ccparam_dir == CC_PARAM_DIR:
            create_dir(ccparam_dir_dest_path)
            copy_converted_ccparam(ccparam_dir_full_path, ccparam_dir_dest_path)
        else:
            copy_file_or_dir(ccparam_dir_full_path, ccparam_dir_dest_path)


def copy_converted_ccparam(input_path, dest_path):
    for ccparam in os.listdir(input_path):
        ccparam_full_path = os.path.join(input_path, ccparam)
        ccparam_dest_path = os.path.join(dest_path, ccparam)
        if os.path.isfile(ccparam_full_path) and ccparam == CC_PARAM_FILE:
            convert_ccparam_file_unix_to_windows(ccparam_full_path, ccparam_dest_path)
        else:
            copy_file_or_dir(ccparam_full_path, ccparam_dest_path)


WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'


def convert_ccparam_file_unix_to_windows(ccparam_full_path, ccparam_dest_path):
    with open(ccparam_full_path, 'rb') as f:
        with open(ccparam_dest_path, 'wb') as dest_f:
            dest_f.write(f.read().replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING))
