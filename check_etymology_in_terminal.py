from data_structures import EtymologyPart, Word, ComplexWord
from raw_etymology_getter import RawEtymologyGetter
from parsers.etymology_parser import EtymologyParser
from utilities import pipeline


def check():
    while True:
        word = input("Input word: ")
        if word == "q":
            break

        lang = input("Input Language: ")

        content = RawEtymologyGetter().get(word, lang)

        print(content)

        if not content.text:
            print("didn't Found.")
            continue

        pipeline(content,
                 EtymologyParser().parse,
                 print)


def exhaustiveSearch(word: str, lang: str):
    parser = EtymologyParser()
    getter = RawEtymologyGetter()
    while True:
        print("Checking word", word, lang)
        content = getter.get(word, lang)
        print(content)
        if content.isEmpty():
            break

        result = parser.parse(content)

        print(result)

        last = result.history[-1]

        if isinstance(last.word, Word):
            word = last.word.wordForm
            lang = last.word.lang

        if isinstance(last.word, ComplexWord):
            for word in last.word.components:
                exhaustiveSearch(word.wordForm, word.lang)
