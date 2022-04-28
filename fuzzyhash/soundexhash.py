""" Soundex hash and compare implementation """

from soundex import Soundex
from fuzzyhash.fuzzyhash import FuzzyHash


class SoundexHash(FuzzyHash):
    """ Soundex hashing class using soundex algorithm """

    def __init__(self):
        self.__soundex = Soundex()

    def compare(self, lhs, rhs):
        """ Compare soundex of given strings

        :param: str: lhs: first string for comparison
        :param: str: rhs: second string for comparison
        :return: bool: True if strings are same or phonetically same
        """
        if self.__soundex.compare(lhs, rhs) != -1:
            return True
        return False

    def hash(self, data):
        """ Create a hash from soundex of given string

        :param: str: string whose hash to be calculated
        :return: int: hash of `data`
        """
        return hash(self.__soundex.soundex(data))
