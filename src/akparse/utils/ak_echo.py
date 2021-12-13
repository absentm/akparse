#!/usr/bin/python
# coding:utf-8

import os
import sys
import json


class AkEcho:
    echo_msg = ''

    def __init__(self, echo_msg):
        self.echo_msg = echo_msg

    def __str__(self):
        return self.echo_msg

    @staticmethod
    def ak_err(err_msg):
        """
        ak_err
        :param err_msg:
        :return:
        """
        sys.stderr.write(err_msg)
        sys.stderr.write("\n")
        sys.exit(1)

    @staticmethod
    def ak_echo(echo_msg):
        """
        ak_echo
        :param echo_msg:
        :return:
        """
        print(echo_msg)

    @staticmethod
    def ak_json(json_src):
        """
        ak_json
        :param json_src:
        :return:
        """
        if not isinstance(json_src, dict):
            AkEcho.ak_err("ERROR: Input must be dict type!")
        else:
            AkEcho.ak_echo(json.dumps(json_src))

    @staticmethod
    def ak_file(file_name):
        """
        ak_file
        :param file_name:
        :return:
        """
        lines = []
        if os.path.isfile(file_name):
            with open(file_name, 'r') as fp:
                lines = fp.readlines()

        for line in lines:
            AkEcho.ak_echo(line)

    @staticmethod
    def ak_help(file_name=None):
        """
        ak_help
        :param file_name:
        :return:
        """
        AkEcho.ak_file(file_name)
