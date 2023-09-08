#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess


__all__ = ["open_file_app"]


def open_file_app(file_path):
    subprocess.call(file_path, shell=True)
