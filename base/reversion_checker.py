from data_structures import Text


class ReversionChecker:
    def __init__(self):
        self._text = Text("")

    @property
    def text(self):
        return self._text.value

    @text.setter
    def text(self, value: str):
        self._text.value = value

    def getCheckers(self):
        return (getattr(self, name) for name in dir(self) if name.startswith("isMarked"))
