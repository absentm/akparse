#!/usr/bin/python
# coding:utf-8


class AkConstants:
    """
    AkParser Constants set
    """

    def __init__(self):
        pass

    # -xxx or -xxx=
    SHORT_OPTS_PATTERN = r"^-[a-zA-Z]$"
    SHORT_KV_OPTS_PATTERN = r"^-[a-zA-Z]=$"

    # --xxx or --xxx=
    LONG_OPTS_PATTERN = r"^--[a-zA-Z][a-zA-Z_-]+$"
    LONG_KV_OPTS_PATTERN = r"^--[a-zA-Z][a-zA-Z_-]+=$"
    SUPPORT_KEYWORDS_PATTERN = r"[^a-zA-Z0-9{|}\[\],=_-]+"

    # Reserved keywords
    COMMA_OPTION = ","
    EQUAL_SIGN_OPTION = "="
    VERTICAL_LINE_OPTION = "|"
    SHORT_HORIZONTAL_LINE_OPTION = "-"
    LONG_HORIZONTAL_LINE_OPTION = "--"

    LEFT_SQUARE_BRACKET_OPTION = "["
    RIGHT_SQUARE_BRACKET_OPTION = "]"
    LEFT_CURLY_BRACKET_OPTION = "{"
    RIGHT_CURLY_BRACKET_OPTION = "}"
