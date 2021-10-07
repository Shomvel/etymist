import unittest

from parsers.etymology_part_parser import EtymologyPartParser


class TestEtymologyPartParser(unittest.TestCase):
    def test_line_with_reference(self):
        line = "Proto-Germanic *aplaz (“apple”) (compare Scots aipple, West Frisian apel, Dutch appel, German Apfel, " \
               "Swedish äpple, Danish æble) "
        print(EtymologyPartParser().parse(line))

    def test_no_word_Form(self):
        line = "Germanic (compare Old High German garwi, garawi (“dress, equipment, preparation”) and English gear)"
        print(EtymologyPartParser().parse(line))

    def test_smurf(self):
        line = "{}Dutch smurf (via the Belgian comic De Smurfen, a translation of French Les Schtroumpfs)"
        print(EtymologyPartParser().parse(line))
if __name__ == '__main__':
    unittest.main()
