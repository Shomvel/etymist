import functools
from copy import copy
from typing import Union

from data_structures import References
from base.extractor import Extractor
from re import sub, IGNORECASE, search, Match
from parsers.word_parser import WordParser
from utilities import removeOutmostParenthesis

referenceStarts = [
    "Doublet of",
    "Cognate to",
    "Cognate with",
    "Akin to",
    "See also",
    "See",
    "More at",
    "Displaced",
    "Eclipsed",
    "Compare also",
    "Compare",
    "Replaced",
    "Not related to",
    "Unrelated to",
    "Related also to",
    "Related to",
    "Merged with",
    "Equivalent to",
    "whence also",
    'whence'
]


# todo: fill omitted lang handling for doublet, see also ...

class ReferenceExtractor(Extractor):
    def __init__(self, text: str = ""):
        super().__init__(text)
        self.delimiter = "|"
        self.referenceStarts = copy(referenceStarts)
        self.referenceWords = ""

    @functools.cached_property
    def referenceTypeMatch(self) -> Union[Match[str], None]:
        for referenceType in referenceStarts:
            result = search(f"{referenceType} ", self.text, IGNORECASE)
            if referenceType == 'Compare':
                if 'compare stem' in self.text:
                    return None

            if result:
                return result

        return None

    @property
    def referenceType(self) -> str:
        if not self.referenceTypeMatch:
            return ""

        return self.referenceTypeMatch[0].strip()

    @property
    def hasReference(self) -> bool:
        return bool(self.referenceTypeMatch)

    def clearCache(self):
        cached = "referenceTypeMatch"
        if cached in self.__dict__:
            del self.__dict__[cached]

    def process(self):
        self.clearCache()
        if not self.hasReference:
            return
        self.referenceWords = self.getReferenceWords()
        self.removeTexts()
        self.insertDelimiters()
        self.getReference()
        self.processPrefixedLanguageName()

    def textLeft(self) -> str:
        if not self.hasReference:
            return self.text

        toReplace = self.referenceType + ' ' + self.getReferenceWords()

        if (start := self.referenceTypeMatch.start()) != 0 and self.text[start] == '(':
            toReplace = '(' + toReplace.lower()

        return self.text.replace(toReplace, '').strip()

    @staticmethod
    def isReferenceSentence(text: str) -> bool:
        e = ReferenceExtractor()
        e.text = text
        return e.hasReference and \
               (text.startswith("The word is") or text.startswith(e.referenceType))
        # eg Compare (...).
        # eg Proto-German xxx (compare ...).
        # eg The word is cognate with

    def removeTexts(self):
        self.referenceWords = sub(pattern=r"\.|(?<=\))\.",
                                  string=self.referenceWords,
                                  repl="",
                                  flags=IGNORECASE).strip()

        self.referenceWords = removeOutmostParenthesis(self.referenceWords)

    def insertDelimiters(self):
        self.referenceWords = sub(pattern=r"(, and |, | and |,|; )([A-Z])",
                                  string=str(self.referenceWords),
                                  repl=r"{}\2".format(self.delimiter))
        # examples:
        # , and Frankish XXX
        # , Middle English
        # Italian primavera and Romanian primăvară
        # put ", and " at front due to short circuit
        self.referenceWords = sub(pattern=r", ([a-z]+ [A-Z]\w+ )",
                                  string=self.referenceWords,
                                  repl=r"{}\1".format(self.delimiter))
        # todo: deal with the situation where query is "and"
        # , dialectal Swedish

    def getReference(self):
        parser = WordParser()
        words = [parser.parse(item) for item in self.referenceWords.split(self.delimiter)]
        self.result = References(self.referenceType.capitalize().strip(), words)

        self.result[-1].wordForm = self.result[-1].wordForm.replace(")", "")

    def getReferenceWords(self) -> str:
        return self.text[self.referenceTypeMatch.end():]

    def processPrefixedLanguageName(self):
        # eg native Old English
        # put here instead of language extractor
        # because native XX only appears in references
        # TODO: refactor

        for word in self.result.words:
            result = search(r"(?P<prefix>[a-z-]+) (?P<name>[A-Z][a-z]+ [A-Z][a-z]+)", word.wordForm)
            if result:
                word.lang = result.group('name')
                word.wordForm = word.wordForm.replace(result[0], "").strip()
                if not word.note:
                    word.note = result.group('prefix')
                else:
                    word.note += '; ' + result.group('prefix')
