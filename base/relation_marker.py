from re import Match
from typing import TypeVar

from data_structures import Text

ReversionCheckerType = TypeVar('ReversionCheckerType', bound='ReversionMarker')


class RelationMarker:
    def __init__(self, reversionChecker: ReversionCheckerType):
        self._text = Text("")
        # use of class Text is to share text between reversionChecker and RelationMarker
        self.reversionChecker = reversionChecker
        self.reversionChecker._text = self._text

    @property
    def text(self):
        return self._text.value

    @text.setter
    def text(self, value: str):
        self._text.value = value

    def mark(self, text: str) -> str:
        if not text:
            raise ValueError("text must not be empty.")

        self.text = text

        self.markRelations()
        self.revertUnwantedMarks()
        self.finish()

        return self.text

    def markRelations(self):
        pass

    def revertUnwantedMarks(self):
        pass

    def finish(self):
        pass

    def replaceOnResult(self, toReplace: str, result: Match):
        self.text = self.text[:result.start()] \
                    + toReplace \
                    + self.text[result.end():]
