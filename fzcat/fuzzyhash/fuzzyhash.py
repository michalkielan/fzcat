#
# file fuzzyhash.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

""" Fuzzy hash and compare interface """

from abc import ABCMeta, abstractmethod


class FuzzyHash(metaclass=ABCMeta):
    """Fuzzy hash and compare class"""

    @abstractmethod
    def compare(self, lhs, rhs):
        """Fuzzy compare two strings"""

    @abstractmethod
    def hash(self, data):
        """Calculate fuzzy hash"""
