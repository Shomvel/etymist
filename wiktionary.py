from wiktionaryparser import WiktionaryParser
from more_itertools import pairwise
from utilities import *

# somehow only succeeds when using iPhone hotspot
# suspect: handshake

phrasesMap = {"older": ["from older"],
              "merger": ["from a merger of",
                         "from the merger of"],
              "alteration": ["from alteration of"],
              "from": ["from",
                       "borrowed from",
                       ": from",
                       "; from",
                       '” from',
                       ") from",
                       "itself borrowed from",
                       "itself from",
                       "and its source",
                       "perhaps a loanword from",
                       "inherited from",
                       "derived from",
                       "a borrowing of",
                       "both from",
                       "originally in",
                       "subsequently also from",
                       "probably from",
                       "perhaps from",
                       "possibly from",
                       "which is possibly from",
                       "which was formed from",
                       "ultimately from",
                       "combined form of",
                       "via"],
              "learned borrowing": ["learned Borrowing from"],
              "semi-learned term": ["a semi-learned term derived from"],
              "ellipsis": ["ellipsis of"],
              "calque": ["a calque of the ",
                         "a calque of",
                         "calque of",
                         "in turn a calque of the"],
              "extended form of prev": ["extended form of"],
              "shortening of prev": ["shortening of"],
              "conflation of": ["conflation of"],
              "clipping": ["clipping of"]}  # for etymology of the word "communism"


class EtymologyPart:
    def __init__(self,
                 lang: str,
                 wordForm: str,
                 note: str):
        self.lang = lang
        self.wordForm = wordForm
        self.note = note

    def __repr__(self):
        return f"lang: {self.lang}\nwordForm: {self.wordForm}\nnote: {self.note}\n"


class ReferenceWords:
    def __init__(self,
                 referenceType: str,
                 items: list[str]):
        self.type = referenceType
        self.items = [i.strip() for i in items]

    def __repr__(self):
        s = "\n".join(self.items)
        return f"{self.type}: \n{s}\n"


class Etymology:
    def __init__(self,
                 etymologyItems: list[EtymologyPart],
                 references: list[ReferenceWords],
                 notes: list[str]):
        self.etymologyItems = etymologyItems
        self.references = references
        self.notes = notes


def getRawEtymologyFromWiktionary(word: str, language: str):
    parser = WiktionaryParser()
    content = parser.fetch(word, language)
    if not content:
        return ""
    else:
        return content[0]['etymology']


def splitEtymologyText(etymology: str) -> list[str]:
    delimiter = "|"

    global phrasesMap

    # todo: check more calques

    for note, phrases in phrasesMap.items():
        itemMarker = delimiter + note + " "

        for phrase in phrases:
            etymology = etymology.replace(phrase.capitalize(), itemMarker) \
                .replace(f", {phrase}", itemMarker)

    etymology = etymology.replace(".", delimiter).replace("c" + delimiter, "c.").replace(delimiter + "c", ".c")
    # c. 1386, cf. receipt
    # "From"
    # ", from"
    # keep "from" as a marker for etymology items

    return splitAndStrip(etymology, delimiter)


def makeCalqueNotes(items: list[EtymologyPart]):
    for a, b in pairwise(items):
        if "calque" in b.note:
            b.note = b.note.replace("calque", "")
            a.note += f"a calque of {b.wordForm}"

    return items


def processEtymology(etymologyLines: list[str], word: str, lang: str):
    etymologyItems = [EtymologyPart(wordForm=word, lang=lang.capitalize(), note=str())]
    references = []
    notes = []

    for line in etymologyLines:
        isNote = True

        referenceType = getReferenceType(line)
        if referenceType != "Not Typed":
            isNote = False
            references.append(ReferenceWords(referenceType, getReferenceWords(line, referenceType)))

        global phrasesMap
        for marker in phrasesMap.keys():
            if line.startswith(marker):
                isNote = False

                if "+" in line:
                    item = processCompoundFormation(line)
                elif "merger" in line:
                    item = processMerger(line)
                else:
                    item = getEtymologyItem(line, marker)

                etymologyItems.append(item)

                break

        if isNote:
            notes.append(line)

    etymologyItems = pipeline(etymologyItems,
                              fillOmittedLang,
                              makeCalqueNotes)

    return Etymology(etymologyItems, references, notes)


def getReferenceType(line: str):
    referenceTypes = [
        "Doublet of",
        "Cognate to",
        "Cognate with",
        "Akin to",
        "See also",
        "See",
        "More at",
        "Cognate with",
        "Displaced",
        "Eclipsed",
        "Compare also",
        "Compare",
        "Related also to",
        "Related to",
        "Merged with"
        "equivalent to",
    ]
    for referenceType in referenceTypes:
        if line.startswith(referenceType) or line.startswith(referenceType.lower()):
            return referenceType

    return "Not Typed"


