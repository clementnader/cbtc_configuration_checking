#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from .colored_output import remove_colors


__all__ = ["Logger"]


class Logger:
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log = log_file

    def write(self, message):
        self.terminal.write(message)
        self.log.write(remove_colors(message))

    def flush(self):
        pass
