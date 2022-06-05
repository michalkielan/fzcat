#
# file fuzzystring.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

""" Fuzzy hashing object """

from fzcat.fuzzyhash.fuzzyhash import FuzzyHash


class FuzzyString:
    """ Fuzzy hashing string """

    def __init__(self, fuzzy_hash: FuzzyHash, data: str):
        self.data = data
        self.fuzzy_hash = fuzzy_hash

    def __str__(self):
        return self.data

    def __eq__(self, other):
        return self.fuzzy_hash.compare(self.data, other.data)

    def __hash__(self):
        return self.fuzzy_hash.hash(self.data)
