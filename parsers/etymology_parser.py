from data_structures import RawEtymology, EtymologyPart, Word, Etymology, CurrentWord
from extractors.reference_extractor import ReferenceExtractor
from extractors.relation_extractor import RelationExtractor
from parsers.etymology_part_parser import EtymologyPartParser
from splitter.text_splitter import TextSplitter
from utilities import wrappedList


class EtymologyParser:
    def __init__(self):
        # todo: 使用反向依赖
        self.splitter = TextSplitter()
        self.parser = EtymologyPartParser()
        self.relationExtractor = RelationExtractor()
        self.referenceExtractor = ReferenceExtractor()

        self.lines: list[CurrentWord, EtymologyPart] = []
        self.history = []
        self.relations = []
        self.rawEtymology = None

    def parse(self, rawEtymology: RawEtymology):
        self.history.clear()
        self.relations.clear()

        self.rawEtymology = rawEtymology
        self.lines = self.splitter.split(rawEtymology.text)
        self.parser.isNounCapitalized = self.rawEtymology.word.istitle()

        self.appendCurrentWord()
        self.getParts()
        self.fillOmittedLang()
        return Etymology('', self.history, self.relations)

    def getParts(self):
        for line in self.lines:
            self.relations.append(self.relationExtractor.extract(line))
            textLeft = self.relationExtractor.textLeft()
            item = self.parser.parse(textLeft)
            self.history.append(item)

    def appendCurrentWord(self):
        word = self.rawEtymology.word
        lang = self.rawEtymology.lang
        references = [self.referenceExtractor.extract(reference) for reference in self.moveReferences()]
        note = self.moveNotes()

        part = CurrentWord(Word(wordForm=word, lang=lang, note=note), references)
        self.history.append(part)

    def removeFromLines(self, toRemove: list):
        self.lines = [x for x in self.lines if x not in toRemove]

    def getFromLines(self, func):
        return [line for line in self.lines if func(line)]

    def moveReferences(self):
        references = self.getFromLines(self.referenceExtractor.isReferenceSentence)
        self.removeFromLines(references)
        return references

    def moveNotes(self):
        notes = self.getFromLines(lambda x: not x.startswith("{"))
        self.removeFromLines(notes)
        return wrappedList(notes)

    def fillOmittedLang(self):
        self.fillOmittedLangInParts()
        self.fillOmittedLangInReferences()

    def fillOmittedLangInParts(self):
        for index, item in enumerate(self.history):
            if not item.word.lang:
                item.word.lang = self.history[index - 1].word.lang

    def fillOmittedLangInReferences(self):
        for reference in self.history[0].references:
            if not (reference.type.startswith("Doublet") or reference.type.startswith("See")):
                return

            for word in reference.words:
                word.lang = self.rawEtymology.lang


        for item in self.history[1:]:
            if not item.references:
                continue

            for word in item.references.words:
                if not word.lang:
                    word.lang = self.rawEtymology.lang
