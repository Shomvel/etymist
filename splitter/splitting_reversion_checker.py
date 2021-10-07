from re import Match

from base.reversion_checker import ReversionChecker
from data_structures import Text
from utilities import isMarkedWithinParenthesis


class SplitterReversionChecker(ReversionChecker):
    def __init__(self):
        super().__init__()
        self.safeWords = ['sense',
                          'meaning',
                          'use',
                          'originally',
                          'are',
                          'Doublet']

    @property
    def text(self):
        return self._text.value

    @text.setter
    def text(self, value: str):
        self._text.value = value

    @text.setter
    def text(self, value: Text):
        self._text.value = value.value

    def isMarkedWithinParenthesis(self, result: Match) -> bool:
        return isMarkedWithinParenthesis(self.text, result)

    def isMarkedSafeWords(self, result: Match) -> bool:
        # to avoid splitting texts like " In Early Modern English, used in the sense of the original Greek word."
        for word in self.safeWords:
            if word in result[0]:
                # print("Entered")
                return True

        return False

    @staticmethod
    def isMarkedNote(result: Match) -> bool:
        # , a people living west of ...
        # , a deity of art ...
        relation = result.group('relation')

        possibleNote = [item for item in relation.split(" ") if item not in ['', ',']]
        possibleNoteLength = 5

        return relation.strip().startswith(", a") and len(possibleNote) > possibleNoteLength

    def isMarkedAroundSafeWords(self, result: Match):
        for word in self.safeWords:
            searchRange = 30
            start = max(result.start() - searchRange, 0)

            end = result.start()
            textToSearch = self.text[start:end]
            if word in textToSearch:
                if '. ' not in textToSearch:
                    return True

                if textToSearch.find('. ') < textToSearch.find(word):
                    return True

        return False
