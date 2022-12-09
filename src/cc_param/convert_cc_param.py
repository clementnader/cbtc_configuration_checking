#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .cc_param_utils import *
import os
import shutil

INPUT_DIRECTORY = r"C:\Users\naderc\Desktop\ML4_TF3_C11_D470_06_05_05_V03\ML4_TF3_C11_D470_06_05_05_V03"
RESULT_DIRECTORY = r"C:\Users\naderc\Desktop"


def convert_cc_param_files():
    result_dir = f"{os.path.split(INPUT_DIRECTORY)[-1]}_converted"
    full_res_dir = os.path.join(RESULT_DIRECTORY, result_dir)
    create_success = create_result_dir(full_res_dir)
    if not create_success:
        print("Process aborted")
        return
    for train_dir in os.listdir(INPUT_DIRECTORY):
        full_path = os.path.join(INPUT_DIRECTORY, train_dir)
        dest_path = os.path.join(full_res_dir, train_dir)
        if os.path.isdir(full_path) and train_dir.startswith(TRAIN_UNIT_PREFIX):
            create_dir(dest_path)
            copy_converted_train_unit(full_path, dest_path)
        else:
            copy_file_or_dir(full_path, dest_path)


def create_result_dir(full_res_dir):
    if os.path.exists(full_res_dir):
        print(f"Warning old a folder already exists"
              f"\n at {full_res_dir}")
        if input("Do you want to continue? [y/n] ").capitalize() not in ["Y", "YES"]:
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
            convert_cc_param(ccparam_full_path, ccparam_dest_path)
        else:
            copy_file_or_dir(ccparam_full_path, ccparam_dest_path)


WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'


def convert_cc_param(ccparam_full_path, ccparam_dest_path):
    with open(ccparam_full_path, 'rb') as f:
        with open(ccparam_dest_path, 'wb') as dest_f:
            dest_f.write(f.read().replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING))
