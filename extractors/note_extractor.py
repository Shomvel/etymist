from re import search, sub, compile

from base.extractor import Extractor
from utilities import removeOutmostParenthesis


class NoNoteError(Exception):
    pass


class NoteExtractor(Extractor):
    """ use: etymology parts and references
        implementation: extract text from note starts;
        """

    def __init__(self, text: str = ""):
        super().__init__(text)
        self.startNoteExtractor = StartNoteExtractor()
        self.endNoteExtractor = EndNoteExtractor()

    def process(self) -> None:
        self.text = self.text.strip()
        self.getNote()
        self.processNeighboringParenthesis()
        self.removePunctuations()

    def textLeft(self) -> str:
        text = self.text
        text = self.startNoteExtractor.removeNote(text)
        text = self.endNoteExtractor.removeNote(text)
        return text

    def getNote(self) -> None:
        self.result = self.startNoteExtractor.getNote(self.text) \
                      + self.endNoteExtractor.getNote(self.text)

    def removePunctuations(self) -> None:
        self.result = sub(pattern=r"^ *,|[,;] *$",
                          repl="",
                          string=self.result).strip()

        self.result = removeOutmostParenthesis(self.result)

    def processNeighboringParenthesis(self) -> None:
        self.result = self.result.replace(") (", "; ")


class StartNoteExtractor:
    def __init__(self):
        self.text = ""
        self.notesAtStart = ['verb', 'noun']
        self.noteStartInParenthesis = compile(r'^\((.+)\) ')

    def getNote(self, text: str) -> str:
        self.text = text

        for note in self.notesAtStart:
            if self.text.startswith(note):
                return note + '; '

        noteInParenthesis = self.noteStartInParenthesis.search(self.text)
        if noteInParenthesis:
            return noteInParenthesis[0]

        return ''

    def removeNote(self, text: str) -> str:
        for note in self.notesAtStart:
            text = text.replace(note, "")

        text = self.noteStartInParenthesis.sub(string=text,
                                               repl='')
        return text.strip()


class EndNoteExtractor:
    def __init__(self):
        self.text = ""

    @property
    def noteStart(self) -> int:
        markers = [
            r", a",
            r", an",
            r', whence',
            r", which",
            r' from which',
            r', since',
            r", but",
            r"“",
            r' "',
            r" \(",
            r'(, \w+d )',
            r', with',
            r': '
        ]
        # need r prefix because self.markers is used with re

        possibleMarkers = [search(marker, self.text) for marker in markers if search(marker, self.text)]
        if not possibleMarkers:
            raise NoNoteError

        marker = sorted(possibleMarkers, key=lambda match: match.start())[0]
        markerText = marker[0]

        if markerText.startswith(", "):
            return marker.start() + 2
        elif markerText.startswith(" ("):
            return marker.start() + 1
        else:
            return marker.start()

    def removeNote(self, text: str) -> str:
        try:
            return text[:self.noteStart].strip()
        except NoNoteError:
            return text

    def getNote(self, text: str) -> str:
        self.text = text

        try:
            return self.text[self.noteStart:]
        except NoNoteError:
            return ''
