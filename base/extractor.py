class Extractor:
    def __init__(self, text: str = ""):
        self.text = text
        self.result = ""

    def extract(self, text):
        if not text:
            return text

        self.text = text
        self.result = ""

        self.process()

        return self.result

    def process(self):
        pass

    def textLeft(self) -> str:
        return ""
