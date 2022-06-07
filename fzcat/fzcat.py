#
# file fzcat.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

""" Tool for parse logcat file """

import argparse
from fzcat.logcount.logcount import count_logs
from fzcat.fuzzyhash.soundexhash import SoundexHash


def main():
    """ main """
    parser = argparse.ArgumentParser(usage="""
Tool for parsing logcat files

Get logs from logcat file:
$ ./main.py -i logcat.log -l E W -t OMX libjingle

Get logs from adb device:
$ ./main.py -l E W -t OMX libjingle

""")
    parser.add_argument('-i', '--input-file', type=str)
    parser.add_argument(
        '-l',
        '--log-levels',
        nargs='+',
        help='Filter output by specified log level(s)',
        default=['S', 'F', 'E', 'W', 'I', 'D', 'V'],
        required=False)
    parser.add_argument(
        '-t',
        '--tags',
        nargs='+',
        help='Filter output by specified tags(s)',
        default=[],
        required=False)
    args = parser.parse_args()
    tags = [tag.lower() for tag in args.tags]
    levels = [level.lower() for level in args.log_levels]

    return count_logs(args.input_file, tags, levels, 4, SoundexHash())
