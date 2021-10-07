import re


class DelimiterInserter:
    def __init__(self, delimiter: str = "|"):
        self.text = ""
        self.delimiter = delimiter
        self.fromMarker = "{}"
        self.fromAndVia = ['from', 'via', 'perhaps via']
        self.andItsSource = [f'and {pronoun} source' for pronoun in ('its', 'their')]
        self.sourceMarkers = self.andItsSource + self.fromAndVia

    def insert(self, text: str) -> str:
        self.text = text

        self.replaceConnectors()

        self.replacePeriods()

        self.revertLowerCaseAbbreviations()
        self.revertUpperCaseAbbreviations()

        self.insertBeforeBrackets()

        return self.text

    def replaceConnectors(self) -> None:
        self.replaceCapitalizedFromAndVia()
        self.replaceAndItsSourceBetweenCommas()
        self.replaceSourceMarkersAfterPunctuations()

    def replaceSourceMarkersAfterPunctuations(self):
        pattern = self.delimiter.join([rf', {marker} |(?<=[\)"”;]) {marker} '
                                       for marker in self.sourceMarkers])
        self.replaceWithFromMarker(pattern)

    def replaceWithFromMarker(self, pattern: str):
        self.text = re.sub(pattern=pattern,
                           string=self.text,
                           repl=self.fromMarker)

    def replaceCapitalizedFromAndVia(self):
        pattern = self.delimiter.join([rf'{marker.title()} ' for marker in self.fromAndVia])
        self.replaceWithFromMarker(pattern)

    def replaceAndItsSourceBetweenCommas(self):
        pattern = self.delimiter.join([f", {marker}, " for marker in self.andItsSource])
        self.replaceWithFromMarker(pattern)

    def replacePeriods(self) -> None:
        self.text = re.sub(pattern=r"\. |\.\n|(?<![A-Z])\.",
                           repl=self.delimiter,
                           string=self.text)

    def revertLowerCaseAbbreviations(self) -> None:
        self.text = re.sub(pattern=r"c(a?)\|(\d{4})",
                           repl=r"c\1. \2",
                           string=self.text)
        # situation: c. 1486 and ca.1550

        abbreviations = ['cf', 'id', 'etc']
        for abbreviation in abbreviations:
            self.text = re.sub(pattern=abbreviation + r"\|",
                               repl=abbreviation + ". ",
                               string=self.text)

    def revertUpperCaseAbbreviations(self) -> None:
        self.text = re.sub(pattern=fr"([A-Z]){self.delimiter}",
                           repl=r"\1",
                           string=self.text)
        # eg. B. C. E.

    def insertBeforeBrackets(self) -> None:
        self.text = re.sub(pattern=r"\{",
                           repl=self.delimiter + "{",
                           string=self.text)
