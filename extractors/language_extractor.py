import re
from base.extractor import Extractor


class LanguageExtractor(Extractor):
    """evidence: language names are capitalized in English. """

    def __init__(self, isNounCapitalized: bool = False):
        super().__init__()
        self.capitalizedWord = r"[A-Z][\w-]+"
        # some language name has hyphen
        # eg. Proto-Indo European, Anglo-Norman
        self._isNounCapitalized = isNounCapitalized
        # for proper nouns
        self.words = []

    def process(self):
        self.removeUnwantedTexts()
        self.result = self.extractConnectedLanguageName() or self.extractOneLanguageName()
        self.dealWithCapitalizedNoun()
        if not self.isFirst():
            self.result = ""

    def textLeft(self) -> str:
        return self.text.replace(self.result, "")

    def dealWithCapitalizedNoun(self):
        self.words = self.result.split(" ")
        if not self.words:
            return

        if self.isNounCapitalized:
            self.result = " ".join(self.words[:-1])
            # get rid of last word

    @property
    def isNounCapitalized(self) -> bool:
        return self.isLanguageWithCapitalizedNoun() \
               or "Lūnae" in self.words \
               or self._isNounCapitalized

        # "Lūnae" for lunes

        # if the queried is proper noun
        # then the parameter is passed from outside

    @isNounCapitalized.setter
    def isNounCapitalized(self, value):
        self._isNounCapitalized = value

    def isLanguageWithCapitalizedNoun(self):
        if 'German Low German' in self.result:
            return False

        langs = ['German', 'Frisian']

        for lang in langs:
            if lang not in self.words:
                continue
            # used rules out Germanic
            allWords = self.text.split(" ")
            # different to self.words
            # need to get
            nextWord = allWords.index(lang) + 1
            return allWords[nextWord].istitle()

    def extractConnectedLanguageName(self) -> str:
        for linker in ["or", "and"]:
            linkerWithSpace = f" {linker} "
            # added space to rule out "Norman"
            linkerWithSpaceIndex = self.text.find(linkerWithSpace)

            if linkerWithSpaceIndex == -1:
                continue

            if not self.linkerSeparatesLanguageName(linker):
                continue

            firstLangNameEnd = linkerWithSpaceIndex + 1
            # plus one to include the space key for regex to work
            nextLangNameStart = linkerWithSpaceIndex + len(linkerWithSpace)

            a = LanguageExtractor()
            # if self.extract were used, self.text would be changed
            first, second = a.extract(self.text[:firstLangNameEnd]), a.extract(self.text[nextLangNameStart:])
            return f"{first} {linker} {second}"

        return ""

    def linkerSeparatesLanguageName(self, linker: str):
        # separates language name: English or German
        # separates notes: king or chess (generally)
        return bool(re.search("{0} {1}".format(self.capitalizedWord, linker), self.text))

    def extractOneLanguageName(self) -> str:
        if self.text.startswith("Tocharian"):
            return re.search(rf"(?P<name>{self.capitalizedWord} [A-Z]) ", self.text).group('name')
            # because Tocharian A and Tocharian B cant be matched
        # three-worded, two-worded, one-worded language name
        results = [self.extractLanguageName(length=i) for i in range(3, 0, -1)]

        for result in results:
            if result:
                return result[0]

        return ""

    def extractionRegex(self, length: int):
        regex = " ".join([self.capitalizedWord for _ in range(length)])
        return re.compile(regex)

    def extractLanguageName(self, length: int):
        return self.extractionRegex(length).findall(self.text)

    def isFirst(self):
        return self.text.find(self.result) == 0

    def removeUnwantedTexts(self):
        self.text = self.text \
            .strip() \
            .removeprefix("a") \
            .removeprefix("the") \
            .removesuffix("word") \
            .strip()
