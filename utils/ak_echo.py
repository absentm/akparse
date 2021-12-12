#!/usr/bin/python
# coding:utf-8

import sys


class AkEcho:
    echo_msg = ''

    def __init__(self, echo_msg):
        self.echo_msg = echo_msg

    def __str__(self):
        return self.echo_msg

    @staticmethod
    def ak_err(err_msg):
        sys.stderr.write(err_msg)
        sys.stderr.write("\n")
        sys.exit(1)

    @staticmethod
    def ak_echo(echo_msg):
        print(echo_msg)
