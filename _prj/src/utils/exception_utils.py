#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["UnableToSaveFileException",
           "UnknownExcelWorkbookType", "UnknownExcelWorksheetType"]


class UnableToSaveFileException(Exception):
    pass


class UnknownExcelWorkbookType(Exception):
    pass


class UnknownExcelWorksheetType(Exception):
    pass
