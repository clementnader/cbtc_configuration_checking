#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["UnableToSaveFileException", "UnknownControlTablesType"]


class UnableToSaveFileException(Exception):
    pass


class UnknownControlTablesType(Exception):
    pass
