from splitter.delimiter_inserter import DelimiterInserter
from splitter.splitting_relation_marker import SplittingRelationMarker


class TextSplitter:
    def __init__(self, delimiter: str = "|"):
        self.text = ""
        self.delimiter = delimiter
        self.delimiterInserter = DelimiterInserter()
        self.relationMarker = SplittingRelationMarker()

    def split(self, text: str):
        if not text:
            raise ValueError("text must not be empty.")
        self.text = text

        self.removeUnwantedTexts()

        self.text = self.relationMarker.mark(self.text)
        self.text = self.delimiterInserter.insert(self.text)
        self.text = self.revertProtectedFrom(self.text)

        return [x for x in self.text.split(self.delimiter) if x]

    def removeUnwantedTexts(self):
        texts = ['\u200e', '\n', '\t']
        for text in texts:
            self.text = self.text.replace(text, "")
            # todo: remove tabs

    def revertProtectedFrom(self, text):
        return text.replace("$rom", "from")
