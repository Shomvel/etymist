import unittest
from unittest import TestCase

from extractors.relation_extractor import RelationExtractor


class Test(TestCase):
    def setUp(self) -> None:
        self.extractor = RelationExtractor()
        self.calque = "{in turn a calque}"

    def test_extract_line(self):
        self.extractor.text = self.calque
        self.extractor.extractLine()
        self.assertEqual(self.extractor.text, "{in turn a calque}")

    def test_extract(self):
        self.assertEqual("calque", self.extractor.extract(self.calque))

    def test_extract_line_when_empty(self):
        a = self.extractor.extract("from a b c. ")
        self.assertEqual(a, "")

    def assert_remove_filler(self, text, filler):
        self.extractor.text = text
        self.extractor.removeFiller()
        self.assertNotIn(filler, self.extractor.result)

    def test_remove_filler(self):
        text = "a diminutive"
        filler = "a"
        self.assert_remove_filler(text, filler)
        text = "A calque"
        filler = "A"
        self.assert_remove_filler(text, filler)


if __name__ == '__main__':
    unittest.main()
