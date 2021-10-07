import re
from re import Match

from more_itertools import chunked


def pipeline(item, *steps):
    for step in steps:
        item = step(item)

    return item


def splitAndStrip(line: str, delimiter):
    # if x means x is not falsy
    return [x.strip() for x in line.split(delimiter) if x]


def savePairs(words: list[str]) -> list[str]:
    # can't delete based on index because index would change after deletion
    if len(words) < 2:
        return words

    pair = ("(", ")")
    # () for later

    unmatched = []
    for i, word in enumerate(words):
        begin, end = pair

        if word.count(begin) != word.count(end):
            unmatched.append(i)

    if not unmatched:
        return words

    for begin, end in chunked(unmatched, 2):
        for i in range(begin + 1, end + 1):
            words[begin] += ", " + words[i]
            words[i] = ""

    return [x for x in words if x]


def wrappedList(x: list):
    if not x:
        return ""

    return "\n".join([item.__str__() for item in x])


def startingIndices(source: str, toIndex: str) -> list[int]:
    return [match.start() for match in re.finditer(toIndex, source)]


def isMarkedWithinPairedSymbol(text: str, result: Match, symbol: tuple[str, str]) -> bool:
    indices = sorted(startingIndices(text, symbol[0]) + startingIndices(text, symbol[1]))
    for start, end in chunked(indices, 2):
        if start < result.start() and result.end() < end:
            return True

    return False


def isMarkedWithinParenthesis(text: str, result: Match) -> bool:
    return isMarkedWithinPairedSymbol(text, result, (r'\(', r'\)'))


def isMarkedWithinApostrophe(text: str, result: Match) -> bool:
    return isMarkedWithinPairedSymbol(text, result, ('“', '”'))


def removeOutmostParenthesis(text: str):
    if text.startswith("(") and text.endswith(")"):
        return text.removeprefix("(").removesuffix(")")

    return text
