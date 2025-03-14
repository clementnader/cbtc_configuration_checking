#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["html_start", "html_end", "html_h1", "html_h2"]


def html_start(title: str, author: str = None, description: str = None, additional_style: str = "") -> str:
    html_code = "<!DOCTYPE html>\n"
    html_code += "<html>\n"
    html_code += html_head(title, author, description, additional_style)
    html_code += "<body>\n\n"
    return html_code


def html_end() -> str:
    html_code = "\n</body>\n"
    html_code += "</html>\n"
    return html_code


def html_h1(header: str) -> str:
    return f"<h1>{header}</h1>\n"


def html_h2(sub_header: str) -> str:
    return f"<h2>{sub_header}</h2>\n"


def html_head(title: str, author: str = None, description: str = None, additional_style: str = "") -> str:
    html_text = f"<head>\n\n"
    html_text += f"\t<meta charset=\"UTF-8\">\n"
    html_text += f"\t<title>{title}</title>\n"
    if description is not None:
        html_text += f"\t<meta name=\"description\" content=\"{description}\"\n>"
    if author is not None:
        html_text += f"<\tmeta name=\"author\" content=\"{author}\"\n>"
    html_text += html_style(additional_style)
    html_text += "\n</head>\n\n"
    return html_text


def html_style(additional_style: str) -> str:
    html_code = "\t<style type=\"text/css\">\n"
    html_code += "h1 {font-size: 24px; font-weight: bold; color: #000080;}\n"
    html_code += "h2 {font-size: 16px; font-weight: bold; color: #000080;}\n"
    html_code += "table {border: 0px solid #565656; border-collapse: collapse;}"
    html_code += "tr {border: 0px solid #000000;}\n"
    html_code += "th {border: 1px solid #565656; font-weight: bold; width: 15%;}\n"
    html_code += "td {border: 1px solid #565656;}\n"
    html_code += "p {color: #000000;}\n"
    html_code += additional_style
    html_code += "\t</style>\n"
    return html_code
