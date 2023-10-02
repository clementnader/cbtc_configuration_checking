#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["additional_css_style"]


def additional_css_style():
    html_code = "div.view  {width: 100%; overflow-x: scroll; white-space: nowrap;}\n"
    html_code += "table.diff-table {overflow: hidden;}\n"
    html_code += "th, td {position: relative;}\n"
    html_code += "tr:hover {background: #EEEEFF;}\n"
    html_code += "tr.headline:hover {background: #FFFFFF;}\n"  # deactivate hover for headline
    html_code += "th:hover, td:hover {background: #CCCCFF;}\n"
    html_code += "th:not(.sticky):hover::after, td:hover::after {background: #EEEEFF; " \
                 "content: ''; position: absolute; left: 0; top: -5000px; width: 100%; height: 10000px; z-index: -1;}\n"
    return html_code
