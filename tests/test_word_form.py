import unittest
from wiktionary import getEtymologyItem


class TestGetWordForm(unittest.TestCase):
    def test_three_word_forms(self):
        # community
        data = "Old French communité, comunité, comunete (modern French communauté)"
        item = getEtymologyItem(data, "")
        self.assertEqual(item.wordForm, "communité, comunité, comunete")


if __name__ == '__main__':
    unittest.main()
