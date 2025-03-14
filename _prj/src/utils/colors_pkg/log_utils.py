#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from .colored_output import remove_colors


__all__ = ["Logger"]


# Create a Logger class to be able to write the logs inside terminal and at the same time, write them into a log file.
# User has to initialize sys.stdout = Logger(log_file_instance) so that the prints (that uses sys.stdout.write()) are
# both printed on the terminal (using the default sys.stdout.write()) and written in the log file.
class Logger:
    def __init__(self, log_file):
        # Initialization: the default sys.stdout is kept as the terminal, and we store the file instance.
        self.terminal = sys.stdout
        self.log = log_file

    def write(self, message):
        # When a print is used, we both print the info on the terminal and write the info in the log file.
        self.terminal.write(message)
        self.log.write(remove_colors(message))  # We remove the colors characters used to show colors on the terminal.

    def flush(self):
        self.terminal.flush()
