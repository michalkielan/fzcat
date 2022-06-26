#
# file test_logcount.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

""" Test for logcat count """

import pytest
from fzcat.logcount.logcount import count_logs_occurrence
from fzcat.fuzzyhash.soundexhash import SoundexHash
from fzcat.fuzzystring.fuzzystring import FuzzyString

FUZZY_HASH = SoundexHash()

DUMMY_LOGCAT = [
    "06-01 12:44:10.07 8898 8898 E dummyTag: lLk42vFjpOEfuF4blzfM",
    "06-01 12:44:10.07 8898 8898 E dummyTag: fK4lkF0Bgl1LP09Mv1YY",
    "06-01 12:44:10.07 8898 8898 E dummyTag: tKfzpZHwfjuP04VHF6K3",
    "06-01 12:44:10.07 8898 8898 E dummyTag: tKfzpZHwfjuP04VHF6K3",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
    "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr",
]

DUMMY_EXPECTED = {
    FuzzyString(
        FUZZY_HASH, "06-01 12:44:10.07 8898 8898 E dummyTag: lLk42vFjpOEfuF4blzfM"
    ): 1,
    FuzzyString(
        FUZZY_HASH, "06-01 12:44:10.07 8898 8898 E dummyTag: fK4lkF0Bgl1LP09Mv1YY"
    ): 1,
    FuzzyString(
        FUZZY_HASH, "06-01 12:44:10.07 8898 8898 E dummyTag: tKfzpZHwfjuP04VHF6K3"
    ): 2,
    FuzzyString(
        FUZZY_HASH, "06-01 12:44:10.07 8898 8898 E dummyTag: DbAleFBEhTdu4cfsSOTr"
    ): 10,
}


@pytest.mark.parametrize("logcat", [DUMMY_LOGCAT])
@pytest.mark.parametrize("expected", [DUMMY_EXPECTED])
def test_count_log_occurrence(logcat, expected):
    """Test count log occurrences"""
    assert expected == count_logs_occurrence(FUZZY_HASH, logcat)
