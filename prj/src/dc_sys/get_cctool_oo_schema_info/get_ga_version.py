#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .create_cctool_oo_schema_info_file import *

__all_ = ["get_ga_version", "get_ga_version_text"]


def get_ga_version() -> tuple[int]:
    cctool_oo_schema_info = get_version_of_cctool_oo_schema_python_file()
    revision = cctool_oo_schema_info.split("Revision: ", 1)[1].split("Comments: ", 1)[0].strip()
    revision_list = [int(rev.strip()) for rev in revision.split("/")]
    revision_list += [0 for _ in range(4 - len(revision_list))]
    return tuple(revision_list)


def get_ga_version_text() -> str:
    return "-".join([f"{a:02}" for a in get_ga_version()])
