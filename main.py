#!/usr/bin/env python3
""" Tool for parse logcat file """

import argparse
import sys
from logcount.logcount import count_logs
from fuzzyhash.soundexhash import SoundexHash


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
        required=True)
    parser.add_argument(
        '-t',
        '--tags',
        nargs='+',
        help='Filter output by specified tags(s)',
        required=True)
    args = parser.parse_args()
    tags = [tag.lower() for tag in args.tags]
    levels = [level.lower() for level in args.log_levels]

    return count_logs(args.input_file, tags, levels, 4, SoundexHash())


if __name__ == '__main__':
    sys.exit(main())
