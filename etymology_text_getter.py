from typing import Dict

from data_structures import EtymologyText, RawEtymology
from re import search, Match
from extractors.reference_extractor import referenceStarts


class EtymologyTextGetter:
    def __init__(self):
        self.paragraphs = []
        self.text = ''
        self.DEFAULT = 'default'

    def get(self, etymology: RawEtymology) -> EtymologyText:
        self.text = etymology.text

        self.paragraphs = self.text.split('\n')

        return EtymologyText(lang=etymology.lang,
                             word=etymology.word,
                             toParse=self.getContentToParse(),
                             note=self.text)

    def removeParagraph(self, text: str):
        self.text = self.text.replace(text, '')

    def getContentToParse(self) -> Dict[str, str]:
        toParse = dict()
        prefix = ''
        prefixedCount = 0

        for paragraph in self.paragraphs:
            canParse = False

            if paragraph.startswith('From'):
                prefix = self.DEFAULT
                canParse = True

            prefixSearch = self.getPrefix(paragraph)
            if prefixSearch:
                prefix = prefixSearch.group(0)
                prefixedCount += 1

            if self.isReference(paragraph):
                prefix = self.DEFAULT
                canParse = True

            if canParse:
                toParse[prefix] = ' ' + paragraph
                self.removeParagraph(paragraph)

        return toParse

    @staticmethod
    def getPrefix(text: str) -> Match:
        return search(r'/^(\w+) from|^The (.*?) from', text)

    @staticmethod
    def isReference(text: str) -> bool:
        for start in referenceStarts:
            if start in text:
                return True

        return False