def fillOmittedLang(etymologyItems: list[EtymologyPart]):
    # eg from a word, someNote
    # not: from Anglo-Norman
    for index, item in enumerate(etymologyItems):
        fillLang = False
        if item.wordForm is str() and item.note is not str():
            item.wordForm = item.lang
            fillLang = True
            # eg from a word, someNote

        if item.lang is str():
            fillLang = True

        if fillLang:
            item.lang = etymologyItems[index - 1].lang

    # for situation: from aWord -> lang,
    # problem: from Middle English,
    return etymologyItems


def getReferenceWords(etymologyLine: str, prefix: str):
    return pipeline(etymologyLine
                    .removeprefix(prefix)
                    .removeprefix(prefix.lower())
                    .replace(", and", ",|")
                    .replace("), ", ")|")
                    .replace(", ", ",|")
                    .split("|"),
                    savePairs)


# todo: case: Lang word1, word2


def getEtymologyItem(etymologyLine: str, marker: str):
    # input eg: "from Middle English privilege ("privilege")"
    # output: EtymologyItem containing following information:
    #         wordform: privilege
    #         lang: Middle English
    #         note: "privilege"
    if etymologyLine is str():
        return

    etymologyLine = etymologyLine.removeprefix(marker).strip()
    language = getLanguageName(etymologyLine)
    etymologyLine = etymologyLine.removeprefix(language).strip().removeprefix("word").strip()
    # German word
    note = getNote(etymologyLine)
    etymologyLine = deleteNote(etymologyLine)
    if marker != "from":
        if note == str():
            note += marker
        else:
            note += f"; {marker}"

    wordForm = etymologyLine.strip().replace(".", "").removesuffix(",")

    return pipeline(EtymologyPart(language, wordForm, note),
                    moveGrammarInfoToNote,
                    moveNoteInWordForm,
                    formatNote)


def formatNote(item: EtymologyPart):
    item.note = item.note \
        .replace("(“", "“") \
        .replace("”)", "”") \
        .replace("\n\n", "") \
        .removesuffix(",")

    return item


def moveNoteInWordForm(item: EtymologyPart):
    if ", which" in item.wordForm:
        start = item.wordForm.find("which")
        note = item.wordForm[start:]
        item.note += note
        item.wordForm = item.wordForm.removesuffix(note)

    return item


def getSourceLink(item: EtymologyPart):
    for delimiter in [",", "and", ", or"]:
        if hasTwoSourcesWithDelimiter(item.wordForm, delimiter):
            return delimiter

    return None


def hasTwoSourcesWithDelimiter(line: str, delimiter: str):
    if delimiter not in line:
        return False

    if len(line) != len(delimiter):
        return False

    items = splitAndStrip(line, delimiter)
    diffs = [abs(len(b) - len(a)) > 5 for a, b in pairwise(items)]
    for diff in diffs:
        if diff:
            return True

    return False
    # if they are only two word forms connected by delimiter
    # instead of one having a language name if it's a source
    # then the difference would be small
    # i set it to be 5


def processMerger(line: str):
    # todo: refactor
    if "merger" not in line:
        return

    lang = getLanguageName(line)
    line = line.removeprefix(lang)

    items = [getEtymologyItem(x.strip(), "") for x in line.removeprefix("a merger").split("and")]

    for item in items:
        if item.wordForm == str():
            # eg: original: prīvus (“private”)
            item.wordForm = item.lang
            item.lang = str()

        if item.lang.endswith(","):
            # eg: original: lēx, lēg-
            item.wordForm = item.lang + item.wordForm
            item.lang = str()

    wordForm = f"{items[0].wordForm} + {items[1].wordForm}"
    # todo: Refactor
    # cf. move two sources

    note = "\n".join([f"{item.wordForm}: {item.note}" for item in items])
    lang = ""
    for item in items:
        if item.lang != str():
            lang += item.lang
            # may cause problems!

    return EtymologyPart(lang, wordForm, note)


def processCompoundFormation(line: str):
    if "+" not in line:
        return

    items = [getEtymologyItem(x.strip(), "") for x in line.removeprefix("from").split("+")]

    for item in items:
        if item.wordForm == str():
            # eg: original: prīvus (“private”)
            item.wordForm = item.lang
            item.lang = str()

        if item.lang.endswith(","):
            # eg: original: lēx, lēg-
            item.wordForm = item.lang + item.wordForm
            item.lang = str()

    wordForm = f"{items[0].wordForm} + {items[1].wordForm}"
    # todo: Refactor
    # cf. move two sources
    # todo: dont add note if there isn't
    note = "\n".join([f"{item.wordForm}: {item.note}" for item in items])
    lang = ""
    for item in items:
        if item.lang != str():
            lang += item.lang
            # may cause problems!
    return EtymologyPart(lang, wordForm, note)


