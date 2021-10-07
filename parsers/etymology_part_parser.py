from data_structures import EtymologyPart
from extractors.reference_extractor import ReferenceExtractor
from parsers.word_parser import WordParser


class EtymologyPartParser:
    def __init__(self):
        self.isNounCapitalized = False
        self.wordParser = WordParser()
        self.referenceExtractor = ReferenceExtractor()
        self.word = None
        self.wordText = ""
        self.references = list()

    def parse(self, text: str):
        self.wordParser.isNounCapitalized = self.isNounCapitalized

        self.references = self.referenceExtractor.extract(text)

        self.wordText = self.referenceExtractor.textLeft()

        self.word = self.wordParser.parse(self.wordText)

        return EtymologyPart(self.word, self.references)
