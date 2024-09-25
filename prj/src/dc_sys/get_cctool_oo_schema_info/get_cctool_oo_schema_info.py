#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from ...utils import *
from ...database_location import *
from .get_compatible_cctool_oo_version import *
from .load_cctool_oo_schema import *
from .load_cctool_oo_schema.load_xl import *


__all__ = ["get_corresponding_cctool_oo_schema", "load_cctool_oo_schema_info", "load_cctool_oo_enum_lists_info",
           "get_cctool_oo_version_info", "create_header_for_the_generated_files"]


CCTOOL_OO_SCHEMA_DIR = r"C:\Users\naderc\Documents\Documents GA\CCTool-OO Schema"

REVISION_SHEET = "Revision"


def load_cctool_oo_schema_info(cctool_oo_file: str):
    if cctool_oo_file is None:
        return dict()
    info_dict = load_cctool_oo_schema(cctool_oo_file)
    return info_dict


def load_cctool_oo_enum_lists_info(cctool_oo_file: str):
    if cctool_oo_file is None:
        return dict()
    info_dict = load_cctool_oo_enum_lists(cctool_oo_file)
    return info_dict


def get_corresponding_cctool_oo_schema():
    if DATABASE_LOC.cctool_oo_schema != "":
        return DATABASE_LOC.cctool_oo_schema

    version = get_cctool_oo_name()
    for file in os.listdir(CCTOOL_OO_SCHEMA_DIR):
        full_path = os.path.join(CCTOOL_OO_SCHEMA_DIR, file)
        file, ext = os.path.splitext(file)
        if os.path.isfile(full_path) and ext == ".xls":
            if file.endswith(version):
                return full_path
    print_error(f"Unable to find the CCTool-OO Schema file for version {version} in directory {CCTOOL_OO_SCHEMA_DIR}")
    sys.exit(1)


def get_cctool_oo_version_info(cctool_oo_file: str) -> tuple[str, str]:
    wb = load_cctool_oo_schema_wb(cctool_oo_file)
    revision_sh = wb.sheet_by_name(REVISION_SHEET)
    for row in range(get_xl_number_of_rows(revision_sh) + 1, 0, -1):
        revision = get_xl_cell_value(revision_sh, row=row, column=1)
        comments = get_xl_cell_value(revision_sh, row=row, column=4)
        if revision is not None:
            return revision, comments
    return "", ""


def create_header_for_the_generated_files(cctool_oo_file: str, file_description: str) -> str:
    header = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n"
    max_len = 96
    header += "\n# " + "-" * max_len + " #\n# "
    header += " #\n# ".join(split_text_to_match_max_length(file_description, max_len))
    header += " #\n# " + "-" * max_len + " #\n# "
    revision, comments = get_cctool_oo_version_info(cctool_oo_file)
    header += " #\n# ".join(split_text_to_match_max_length("Revision: " + revision, max_len))
    header += " #\n# "
    header += " #\n# ".join(split_text_to_match_max_length("Comments: " + comments, max_len))
    header += " #\n# " + "-" * max_len + " #\n"
    return header


def split_text_to_match_max_length(text: str, max_len: int) -> list[str]:
    lines = list()
    for line in text.splitlines():
        lines.extend(split_line_to_match_max_length(line, max_len))
    return lines


def split_line_to_match_max_length(line: str, max_len: int) -> list[str]:
    file_description_split = line.split()
    lines = list()
    current_line = str()
    for word in file_description_split:
        if len(current_line) + 1 + len(word) > max_len:  # if the word is added, the length of the line is too large
            lines.append(current_line + " " * (max_len-len(current_line)))
            current_line = str()
        else:
            if not current_line:
                current_line = word
            else:
                current_line += " " + word
    if current_line:
        lines.append(current_line + " " * (max_len-len(current_line)))
    return lines
