from unittest import TestCase
from wiktionary import getLanguageName


class TestGetLanguageName(TestCase):
    def test_two_worded_language_name(self):
        # commerce
        data = {"Late Latin commercialis": "Late Latin",
                "Middle English comun": "Middle English",
                }

        for line, result in data.items():
            self.assertEqual(getLanguageName(line), result)
