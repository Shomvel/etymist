import unittest

from splitter.text_splitter import TextSplitter


class TestTextSplitter(unittest.TestCase):
    def setUp(self) -> None:
        self.splitter = TextSplitter()
        self.result = None

    def assert_split(self, line: str, num: int):
        result = self.splitter.split(line)
        print(result)
        self.assertEqual(first=len(result), second=num, msg=f"result of {line} should have {num} items.")

    def assert_relation(self, line, word, index):
        result = self.splitter.split(line)
        self.assertIn(word, result[index])

    def test_plain_from(self):
        line = "From Proto-Italic: *luβēō (“to desire”), from Proto-Indo-European *lewbʰ- (“love, care, desire”)."
        self.assert_split(line, 2)

    def test_via(self):
        line = "From Middle English pork, porc, via Anglo-Norman"
        self.assert_split(line, 2)

    def test_of_multiple_worded_relation(self):
        line = "Old English cūþe, past indicative and past subjunctive form of cunnan (“to be able”) (compare " \
               "related cūþ, " \
               "whence English couth) "

        self.assert_split(line, 2)

        self.assertIn("{, past indicative and past subjunctive form of }", self.splitter.split(line)[1])

    def test_circa(self):
        circa = "c. 1459 and ca. 1550"
        self.assert_split(circa, 1)

    def test_prefixed_from(self):
        line = "Learned borrowing from Latin abaculus, a diminutive of abacus (“panel”)."
        self.assert_split(line, 2)
        self.assert_relation(line, r"{Learned borrowing from }", 0)
        self.assert_relation(line, r"{, a diminutive of }", 1)

    def test_probably_from(self):
        line = "Probably from Dutch Smurf"

        result = self.splitter.split(line)
        print(result)

    def test_comma(self):
        line = "Apple is red. Germany is good. China rules.\nApple is from trees.It is a fact."
        self.assert_split(line, 5)

    def test_beginning_of_relation(self):
        # todo: remove relation space at beginning
        calque = "A calque of the German word Kommunismus (from Marx and Engels's Manifesto of the Communist Party, " \
                 "published in 1848), in turn a calque of the French word communisme "
        self.assert_split(calque, 2)

    def test_prefixed_from_2(self):
        line = "which was formed from commun (“common”) (from Latin commūnis) and the suffix -isme (“-ism”)."
        self.assert_split(line, 1)

    def test_prefixed_from_3(self):
        line = "From the noun terrazo, or more likely borrowed from French terrasse"
        self.assert_split(line, 2)
        # a case of compound origin

    def test_after_pair_from_for_parenthesis(self):
        line = "from Old English dīċ (“trench, moat”) from Proto-Germanic *dīkaz (compare Swedish dike, Icelandic díki)"
        self.assert_split(line, 2)

    def test_after_pair_from_for_apostrophe(self):
        line = 'medicine," from Anglo-Norman'
        self.assert_split(line, 2)

    def test_for_comma_remains(self):
        line = ", from Proto-West Germanic *spendōn (“to spend”), borrowed from Latin expendere (“to weigh out”)."
        result = self.splitter.split(line)
        print(result)

    def test_process_abbreviations(self):
        line = "B.C.E."
        self.assert_split(line, 1)

        line = "A.D. "
        self.assert_split(line, 1)

    def test_splitting_informal_sentence_ending(self):
        line = "blablabla.\nThe word is cognate with Italian giara " \
               "(“jar; crock”), Occitan jarro, Portuguese jarra, jarro (“jug; ewer, pitcher”).The " \
               "verb is derived from the noun."
        self.assert_split(line, 3)

    def test_not_splitting_for_sense(self):
        line = "In sense 'maize' a shortening from earlier Indian corn."
        self.assert_split(line, 1)

        line = "All English senses developed from the chess sense. "
        self.assert_split(line, 1)

        line = "In Early Modern English, used in the sense of the original Greek word."
        self.assert_split(line, 1)

    def test_process_relation_with_connector(self):
        line = "zero-grade form of abc"
        result = self.splitter.split(line)
        self.assertTrue(result[0].startswith("{zero-grade form of }"))

    def test_of_within_notes(self):
        line = "from muse, an Ancient Greek deity of the arts."
        self.assert_split(line, 1)

        line = "from French crucial, a medical term for ligaments of the knee (which cross each other)"
        self.assert_split(line, 1)

    def test_from_and_of(self):
        line = "from a derivative of Latin carrus (“four-wheeled baggage wagon”)"
        self.assert_split(line, 1)

    def test_plain_from_and_their_source(self):
        line = "borrowed from Anglo-Norman musik, musike, Old French musique, and their source Latin mūsica,"
        self.assert_split(line, 2)

    def test_upper_case_from(self):
        line = "From Middle English toye (“amorous play, piece of fun or entertainment”), "
        self.assert_split(line, 1)

    def test_of_in_parenthesis(self):
        line = "From Middle English spoon, spoune, spone, spon (“spoon, chip of wood”), from Old English spōn (“sliver, chip of wood, shaving”),"
        self.assert_split(line, 2)

    def test_meaning_and_apostrophe(self):
        line = 'In the meaning "primordial matter" from the 16th century.'
        self.assert_split(line, 1)

    def test_sense(self):
        line = '''Figurative usage in the sense "confusion, disorder" from the 17th century.'''
        self.assert_split(line, 1)

    def test_chaos(self):
        line = '''Borrowed from Ancient Greek χάος (kháos, “vast chasm, void”).\nIn Early Modern English, used in the sense of the original Greek word. In the meaning "primordial matter" from the 16th century. Figurative usage in the sense "confusion, disorder" from the 17th century. The technical sense in mathematics and science dates from the 1960s.'''
        self.assert_split(line, 5)

    def test_in_turn_from_a(self):
        line = ", in turn from a Vulgar Latin *vocitus"
        self.assert_split(line, 1)

    def test_capitalized_prefix(self):
        line = 'Originally a verb of uncertain etymology. Possibly from French esclachier (“to break”). '
        self.assert_split(line, 2)

    def test_origin(self):
        line = ', from Old English cors, curs (“curse”), of unknown origin.'
        self.assert_split(line, 1)

    def test_both_ultimately_borrowed(self):
        line = 'Eclipsed non-native Middle English cuculer and coclear (“spoon”) both ultimately borrowed from the Latin.'
        self.assert_split(line, 2)

    def test_doublet_of_not_marked(self):
        line = "Doublet of panth."
        self.assertNotIn("{", self.splitter.split(line))

    def test_and_their_source(self):
        line = 'from Anglo-Norman reguler, Middle French reguler, regulier, and their source, Latin rēgulāris (“continuing rules for guidance”)'
        self.assert_split(line, 2)

    def test_and_its_source(self):
        line = 'bla, and its source, Latin generōsus (“of noble birth”)'
        self.assert_split(line, 2)

    def test_splitting_a_xxx_of(self):
        line = ' from Proto-Indo-European *kewk- (“to bend, curve, arch, vault”), a suffixed form of *kew-.'
        self.assert_split(line, 2)

    def test_split(self):
        line = 'From Proto-Italic *doleō (“hurt, cause pain”), from Proto-Indo-European *dolh₁éyeti (“divide”)'
        self.assert_split(line, 2)

if __name__ == '__main__':
    unittest.main()
