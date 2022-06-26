#
# file logparser.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

""" Logcat parser helpers """

import re


LOG_LINE = re.compile(r"(.\S*) *(.\S*) *(\d*) *(\d*) *([A-Z]) *([^:]*): *(.*?)$")


class ParseLogLineFailed(Exception):
    """Raises when line is not logcat log"""


def parse_log_line(line):
    """Parse log line

    :raises ParseLogLineFailed: log line parse failed
    :param: str: line: line from logcat
    :return: str[]: date, time, process, thread, level, tag, message
    """
    log_line = LOG_LINE.match(line)
    if log_line is None:
        raise ParseLogLineFailed(f"This is not a valid log line: {line}")
    return log_line.groups()


def contain_tag(log_tag, tags):
    """Check if logcat tag is in the filter tags

    :param: str: log_tag: tag from logcat line
    :param: str[]: tags: ignore log if tag is not on the list
    :return: bool: True if tag is within the tags list or list is empty,
        False otherwise
    """
    if not tags:
        return True
    for tag in tags:
        if tag.lower() in log_tag.lower():
            return True
    return False
