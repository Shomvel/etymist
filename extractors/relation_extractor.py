import re
from base.extractor import Extractor


class RelationExtractor(Extractor):
    def __init__(self, text: str = ""):
        super().__init__(text)
        self.relationRegex = r'\{(.*)\}'
        self.text = text

    def textLeft(self):
        return re.sub(pattern=self.relationRegex, string=self.text, repl="")

    def process(self):
        self.extractLine()
        self.trim()

    def extractLine(self):
        result = re.findall(self.relationRegex, self.text)
        if not result:
            return

        self.result = result[0]

    def trim(self):
        self.trimForFromRelation()
        self.generalTrim()

    def generalTrim(self):
        toRemove = [',', 'a', 'the', 'from', 'of']
        for word in toRemove:
            self.result = re.sub(pattern=f'{word} ', string=self.result, repl='', flags=re.IGNORECASE)

        self.result = self.result.strip()

    def trimForFromRelation(self):
        wordsToKeep = ['or','all', 'learned']
        if 'from' in self.result:
            for word in wordsToKeep:
                if word in self.result:
                    return

            self.result = ''
