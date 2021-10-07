from dataclasses import dataclass

from typing import Dict, List


@dataclass
class Text:
    value: str

    def __getitem__(self, item):
        return self.value[item]


@dataclass
class Word:
    wordForm: str
    lang: str
    note: str

    def __str__(self):
        return f"wordForm: {self.wordForm}\nlang: {self.lang}\nnote: {self.note}\n"


@dataclass
class Relation:
    _wordDelimiter: str
    _langDelimiter: str = "/"

    @property
    def wordDelimiter(self):
        return f" {self._wordDelimiter} "

    @property
    def langDelimiter(self):
        return f" {self._langDelimiter} "


class ComplexWord:
    def __init__(self,
                 components: List[Word],
                 relation: Relation,
                 _note: str = ""
                 ):
        self.components = components
        self.relation = relation
        self._note = _note

    @property
    def lang(self):
        langs = [word.lang for word in self.components if word.lang]
        if not langs:
            return ""

        return self.relation.langDelimiter.join(langs)

    @lang.setter
    def lang(self, value):
        for word in self.components:
            if not word.lang:
                word.lang = value

    @property
    def wordForm(self):
        return self.relation.wordDelimiter.join([word.wordForm for word in self.components])

    @wordForm.setter
    def wordForm(self, value):
        self.components[0].wordForm = value

    @property
    def note(self):
        notes = [(word.wordForm, word.note) for word in self.components if word.note]

        if len(notes) == 0:
            return self._note

        return self._note + "\n".join([f"{word}: {note};" for (word, note) in notes])

    @note.setter
    def note(self, value):
        self.components[0].note += value

    def __str__(self):
        return f"wordForm: {self.wordForm}\nlang: {self.lang}\nnote: {self.note}"


@dataclass
class References:
    type: str = ""
    words: List[ComplexWord] = None

    def __str__(self):
        words = "\n".join([f"{word}" for word in self.words])
        return f"{self.type} {{\n{words}}}\n\n"

    def __getitem__(self, item):
        return self.words[item]

    def __len__(self):
        return len(self.words)


@dataclass
class EtymologyPart:
    word: Word
    references: References

    def __str__(self):
        if not self.references:
            return f"{self.word}"

        return f"{self.word}\n{self.references}"

    @property
    def lang(self):
        return self.word.lang


@dataclass
class CurrentWord:
    word: Word
    references: List[References]

    def __str__(self):
        result = f"{self.word}"
        for reference in self.references:
            result += str(reference)

        return result

    @property
    def lang(self):
        return self.word.lang


@dataclass
class Etymology:
    prefix: str
    history: list[CurrentWord, EtymologyPart]
    relations: list[str]

    def __str__(self):
        result = f"{self.history[0].word}"

        for item, relation in zip(self.history[1:], self.relations):
            if relation:
                result += f"↑{relation}\n{str(item)}\n"
            else:
                result += f"{str(item)}\n"

        references = ""
        for reference in self.history[0].references:
            references += str(reference)

        return f"{result}\n\n{references}"


@dataclass
class RawEtymology:
    text: str
    word: str
    lang: str

    def isEmpty(self):
        return not bool(self.text)


@dataclass
class EtymologyText:
    word: str
    lang: str
    note: str
    toParse: Dict[str, str]
