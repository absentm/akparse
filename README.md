# akparse package

A simple and easy-to-use CLI parse tool package. You can use '-', '--', ',', '|', '{', '}', '[', ']', '=' and character
to define your CLI API and the constraints are as follows:

* '-' : indicate a short option, followed by a character usually.
* '--': indicate a long option, followed by a word usually.
* ',' : indicate a required option of one CLI API defined.
* '|' : indicate a parallel option of one CLI API defined with same prefix.
* '{}': indicate the parallel option, always with '|' together.
* '[]': indicate the optional option.
* '=' : indicate the k-v option.

eg, one disk-file API:

```shell
# create a disk file when be defined: --create,-p=[--user=,-a=]
disk-file --create -p file_path
disk-file --create -p file_path --user u1 -a 777

# query a disk file  when be defined: --query[{-p=|--list}]
disk-file --query
disk-file --query -p file_path
disk-file --query --list

```

# usage

```python
import sys

from akparse.parsers import AkParser
from akparse.utils.ak_echo import AkEcho
from akparse.errs.ak_error import AkError

flag_name = None
flag_options = None

try:
    file_parser = AkParser()
    file_parser.add("help", "{-h|--help}")
    file_parser.add("file_create", "--create,-p=[--user=,-a=]")
    file_parser.add("file_query", "--query[{-p=|--list}]")
    file_parser.add("file_set", "--set{-p=,--user=,-a=|--limit=}")
    file_parser.add("file_delete", "--delete,-p=[--user=]")
    file_parser.add("file_status", "--status")
    flag_name, flag_options = file_parser.parse(sys.argv[1:])
except AkError as err:
    AkEcho.ak_err(AkError.ERROR_PARSE_MSG + err.msg)

# Print parse result
AkEcho.ak_echo(flag_name)
AkEcho.ak_echo(flag_options)
```

**Please see more detail usage in examples**
