""" Fuzzy hash and compare interface """

from abc import ABCMeta, abstractmethod


class FuzzyHash(metaclass=ABCMeta):
    """ Fuzzy hash and compare class """

    @abstractmethod
    def compare(self, lhs, rhs):
        """ Fuzzy compare two strings """

    @abstractmethod
    def hash(self, data):
        """ Calculate fuzzy hash """
