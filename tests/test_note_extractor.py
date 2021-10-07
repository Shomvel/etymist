from unittest import TestCase
from extractors.note_extractor import NoteExtractor


class TestNoteExtractor(TestCase):
    def setUp(self) -> None:
        self.extractor = NoteExtractor()
        self.text = ""
        self.textLeft = ""

    def assert_note(self) -> None:
        self.assertEqual(self.note, self.extractor.extract(self.text))

    def test_but_separated_note(self) -> None:
        self.text = "Late Latin *compania, but this word is not attested"
        self.note = "but this word is not attested"
        self.assert_note()

    def assert_text_left(self):
        self.extractor.extract(self.text)
        self.assertEqual(self.extractor.textLeft(), self.textLeft)

    def test_text_left_for_note_in_apostrophe(self):
        self.text = "contra “against, opposite”"
        self.textLeft = "contra"
        self.test_text_left()

    def test_text_left_for_note_in_parenthesis(self):
        self.text = "Latin expendere (“to weigh out”)"
        self.extractor.extract(self.text)
        self.assertNotIn(self.extractor.textLeft(), "(“to weigh out”)")

    def test_note_with_parenthesis(self):
        self.text = "Latin expendere (“to weigh out”)"
        self.note = "“to weigh out”"
        self.assert_note()

    def test_note_with_embedded_parenthesis(self):
        self.text = "Old English spendan (attested especially in compounds āspendan (“to spend”), forspendan (“to use up, " \
                    "consume”)) "
        self.note = "attested especially in compounds āspendan (“to spend”), forspendan (“to use up, consume”)"
        self.assert_note()

    def test_note_with_multiple_parenthesis(self):
        self.text = "Old High German spentōn (“to consume, use, spend”) (whence German spenden (“to donate, provide”))"
        self.note = "“to consume, use, spend”; whence German spenden (“to donate, provide”)"
        self.assert_note()

    def test_note_with_past_participle(self):
        self.text = '''From Middle English receipt, receyt, receite, recorded since c.\xa01386 as "statement of ingredients in a potion or medicine,'''
        self.note = '''recorded since c.\xa01386 as "statement of ingredients in a potion or medicine'''
        self.assert_note()

    def test_note_starting_with_a(self):
        self.text = '''from French schtroumpf, a word that was created by Peyo based on German Strumpf (literally 
        “stocking, sock”), either simply because it sounds funny to the French ear or based on a regional German use 
        for “idiot”. '''
        self.note = '''a word that was created by Peyo based on German Strumpf (literally 
        “stocking, sock”), either simply because it sounds funny to the French ear or based on a regional German use 
        for “idiot”.'''
        self.assert_note()
        # schtruoumpf was

    def test_note_with_multiple_markers(self):
        self.text = '''Borrowed from Dutch smurf (via the Belgian comic De Smurfen, a translation of French Les 
        Schtroumpfs) '''
        self.note = '''via the Belgian comic De Smurfen, a translation of French Les 
        Schtroumpfs'''
        self.assert_note()

    def test_past_participle(self):
        self.text = "xxx, recorded since 1980s"
        self.note = 'recorded since 1980s'
        self.assert_note()
        textLeft = 'xxx'

    def test_pattern_similar_to_past_participle(self):
        self.text = 'From Middle English voide, voyde'
        self.note = ''
        self.assert_note()

    def test_removing_parenthesis(self):
        self.text = '''Icelandic klót (“knob on a sword's hilt”)'''
        self.note = '''“knob on a sword's hilt”'''
        self.assert_note()

    def test_text_left(self):
        self.text = '''noun terrazo'''
        self.note = "noun"
        self.assert_note()

        self.textLeft = 'terrazo'
        self.assert_text_left()

    def test_note_in_parenthesis_at_front(self):
        self.text = '''(a byform of, see it for more) Medieval Latin masca, mascha'''
        self.note = '''a byform of, see it for more'''
        self.assert_note()

        self.textLeft = '''Medieval Latin masca, mascha'''
        self.assert_text_left()

    def test_from_which(self):
        self.text = '''Germanic *maskā from which English mesh\xa0is regularly inherited'''
        self.note = '''from which English mesh\xa0is regularly inherited'''
        self.assert_note()



