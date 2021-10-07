from unittest import TestCase

from data_structures import References
from extractors.reference_extractor import ReferenceExtractor


class TestReferenceExtractor(TestCase):
    def setUp(self) -> None:
        self.extractor = ReferenceExtractor()
        self.result = None
        self.line = ""

    def extract(self):
        self.result = self.extractor.extract(self.line)

    def print(self):
        if not self.result:
            self.extract()

        print(self.result)

    def assert_reference_type(self, referenceType: str):
        self.extract()
        self.assertEqual(self.extractor.referenceType, referenceType)

    def test_get_reference_type(self):
        self.line = "Cognate with Scots kintra."
        self.assert_reference_type("Cognate with")

    def assert_reference_counts(self, count: int):
        self.assertEqual(len(self.result), count)

    def test_extract_standalone_reference(self):
        self.line = "Compare Portuguese praia, French plage, Italian spiaggia."
        self.extract()
        self.assert_reference_type("Compare")
        self.assert_reference_counts(3)

    def test_extract_inline_reference(self):
        self.line = "“apple” (compare Scots aipple, West Frisian apel, Dutch appel, German Apfel, Swedish äpple, Danish æble)"
        self.extract()
        self.assert_reference_counts(6)
        self.assertFalse(self.result[-1].wordForm.endswith(")"))

    def test_text_left_for_inline_reference(self):
        self.line = "“apple” (compare Scots aipple, West Frisian apel, Dutch appel, German Apfel, Swedish äpple, Danish æble)"
        self.extractor.extract(self.line)
        self.assertEqual(self.extractor.textLeft(), "“apple”")

    def test_standalone_reference_with_notes(self):
        self.line = "Cognate to Portuguese olho, French œil, Italian occhio, Romanian ochi, Russian око (oko)."
        self.extract()
        word = self.result[-1]
        self.assertEqual(word.wordForm, "око")
        self.assertEqual(word.note, "oko")

    def test_reference_with_multiple_word_forms(self):
        self.line = "Cognate with Kyrgyz туура (tuura), Uzbek toʻgʻri, Old Turkic toğru, toğuru, toğrı‎ (toğru, toğuru, toğrı), "
        self.extract()
        self.assertEqual(len(self.result[-1].wordForm.split(", ")), 3)

    def test_reference_separated_with_and(self):
        self.line = "Compare Italian primavera and Romanian primăvară."
        self.extract()
        self.assert_reference_counts(2)

    def test_clearing_also(self):
        self.line = "Compare also Saterland Frisian Kop (“cup”), West Frisian kop (“cup”), Dutch kop (“cup”), " \
                    "German Low German Koppke, Köppke (“cup”), Danish kop (“cup”), Swedish kopp (“cup”) "
        self.extract()
        self.print()

    def test_a_lot_of_parenthesis(self):
        self.line = "Displaced native Middle English imene, ȝemǣne (“common, general, universal”) (from Old English " \
                    "ġemǣne (“common, universal”)), Middle English mene, mǣne (“mean, common”) (also from Old English " \
                    "ġemǣne (“common, universal”)), Middle English samen, somen (“in common, together”) (from Old " \
                    "English samen (“together”)) "

        self.extract()
        self.print()

    def test_cognate(self):
        self.line = "Cognate with Old English iucian, iugian, ġeocian, ġyċċan (“to join; yoke”). "
        self.extract()
        self.print()

    def test_cognate_Sicilian(self):
        self.line = "Cognate with West Flemish meuzie (“mosquito”), dialectal Swedish mausa (“mosquito”), Lithuanian musė (“a " \
                    "fly”) and Sicilian muschitta (“midge”) "
        self.extract()
        self.print()

    def test_unrelated(self):
        self.line = "Unrelated to English cower."
        self.extract()
        self.assertEqual(self.result.type, "Unrelated to")

    def test_native_before_language(self):
        self.line = "Displaced native Old English earg."
        self.extract()
        self.assertEqual(self.result[0].lang, "Old English")
        self.assertEqual(self.result[0].note, 'native')

    def test_non_native_before_language(self):
        self.line = "Eclipsed non-native Middle English cuculer and coclear (“spoon”) both ultimately borrowed from the Latin."
        self.extract()
        self.assertEqual(self.result[0].lang, "Middle English")
        self.assertEqual(self.result[0].note, 'non-native;')

    def test_colon_separated_reference(self):
        self.line = ' Cognate with Scots twa (“two”); North Frisian tou, tuu (“two”); Saterland Frisian twäin, two (“two”); West Frisian twa (“two”); Dutch twee (“two”); Low German twee, twei (“two”); German zwei, zwo (“two”); Danish and Norwegian to (“two”); Swedish två, tu (“two”); Icelandic tvö (“two”); Latin duō (“two”); Ancient Greek δύο (dúo, “two”); Irish dhá (“two”); Lithuanian dù (“two”); Russian два (dva, “two”); Albanian dy (“two”); Old Armenian երկու (erku, “two”); Sanskrit द्व (dvá, “two”); Tocharian A wu, Tocharian B wi.'
        self.extract()

    def test_under(self):
        self.line = ', from Proto-Germanic *under (whence also German unter, Dutch onder, Danish and Norwegian under)'
        self.extract()

    def test_whence(self):
        self.line = 'legō (whence English lesson and legend)'
        self.extract()
        self.assert_reference_counts(2)

    def test_and_its_descendants(self):
        self.line = 'Compare French échecs (“chess”) and its descendants: Catalan escacs and Dutch schaak.'
        self.extract()

    def test_text_left(self):
        self.line = 'Proto-Germanic *samdaz (compare West Frisian sân, Dutch zand, German Sand, Danish, Swedish and Norwegian sand)'
        self.extract()
        print(self.extractor.textLeft())

    def test_text_left_for_reference_in_parenthesis(self):
        self.line = ' from Proto-Germanic *paþaz (“path”) (compare West Frisian paad, Dutch pad, German Pfad)'
        self.extract()
        self.print()
        print(self.extractor.textLeft())

    def test_not_related(self):
        self.line = 'Not related to Latin tempus'
        self.assert_reference_type("Not related to")

    def test_greek(self):
        self.line = 'Cognate with Ancient Greek βαμβαίνω (bambaínō), βαμβαλύζω (bambalúzō, “I chatter with the teeth”), Russian болтать (boltatʹ, “to chatter, babble”)'
        self.print()