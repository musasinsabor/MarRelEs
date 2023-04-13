import unittest
import pandas as pd
import re

def tagset_parsing():
    sp_data = pd.read_csv("spanish-tagset.txt", sep="\t")
    data = pd.read_csv("Pretraitement/transposition.csv")
    sp = set(sp_data["ACRNM"])
    tr = set(data["spanish"])
    not_included = set()
    for e in sp:
        if e not in tr:
            if not re.search(r"V.*", e):
                not_included.add(e)
    return not_included

class TestTagsets(unittest.TestCase):
    def test_spanish_tagset(self):
        not_included_tags = tagset_parsing()
        expected = {'ALFP', 'ALFS', 'FO', 'NEG', 'PE', 'PNC', 'SE', 'UMMX', 'PREP/DEL Complex preposition "después del"', 'BACKSLASH backslash (\\)'}
        self.assertEqual(not_included_tags, expected)  # add assertion here


if __name__ == '__main__':
    unittest.main()
