#!/usr/bin/env python3
""" Tool for parse logcat file """

import argparse
import sys
import subprocess
from subprocess import PIPE
from collections import defaultdict
from fuzzystring.fuzzystring import FuzzyString
from fuzzyhash.soundexhash import SoundexHash
from logparser.logparser import parse_log_line, contain_tag, ParseLogLineFailed


def filter_logs_from_file(filename, tags, levels):
    """ Filter log file

    :param: str: filename: logcat file filename
    :param: str: tags: tags to filter
    :param: str: levels: levels to filter
    """
    logs = []
    with open(filename, mode='r', encoding='utf-8') as logfile_fd:
        for line in logfile_fd:
            try:
                _, _, _, _, level, tag, message = parse_log_line(line)
            except ParseLogLineFailed:
                continue
            if contain_tag(tag, tags) and level.lower() in levels:
                logs.append(f'{level} {tag} {message.strip()}')
    return logs


def count_logs(fuzzy_hash, logs):
    """ Count how many times each log occurs in the logcat

    :param: FuzzyHash: fuzzy_hash: fuzzy hash
    :param: str[] logs: list with logs
    :return: dict: map with log line and count
    """
    count = defaultdict(int)

    for log_line in logs:
        count[FuzzyString(fuzzy_hash, log_line)] += 1
    return count


def print_log_counts(logs_count, ignore_less_than):
    """ Sort and print log lines and count

    output:
    [<log count>]: <log line>

    :param: int: ignore_less_than: ignore less than N occurs
    :param: dict: logs_count: map with log line and count
    :return: None
    """
    for key in sorted(logs_count, key=logs_count.get, reverse=True):
        if logs_count[key] >= ignore_less_than:
            print(f"[{logs_count[key]}]: {key}")


def print_log_counts_adb(fuzzy_hash, tags, levels, ignore_less_than):
    """ Sort and print log lines and count from connected adb device

    output:
    [<log count>]: <log line>

    :param: FuzzyHash: fuzzy_hash: Fuzzy hashing engine
    :param: str[]: tags: Filter output by specified tags(s)
    :param: str[]: levels: Filter output by specified log level(s)
    :param: int: ignore_less_than: ignore less than N occurs
    :return: None
    """
    adb = subprocess.Popen(['adb', 'logcat'],
                           stdin=PIPE,
                           stdout=PIPE,
                           stderr=PIPE)
    logs_count = defaultdict(int)
    while True:
        try:
            line = adb.stdout.readline().decode('utf-8', 'replace').strip()
            _, _, _, _, level, tag, message = parse_log_line(line)
            if len(line) == 0:
                break
            if contain_tag(tag, tags) and level.lower() in levels:
                logs_count[FuzzyString(fuzzy_hash,
                                       f'{level} {tag} {message.strip()}')] += 1
                print('\033c', end='')
                print_log_counts(logs_count, ignore_less_than)
        except KeyboardInterrupt:
            print_log_counts(logs_count, ignore_less_than)
            break
        except ParseLogLineFailed:
            continue


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

    ignore_less_than = 4
    soundex_hash = SoundexHash()
    if args.input_file:
        logs_count = count_logs(
            soundex_hash,
            filter_logs_from_file(args.input_file, tags, levels)
        )
        print_log_counts(logs_count, ignore_less_than)
        return 0
    print_log_counts_adb(soundex_hash, tags, levels, ignore_less_than)
    return 0


if __name__ == '__main__':
    sys.exit(main())
