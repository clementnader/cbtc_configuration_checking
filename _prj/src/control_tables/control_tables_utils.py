#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["CONTROL_TABLE_TYPE",
           "ROUTE_NAME_KEY", "ROUTE_ORIGIN_SIGNAL_KEY", "ROUTE_IVB_LIST_KEY", "ROUTE_SWITCHES_LIST_KEY",
           "OVERLAP_NAME_KEY", "OVERLAP_SIGNAL_NAME_KEY", "OVERLAP_IVB_LIST_KEY", "OVERLAP_SWITCHES_LIST_KEY"]


class CONTROL_TABLE_TYPE:
    route = "route"
    overlap = "overlap"


ROUTE_NAME_KEY = "Route Name"
ROUTE_ORIGIN_SIGNAL_KEY = "Origin Signal"
ROUTE_IVB_LIST_KEY = "Route IVB List"
ROUTE_SWITCHES_LIST_KEY = "Switches List"

OVERLAP_NAME_KEY = "Interlocking Overlap Name"
OVERLAP_SIGNAL_NAME_KEY = "Signal Name"
OVERLAP_IVB_LIST_KEY = "Overlap IVB List"
OVERLAP_SWITCHES_LIST_KEY = "Switches List"
