#!/usr/bin/python
# coding:utf-8

class AkError(Exception):
    opt = ''
    msg = ''

    # Error msg
    ERROR_CONFLICT_MSG = "ERROR: Conflict with existing argument"
    ERROR_EMPTY_BRANCHES_MSG = "ERROR: There are empty independent branches in parentheses"
    ERROR_MISMATCHED_PARENTHESES_MSG = "ERROR: Mismatched parentheses"
    ERROR_WRONG_KEY_MSG = "ERROR: Wrong option key, "
    ERROR_STATE_MSG = "ERROR: The state has not been restored"
    ERROR_DUPLICATE_ARGS_MSG = "ERROR: Duplicate arguments"
    ERROR_NOT_MATCH_MSG = "ERROR: No matching CLI patterns were found"
    ERROR_REDUNDANT_MSG = "ERROR: Redundant arguments"
    ERROR_PARSE_MSG = "ERROR: Parse error, "
    ERROR_INPUT_MSG = "ERROR: Illegal pattern string, Only: '-', '--', ',', '|', '{', '}', '[', ']', '=' and character"

    def __init__(self, msg, opt=''):
        self.msg = msg
        self.opt = opt
        Exception.__init__(self, msg, opt)

    def __str__(self):
        return self.msg
