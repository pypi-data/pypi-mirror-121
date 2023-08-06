import unittest

from unittest_kana_text_01 import UnittestKanaText
from unittest_kana_text_02 import UnittestKanaIndexer

def suites():
    suites = unittest.TestSuite()
    suites.addTests(unittest.makeSuite(UnittestKanaText))
    suites.addTests(unittest.makeSuite(UnittestKanaIndexer))
    return suites

    
