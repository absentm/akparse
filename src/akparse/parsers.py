#!/usr/bin/python
# coding:utf-8

import re
import sys
import copy
import getopt

from utils.ak_echo import AkEcho
from errs.ak_error import AkError
from consts.ak_constants import AkConstants


class AkParser:
    """
    Main build
    """
    # Define 0, 1, 2, 3 four state of State Machine to record state switch
    AK_STATE_0 = 0  # 0 -- default original state, NULL
    AK_STATE_1 = 1  # 1 -- single option state, -x
    AK_STATE_2 = 2  # 2 -- Curly bracket state, {}
    AK_STATE_3 = 3  # 3 -- Square bracket state, []

    def __init__(self):
        """
        initiator
        """
        self._short_options = ""
        self._long_options = []
        self._options_list = []
        self._defined_options = []

    def _parse_single_options(self, input_str):
        """
        Parse single options
        :param input_str: one character or one word
        :return:
        """
        if re.match(AkConstants.SHORT_OPTS_PATTERN, input_str):
            if (input_str[1] + ":") in self._short_options:
                # conflict
                AkEcho.ak_err(AkError.ERROR_CONFLICT_MSG)
            elif input_str[1] not in self._short_options:
                self._short_options += input_str[1]

            return input_str
        elif re.match(AkConstants.SHORT_KV_OPTS_PATTERN, input_str):
            if (input_str[1] + ":") not in self._short_options:
                if input_str[1] in self._short_options:
                    # conflict
                    AkEcho.ak_err(AkError.ERROR_CONFLICT_MSG)
                else:
                    self._short_options += (input_str[1] + ":")

            return input_str.strip(AkConstants.EQUAL_SIGN_OPTION)
        elif re.match(AkConstants.LONG_OPTS_PATTERN, input_str):
            if (input_str[2:] + AkConstants.EQUAL_SIGN_OPTION) in self._long_options:
                # conflict
                AkEcho.ak_err(AkError.ERROR_CONFLICT_MSG)
            elif input_str[2:] not in self._long_options:
                self._long_options.append(input_str[2:])

            return input_str
        elif re.match(AkConstants.LONG_KV_OPTS_PATTERN, input_str):
            if input_str[2:-1] in self._long_options:
                # conflict
                AkEcho.ak_err(AkError.ERROR_CONFLICT_MSG)
            elif input_str[2:] not in self._long_options:
                self._long_options.append(input_str[2:])

            return input_str.strip(AkConstants.EQUAL_SIGN_OPTION)

        AkEcho.ak_err(AkError.ERROR_WRONG_KEY_MSG + "%s" % input_str)

    def _parse_bracket_options(self, input_bracket_str):
        """
        Parse mode block in brace
        :param input_bracket_str:
        :return:
        """
        result_list = []
        result_str = ""
        curly_bracket_counter = 0
        square_bracket_counter = 0

        for item in input_bracket_str:
            if item == AkConstants.VERTICAL_LINE_OPTION and curly_bracket_counter == 0 and square_bracket_counter == 0:
                if result_str == "":
                    AkEcho.ak_err(AkError.ERROR_EMPTY_BRANCHES_MSG)
                else:
                    result_list += self._parse_pattern(result_str)
                    result_str = ""
                    curly_bracket_counter = 0
                    square_bracket_counter = 0
            elif item == AkConstants.LEFT_CURLY_BRACKET_OPTION:
                curly_bracket_counter += 1
                result_str += item
            elif item == AkConstants.RIGHT_CURLY_BRACKET_OPTION:
                if curly_bracket_counter <= 0:
                    AkEcho.ak_err(AkError.ERROR_MISMATCHED_PARENTHESES_MSG)

                curly_bracket_counter -= 1
                result_str += item
            elif item == AkConstants.LEFT_SQUARE_BRACKET_OPTION:
                curly_bracket_counter += 1
                result_str += item
            elif item == AkConstants.RIGHT_SQUARE_BRACKET_OPTION:
                if curly_bracket_counter <= 0:
                    AkEcho.ak_err(AkError.ERROR_MISMATCHED_PARENTHESES_MSG)

                curly_bracket_counter -= 1
                result_str += item
            else:
                result_str += item

        if result_str == "":
            AkEcho.ak_err(AkError.ERROR_EMPTY_BRANCHES_MSG)
        else:
            result_list += self._parse_pattern(result_str)

        return result_list

    def _parse_pattern(self, input_str):
        """
        Main parse
        :param input_str:
        :return:
        """
        result_list = [[]]
        pattern_str = ""
        curly_bracket_counter = 0
        square_bracket_counter = 0
        state = AkParser.AK_STATE_0

        for item in input_str:
            if state == AkParser.AK_STATE_0:
                # current state is
                if item == AkConstants.LEFT_CURLY_BRACKET_OPTION:
                    # AK_STATE_0 -> AK_STATE_2
                    curly_bracket_counter += 1
                    state = AkParser.AK_STATE_2
                elif item == AkConstants.LEFT_SQUARE_BRACKET_OPTION:
                    # AK_STATE_0 -> AK_STATE_3
                    square_bracket_counter += 1
                    state = AkParser.AK_STATE_3
                else:
                    # AK_STATE_0 -> AK_STATE_1
                    state = AkParser.AK_STATE_1
                    pattern_str += item
            elif state == AkParser.AK_STATE_1:
                if item == AkConstants.COMMA_OPTION:
                    # AK_STATE_1 -> AK_STATE_0
                    opts = self._parse_single_options(pattern_str)
                    for mode in result_list:
                        mode.append(opts)
                    pattern_str = ""
                    state = AkParser.AK_STATE_0
                elif item == AkConstants.LEFT_CURLY_BRACKET_OPTION:
                    # AK_STATE_1 -> AK_STATE_2
                    opts = self._parse_single_options(pattern_str)
                    for mode in result_list:
                        mode.append(opts)
                    pattern_str = ""
                    curly_bracket_counter += 1
                    state = AkParser.AK_STATE_2
                elif item == AkConstants.LEFT_SQUARE_BRACKET_OPTION:
                    # AK_STATE_1 -> AK_STATE_3
                    opts = self._parse_single_options(pattern_str)
                    for mode in result_list:
                        mode.append(opts)
                    pattern_str = ""
                    square_bracket_counter += 1
                    state = AkParser.AK_STATE_3
                else:
                    pattern_str += item
            elif state == AkParser.AK_STATE_2:
                if item == AkConstants.LEFT_CURLY_BRACKET_OPTION:
                    curly_bracket_counter += 1
                    pattern_str += item
                elif item == AkConstants.RIGHT_CURLY_BRACKET_OPTION:
                    if curly_bracket_counter <= 0:
                        AkEcho.ak_err(AkError.ERROR_MISMATCHED_PARENTHESES_MSG)

                    curly_bracket_counter -= 1
                    if curly_bracket_counter == 0:
                        # AK_STATE_2 -> AK_STATE_0
                        sub_pattern_list = self._parse_bracket_options(pattern_str)
                        tmp_pattern_list = result_list
                        result_list = []
                        for sub_mode in sub_pattern_list:
                            for tmp_mode in tmp_pattern_list:
                                result_list.append(tmp_mode + sub_mode)

                        pattern_str = ""
                        state = AkParser.AK_STATE_0
                    else:
                        pattern_str += item
                else:
                    pattern_str += item
            elif state == AkParser.AK_STATE_3:
                if item == AkConstants.LEFT_SQUARE_BRACKET_OPTION:
                    square_bracket_counter += 1
                    pattern_str += item
                elif item == AkConstants.RIGHT_SQUARE_BRACKET_OPTION:
                    if square_bracket_counter <= 0:
                        AkEcho.ak_err(AkError.ERROR_MISMATCHED_PARENTHESES_MSG)

                    square_bracket_counter -= 1
                    if square_bracket_counter == 0:
                        # AK_STATE_3 -> AK_STATE_0
                        sub_pattern_list = self._parse_pattern(pattern_str)
                        tmp_pattern_list = copy.deepcopy(result_list)
                        for sub_mode in sub_pattern_list:
                            for tmp_mode in tmp_pattern_list:
                                result_list.append(tmp_mode + sub_mode)

                        pattern_str = ""
                        state = AkParser.AK_STATE_0
                    else:
                        pattern_str += item
                else:
                    pattern_str += item

        if state == AkParser.AK_STATE_1:
            # AK_STATE_1 -> AK_STATE_0
            opts = self._parse_single_options(pattern_str)
            for mode in result_list:
                mode.append(opts)
            state = AkParser.AK_STATE_0

        if state != AkParser.AK_STATE_0:
            # State machine stopped with wrong state
            AkEcho.ak_err(AkError.ERROR_STATE_MSG)

        return result_list

    def parse(self, args_list):
        options = None
        args = None

        try:
            options, args = getopt.getopt(args_list, self._short_options, self._long_options)
        except getopt.GetoptError as getopt_err:
            AkEcho.ak_err(AkError.ERROR_PARSE_MSG + "%s" % getopt_err.msg)

        # Has redundant arguments?
        if len(args) != 0:
            AkEcho.ak_err(AkError.ERROR_REDUNDANT_MSG + "%s" % args)

        # Has duplicate arguments?
        key_list = [k for k, v in options]
        if len(key_list) != len(set(key_list)):
            AkEcho.ak_err(AkError.ERROR_DUPLICATE_ARGS_MSG)

        # Check input keys is defined
        for flag_name, flag_key_list in self._options_list:
            self._defined_options += flag_key_list

        for item in args_list:
            if str(item).startswith("-") and str(item) not in self._defined_options:
                AkEcho.ak_err(AkError.ERROR_WRONG_KEY_MSG + "%s" % str(item))

        # Match pattern
        for flag_name, flag_key_list in self._options_list:
            if set(flag_key_list) == set(key_list):
                return flag_name, options

        AkEcho.ak_err(AkError.ERROR_NOT_MATCH_MSG)

    def add(self, flag_name, input_str):
        """
        Add command option
        :param flag_name:
        :param input_str:
        :return:
        """
        if not isinstance(flag_name, str) or not isinstance(input_str, str):
            AkEcho.ak_err(AkError.ERROR_INPUT_MSG)

        # Has special character?
        if re.findall(AkConstants.SUPPORT_KEYWORDS_PATTERN, input_str):
            AkEcho.ak_err(AkError.ERROR_INPUT_MSG)

        # Parse and save pattern list
        result_list = self._parse_pattern(input_str)
        for item in result_list:
            self._options_list.append([flag_name, item])

    def remove(self, flag_name, input_str):
        """
        Remove command option
        :param flag_name:
        :param input_str:
        :return:
        """
        if not isinstance(flag_name, str) or not isinstance(input_str, str):
            AkEcho.ak_err(AkError.ERROR_INPUT_MSG)

        # Has special character?
        if re.findall(AkConstants.SUPPORT_KEYWORDS_PATTERN, input_str):
            AkEcho.ak_err(AkError.ERROR_INPUT_MSG)

        # Parse and save mode list
        result_list = self._parse_pattern(input_str)
        for item in result_list:
            self._options_list.remove([flag_name, item])

    def clear(self):
        """
        Clear options list
        :return:
        """
        del self._options_list[:]


if __name__ == "__main__":
    flag_names = None
    flag_options = None

    try:
        file_parser = AkParser()
        file_parser.add("help", "{-h|--help}")
        file_parser.add("file_create", "--create,-p=[--user=,-a=]")
        file_parser.add("file_query", "--query[{-p=|--service}]")
        file_parser.add("file_set", "--set{-p=,--user=,-a=|--limit=}")
        file_parser.add("file_delete", "--delete,-p=[--user=]")
        file_parser.add("file_start", "--start")
        file_parser.add("file_stop", "--stop")
        file_parser.add("file_status", "--status")
        flag_names, flag_options = file_parser.parse(sys.argv[1:])
    except AkError as err:
        AkEcho.ak_err(AkError.ERROR_PARSE_MSG + err.msg)

    # Print parse result
    AkEcho.ak_echo(flag_names)
    AkEcho.ak_echo(flag_options)
