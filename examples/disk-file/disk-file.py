#!/usr/bin/python
# coding:utf-8

import os
import sys

from akparse.parsers import AkParser
from akparse.utils.ak_echo import AkEcho
from akparse.errs.ak_error import AkError


def query_disk_files(dir_name=None):
    """
    query_disk_files
    :param dir_name:
    :return:
    """
    if not dir_name:
        dir_name = os.getcwd()

    ls_dir = os.listdir(dir_name)
    dirs = [i for i in ls_dir if os.path.isdir(os.path.join(dir_name, i))]
    files = [i for i in ls_dir if os.path.isfile(os.path.join(dir_name, i))]

    if files:
        for f in files:
            AkEcho.ak_echo(os.path.join(dir_name, f))

    if dirs:
        for d in dirs:
            query_disk_files(os.path.join(dir_name, d))  # 递归查找


def query_file_status(dir_name, show_json=None):
    result = os.path.exists(dir_name)
    if show_json:
        ret_dic = {
            "file_name": dir_name,
            "status": result
        }
        AkEcho.ak_json(ret_dic)
    else:
        AkEcho.ak_echo("file name: %s" % dir_name)
        AkEcho.ak_echo("status: %s" % result)


if __name__ == '__main__':

    flag_name = None
    flag_options = None

    dir_path = None
    json_flag = False

    try:
        disk_file_parser = AkParser()
        disk_file_parser.add("file_help", "{-h|--help}")
        disk_file_parser.add("file_create", "--create,-p=[--user=,-a=]")
        disk_file_parser.add("file_query", "--query[{-p=|--list}]")
        disk_file_parser.add("file_rename", "--rename,-p=,--new-name=")
        disk_file_parser.add("file_delete", "--delete,-p=")
        disk_file_parser.add("file_status", "--status,-p=[--json]")
        flag_name, flag_options = disk_file_parser.parse(sys.argv[1:])
    except AkError as err:
        AkEcho.ak_err(AkError.ERROR_PARSE_MSG + err.msg)

    # Print parse result
    AkEcho.ak_echo(flag_name)
    AkEcho.ak_echo(flag_options)

    # Parse opts
    for k, v in flag_options:
        if k == '-p':
            dir_path = v
        elif k == '--json':
            json_flag = True
    if flag_name == "file_help":
        help_file_path = os.getcwd() + "/.helps/." + os.path.basename(__file__).split(".py")[0] + ".help"
        AkEcho.ak_help(help_file_path)
    elif flag_name == "file_query":
        query_disk_files(dir_name=dir_path)
    elif flag_name == "file_status":
        query_file_status(dir_path, json_flag)
