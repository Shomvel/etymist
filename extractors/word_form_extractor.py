from base.extractor import Extractor


class WordFormExtractor(Extractor):
    def __init__(self, text: str = ""):
        super().__init__(text)

    def process(self):
        self.result = self.text.strip()\
            .removesuffix(",")\
            .removesuffix(".")\
            .replace("as well", "")\
            .strip()

