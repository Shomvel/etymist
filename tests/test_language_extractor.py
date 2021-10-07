import unittest
from extractors.language_extractor import LanguageExtractor
import re


class TestLanguageExtractor(unittest.TestCase):
    def test_regex(self):
        e = LanguageExtractor()
        regexes = [re.compile(r"[A-Z][\w-]+"),
                   re.compile(r"[A-Z][\w-]+ [A-Z][\w-]+"),
                   re.compile(r"[A-Z][\w-]+ [A-Z][\w-]+ [A-Z][\w-]+")]

        for i, regex in zip(range(1, 4), regexes):
            self.assertEqual(e.extractionRegex(i), regex)

    def assert_language(self, text, expected, isNounCapitalized=False):
        e = LanguageExtractor(isNounCapitalized=isNounCapitalized)
        result = e.extract(text)
        self.assertEqual(expected, result)

    def test_two_word(self):
        self.assert_language(text='Old Spanish ojo',
                             expected='Old Spanish')

        self.assert_language(text="Ottoman Turkish طوغری (doğrı)",
                             expected='Ottoman Turkish')

        self.assert_language(text='Vulgar Latin oclus',
                             expected='Vulgar Latin')

    def test_one_word(self):
        self.assert_language(text='Latin oculus',
                             expected='Latin')

    def test_noun_capitalize_for_spanish_lunes(self):
        self.assert_language(text="Latin Lūnae dīēs",
                             expected="Latin")
        # a special case
        # lunes itself is not capitalized
        # though it's a proper noun

    def test_noun_capitalize_for_proper_noun(self):
        self.assert_language(text="Latin Germānus,",
                             expected="Latin",
                             isNounCapitalized=True)
        # because it's a proper noun
        # in reality it's based on whether query is capitalized or not

    def test_noun_capitalize_for_German(self):
        self.assert_language(text="German Seminar",
                             expected="German")

    def test_multiple_language_name(self):
        s = "Anglo-Norman or Old Northern French receite (“receipt, recipe”) (1304)" \
            ", altered (by influence of receit (“he receives”) "

        self.assert_language(s, "Anglo-Norman or Old Northern French")

    def test_hyphened_name(self):
        tests = ["Anglo-Norman", "Proto-West Germanic", "Proto-Indo-European"]
        [self.assert_language(test, test) for test in tests]

    def test_no_language_name(self):
        s = "from comun"
        self.assert_language(s, "")

    def test_language_not_at_front(self):
        s = "itās (ultimately from Proto-Indo-European *-teh₂ts (“suffix forming nouns indicating a state of being”))"
        self.assert_language(s, "")

    def test_omitted_language_with_capitalized_noun(self):
        s = '''from Germānī, a people living around and east of the Rhine first attested in the 1st 
                 century B.C.E. works of Julius Caesar and of uncertain etymology.'''
        self.assert_language(s, "")

    def test_old_high_german(self):
        s = '''Old High German garwi, garawi (“dress, equipment, preparation”)'''
        self.assert_language(s, "Old High German")

    def test_middle_english(self):
        s = '''Middle English receipt, receyt, receite, recorded since c.\xa01386 as "statement of '
                 'ingredients in a potion or medicine,'''
        self.assert_language(s, "Middle English")

    def test_or_not_separating_language_name(self):
        s = "Arabic شَاه\u200e (šāh, “king or check at chess, shah”)"
        self.assert_language(s, "Arabic")

    def test_frisian_with_capitalized_noun(self):
        s = "Saterland Frisian Schak, Schach"
        self.assert_language(s, "Saterland Frisian")

    def test_tocharian(self):
        s = "Tocharian A wu"
        self.assert_language(s, "Tocharian A")

        s = "Tocharian B wu"
        self.assert_language(s, "Tocharian B")

    def test_german_low_german(self):
        s = "German Low German Kluut, Kluute (“lump, mass, ball”)"
        self.assert_language(s, "German Low German")

    def test_with_prefixes_and_suffixes(self):
        s = "a German word Wasser"
        self.assert_language(s, "German")

if __name__ == '__main__':
    unittest.main()
