from data_structures import Word
from extractors.language_extractor import LanguageExtractor
from extractors.note_extractor import NoteExtractor
from extractors.word_form_extractor import WordFormExtractor


class PlainWordParser:
    def __init__(self):
        self.text = ""
        self.isNounCapitalized = False
        self.extractors = [LanguageExtractor(), NoteExtractor(), WordFormExtractor()]
        self.fields = []

    def parse(self, text: str):
        self.text = text
        self.fields = []

        self.extractors[0].isNounCapitalized = self.isNounCapitalized

        #todo: use a dictionary

        for extractor in self.extractors:
            field = extractor.extract(self.text)
            self.fields.append(field)
            self.text = extractor.textLeft()

        lang, note, wordForm = self.fields

        return Word(lang=lang, note=note, wordForm=wordForm)
