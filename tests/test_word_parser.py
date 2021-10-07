import unittest

from extractors.note_extractor import NoteExtractor
from parsers.word_parser import WordParser
from data_structures import Word, ComplexWord


class TestComplexWordParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = WordParser()
        self.result = None
        self.line = ""
        self.expected = None

    def parse(self):
        self.result = self.parser.parse(self.line)

    def print(self):
        self.parse()
        print(self.result)
        self.result

    def get_expected(self):
        self.parse()
        word = self.result
        return Word(wordForm=word.wordForm, lang=word.lang, note=word.note).__repr__()

    def get_code(self):
        print(f"self.expected = {self.get_expected()}\nself.assert_complex_word()")

    def assert_complex_word(self):
        self.result = self.parser.parse(self.line)
        self.assertEqual(self.result.lang, self.expected.lang)
        self.assertEqual(self.result.wordForm, self.expected.wordForm)
        self.assertEqual(self.result.note, self.expected.note)

    def test_parse_compound_with_one_note(self):
        self.line = "com- + par (“equal”)"
        self.expected = Word("com- + par", "", "par: “equal”;")
        self.assert_complex_word()

    def test_parse_compound_with_two_notes(self):
        self.line = "commūnis (“common, ordinary; of or for the community, public”) + -itās (ultimately from " \
                    "Proto-Indo-European *-teh₂ts (“suffix forming nouns indicating a state of being”)) "
        self.expected = Word("commūnis + -itās",
                             "",
                             "commūnis: “common, ordinary; of or for the community, public”;\n"
                             "-itās: ultimately from Proto-Indo-European *-teh₂ts (“suffix forming nouns indicating a "
                             "state of being”);")
        self.assert_complex_word()

    def test_parse_or(self):
        self.line = "Late Latin charta (“paper, card, map”), Latin charta (“papyrus, writing”)"
        self.expected = Word("charta , charta",
                             "Late Latin / Latin",
                             "charta: “paper, card, map”;\ncharta: “papyrus, writing”;")
        self.assert_complex_word()

    def test_parse_and(self):
        self.line = "Old English discipul m (“disciple; scholar”) and discipula f (“female disciple”)"
        self.expected = Word("discipul m and discipula f",
                             "Old English / Old English",
                             "discipul m: “disciple; scholar”;discipula f: “female disciple” ")

    def test_parse_and_2(self):
        self.line = "Old French cercle and Latin circulus"
        print(self.parser.parse(self.line))
        self.expected = Word("cercle and circulus",
                             "Old French / Latin",
                             "")
        self.assert_complex_word()

    def test_parse_or_without_language(self):
        self.line = "al- (seen in alius (“other”), alienus (“of another”), etc)"
        self.expected = Word("al- / alienus",
                             "",
                             "al-: seen in alius (“other”; alienus :“of another”;")
        self.assert_complex_word()

    def test(self):
        self.line = "Old English not, nōt (“note, mark, sign”) and Old French note (“letter, note”)"
        self.print()

    #     wordForm: not, nōt and note
    # lang: Old English / Old French
    # note: not, nōt: “note, mark, sign”;
    # note: “letter, note”;

    def test_parse_or_with_duru(self):
        self.line = "Old English duru (“door”), dor (“gate”)"
        self.expected = Word(wordForm='duru , dor', lang='Old English', note='duru: “door”;\ndor: “gate”;')
        self.assert_complex_word()

    def test_only_note(self):
        self.line = "late 17th century"
        self.print()

    def test_etc(self):
        self.line = "Anglo-Norman memorie, Old French memoire etc"
        self.expected = Word(wordForm="memorie , memoire",
                             lang="Anglo-Norman / Old French",
                             note="possibly other sources")
        self.assert_complex_word()

    def test_spiel(self):
        self.line = '''German Spiel (“game”) + Zeug (“stuff”) or spielen (“to play”) + Zeug (“stuff”)"'''
        self.print()

    def test_and(self):
        self.line = '''Middle English karette and Middle French carotte'''
        self.expected = Word(lang='Middle English / Middle French', wordForm='karette and carotte', note='')
        self.assert_complex_word()

    def test_t(self):
        self.line = '''Proto-Indo-European *n̥dʰér (“under”) and *n̥tér (“inside”)'''
        self.get_code()

    def test_comma_separated_words_with_greek(self):
        self.line = '''Ancient Greek ἀμάω (amáō, “to gather”), ἄμη (ámē, “water bucket”)'''
        self.print()

    def test_comma_separated_words_with_greek_2(self):
        self.line = '''Ancient Greek βαμβαίνω (bambaínō), βαμβαλύζω (bambalúzō, “I chatter with the teeth”)'''
        self.print()

    def test_comma_and_or(self):
        self.line = '''mosca + -ito (diminutive suffix), or Old Spanish moquito'''
        self.print()

    def test_slash(self):
        self.line = '''Ancient Greek πατέω (patéō) / πάτος (pátos)'''
        self.expected = Word(lang='Ancient Greek', wordForm='πατέω / πάτος', note='πατέω: patéō;\nπάτος: pátos;')
        self.assert_complex_word()

    def test_comma_after_parenthesis(self):
        self.line = '''Avestan 𐬞𐬀𐬥𐬙𐬀 (panta, “way”), 𐬞𐬀𐬚𐬀 (paθa, genitive)'''
        self.print()
if __name__ == '__main__':
    unittest.main()

# print(p.parse())
# r = p.parse("contra “against, opposite” + Medieval Latin rotulus, Latin rotula “roll, a little wheel”, diminutive of rota “a wheel”")
# print(r)
