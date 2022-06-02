""" Log count """

import os
import subprocess
import tqdm
from subprocess import PIPE
from collections import defaultdict
from fuzzystring.fuzzystring import FuzzyString
from fuzzyhash.fuzzyhash import FuzzyHash
from logparser.logparser import parse_log_line, contain_tag, ParseLogLineFailed


def filter_logs_from_file(filename, tags, levels):
    """ Filter log file

    :param: str: filename: logcat file filename
    :param: str: tags: tags to filter
    :param: str: levels: levels to filter
    """
    logs = []
    with tqdm.tqdm(total=os.path.getsize(filename), desc='Open file ') as pbar:
        with open(filename, mode='r', encoding='utf-8') as logfile_fd:
            for line in logfile_fd:
                pbar.update(len(line))
                try:
                    _, _, _, _, level, tag, message = parse_log_line(line)
                except ParseLogLineFailed:
                    continue
                if contain_tag(tag, tags) and level.lower() in levels:
                    logs.append(f'{level} {tag} {message.strip()}')
    return logs


def count_logs_occurrence(fuzzy_hash, logs):
    """ Count how many times each log occurs in the logcat

    :param: FuzzyHash: fuzzy_hash: fuzzy hash
    :param: str[] logs: list with logs
    :return: dict: map with log line and count
    """
    count = defaultdict(int)

    with tqdm.tqdm(total=len(logs), desc='Count logs') as pbar:
        for log_line in logs:
            pbar.update(1)
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
    with subprocess.Popen(
            ['adb', 'logcat'],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE) as adb_logcat:
        logs_count = defaultdict(int)
        while True:
            try:
                line = (
                    adb_logcat
                    .stdout
                    .readline()
                    .decode('utf-8', 'replace')
                    .strip()
                )
                _, _, _, _, level, tag, message = parse_log_line(line)
                if len(line) == 0:
                    break
                if contain_tag(tag, tags) and level.lower() in levels:
                    logs_count[
                        FuzzyString(
                            fuzzy_hash,
                            f'{level} {tag} {message.strip()}'
                        )
                    ] += 1
                    print('\033c', end='')
                    print_log_counts(logs_count, ignore_less_than)
            except KeyboardInterrupt:
                print_log_counts(logs_count, ignore_less_than)
                break
            except ParseLogLineFailed:
                continue


def count_logs(input_file, tags, levels, ignore_less_than,
               fuzzy_hash: FuzzyHash):
    """ Sort and print log lines and count from connected adb device

    output:
    [<log count>]: <log line>

    :param: str: input_file: Input logcat file
    :param: str[]: tags: Filter output by specified tags(s)
    :param: str[]: levels: Filter output by specified log level(s)
    :param: int: ignore_less_than: ignore less than N occurrences
    :param: FuzzyHash: fuzzy_hash: Fuzzy hashing engine
    :return: 0 if success, otherwise error code
    """
    if input_file:
        logs_count = count_logs_occurrence(
            fuzzy_hash,
            filter_logs_from_file(input_file, tags, levels)
        )
        print_log_counts(logs_count, ignore_less_than)
        return 0
    print_log_counts_adb(fuzzy_hash, tags, levels, ignore_less_than)
    return 0
