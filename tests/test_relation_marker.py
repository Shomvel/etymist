import re
from unittest import TestCase

from splitter.splitting_relation_marker import SplittingRelationMarker


class TestRelationMarker(TestCase):
    def setUp(self) -> None:
        self.marker = SplittingRelationMarker()
        self.result = None

    def test_split(self):
        self.fail()

    def test_get_relation_regex(self):
        print(self.marker.getRelationRegex())
        r = [re.compile(", ([\\w'\\- ]+ from)|^([\\w'\\- ]+ from)"), re.compile(", ([\\w'\\- ]+ of)|^([\\w'\\- ]+ of)")]
        self.assertEqual(self.marker.getRelationRegex(), r)

    def assert_mark(self, line: str):
        result = self.marker.mark(line)
        print(result)

    def assert_relation(self, line, word, index):
        result = self.marker.mark(line)
        self.assertIn(word, result[index])

    def test_of_multiple_worded_relation(self):
        line = "Old English cūþe, past indicative and past subjunctive form of cunnan (“to be able”) (compare " \
               "related cūþ, " \
               "whence English couth) "

        self.assert_mark(line)

        self.assertIn("{past indicative and past subjunctive form}", self.marker.mark(line)[1])

    def test_prefixed_from(self):
        line = "Learned borrowing from Latin abaculus, a diminutive of abacus (“panel”)."
        self.assert_mark(line)

    def test_probably_from(self):
        line = "Probably from Dutch Smurf"

        result = self.marker.mark(line)
        print(result)

    def test_beginning_of_relation(self):
        # todo: remove relation space at beginning
        calque = "A calque of the German word Kommunismus (from Marx and Engels's Manifesto of the Communist Party, " \
                 "published in 1848), in turn a calque of the French word communisme "
        self.assert_mark(calque)

    def test_prefixed_from_2(self):
        line = "which was formed from commun (“common”) (from Latin commūnis) and the suffix -isme (“-ism”)."
        self.assert_mark(line)

    def test_prefixed_from_3(self):
        line = "From the noun terrazo, or more likely borrowed from French terrasse"
        self.assert_mark(line)
        # a case of compound origin

    def test_for_comma_remains(self):
        line = ", from Proto-West Germanic *spendōn (“to spend”), borrowed from Latin expendere (“to weigh out”)."
        result = self.marker.mark(line)
        print(result)

    def test_not_splitting_for_sense(self):
        line = "In sense 'maize' a shortening from earlier Indian corn."
        self.assert_mark(line)

        line = "All English senses developed from the chess sense. "
        self.assert_mark(line)

        line = "In Early Modern English, used in the sense of the original Greek word."
        self.assert_mark(line)

    def test_process_relation_with_connector(self):
        line = "zero-grade form of abc"
        self.assert_mark(line)

    def test_of_within_notes(self):
        line = "from muse, an Ancient Greek deity of the arts."
        self.assert_mark(line)

        line = "from French crucial, a medical term for ligaments of the knee (which cross each other)"
        self.assert_mark(line)

    def test_from_and_of(self):
        line = " from a derivative of Latin carrus (“four-wheeled baggage wagon”)"
        self.assert_mark(line)

    def test_plain_from_and_their_source(self):
        line = "borrowed from Anglo-Norman musik, musike, Old French musique, and their source Latin mūsica,"
        self.assert_mark(line)

    def test_upper_case_from(self):
        line = "From Middle English toye (“amorous play, piece of fun or entertainment”), "
        self.assert_mark(line)

    def test_of_in_parenthesis(self):
        line = "From Middle English spoon, spoune, spone, spon (“spoon, chip of wood”), from Old English spōn (“sliver, chip of wood, shaving”),"
        self.assert_mark(line)