def moveGrammarInfoToNote(item: EtymologyPart):
    # eg xx ,diminutive of yy; xx, past participle of yy
    if "of" not in item.wordForm:
        return item

    start = item.wordForm.find(",")
    grammarInfo = item.wordForm[start:]
    item.note += grammarInfo
    item.wordForm = item.wordForm.removesuffix(grammarInfo)

    return item


def getFirstWordsFromList(words: list[str], count: int):
    return " ".join(words[0:count])


def beginsWithTwoWordedLanguageName(words: list[str]):
    if len(words) < 2:
        return False

    periods = ['Old', 'Ancient', 'Late', 'Middle', 'Classical', 'Medieval', 'Archaic']
    # like Old English, Ancient Greek, Middle English
    languageFamilies = ['Germanic', 'Arabic', 'Chinese', 'Latin', 'Turkish']
    # like Vulgar Latin, Ancient Chinese, Ottoman Turkish
    specialCases = ["Tocharian B", "Min Nan"]

    locations = ["Northern", "Western", "Eastern", "Southern"]
    # like

    firstTwo = getFirstWordsFromList(words, 2)

    return words[0] in periods or \
           words[0] in locations or \
           words[1] in languageFamilies or \
           firstTwo in specialCases


def beginsWithThreeWordedLanguageName(words: list[str]):
    if len(words) < 3:
        return False

    heights = ["Low", "High", "Middle"]
    # eg Late Middle English
    # Old Low German
    # Middle High German~
    locations = ["Northern", "Western", "Eastern", "Southern"]
    # Old Northern French
    slavic = ["Slavonic", "Slavic"]
    # Old Church Slavonic
    # Old East Slavic
    return words[1] in heights or words[2] in slavic or words[1] in locations


# todo: make extracting language name a class

def getLanguageName(etymologyLine: str):
    words = etymologyLine.split(" ")

    return getConnectedLanguageName(words) or getSingleLanguageName(words)


def getConnectedLanguageName(words: list[str]):
    # example Hakka and Min / Anglo-Norman or Old Northern French
    for linker in ["or", "and"]:
        if linker in words:
            linkerIndex = words.index(linker) + 1

            if linkerIndex > 4:
                return ""
            # to be adjusted

            return " ".join(words[:linkerIndex]) + " " + getSingleLanguageName(words[linkerIndex:])

    return ""


def getSingleLanguageName(words: list[str]):
    # 用时期检验的话，对于三个字的语言名，同样能通过 hasTwoWordedLanguageName 的检验
    # 因此先检验 hasThreeWordedLanguageName
    if beginsWithThreeWordedLanguageName(words):
        return getFirstWordsFromList(words, 3)

    if beginsWithTwoWordedLanguageName(words):
        return getFirstWordsFromList(words, 2)

    # 应对情况：不加语言名，eg from cohors
    # 检测依据：语言名首字母大写
    # 可能例外：德语名词首字母大写
    if words[0][0].isupper():
        return words[0]

    return ""


def getNote(etymologyLine: str):
    noteDelimiter = getNoteDelimiter(etymologyLine)
    if noteDelimiter == "N":
        return str()

    noteLeftEnd = etymologyLine.find(noteDelimiter) + len(noteDelimiter) - 1
    return etymologyLine[noteLeftEnd:]


def getNoteDelimiter(etymologyLine: str):
    for marker in ["(", ", which", "but"]:
        if marker in etymologyLine:
            return marker

    return "N"


def deleteNote(etymologyLine: str):
    noteDelimiter = getNoteDelimiter(etymologyLine)
    if noteDelimiter == "N":
        return etymologyLine

    return etymologyLine.replace(etymologyLine[etymologyLine.find(noteDelimiter):], "")


def printEtymologyItemTable(etymologyItems: list[EtymologyPart]):
    from prettytable import PrettyTable

    table = PrettyTable()
    table.field_names = ["wordForm", "lang", "note"]
    table.align["wordForm"] = "l"
    table.align["lang"] = "c"
    table.align["note"] = "l"

    for item in etymologyItems:
        if item:
            table.add_row([item.wordForm, item.lang, item.note])

    print(table)


def formatEtymology(etymology: str):
    #   function: format the etymology as follows:
    #   word
    #   <- Language1 word1
    #   <- Language2 word2
    #   From, from, <- <
    #   naive version
    return "\n<- ".join([item for item in splitEtymologyText(etymology)])


def getEtymologyFromWiktionary(word: str, language: str):
    print(word)
    rawEtymology = getRawEtymologyFromWiktionary(word, language)
    if rawEtymology is str():
        print("Word not found or no etymology exists.")
        return
    else:
        print(formatEtymology(getRawEtymologyFromWiktionary(word, language)))


# Todo 默认值
def checkEtymologyInTerminal():
    while True:
        word = input("Input word: ")
        if word == "q":
            break

        langInput = input("Input Language: ")
        getEtymologyFromWiktionary(word, langInput)

# checkEtymologyInTerminal()
