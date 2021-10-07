from splitter.text_splitter import TextSplitter
from wiktionary import *
from more_itertools import chunked


def testGetEtymologyItemBatch():
    tests = ["Gaulish dūnom (“hill, hillfort”)",
             "Proto-Celtic *dūnom (compare archaic Welsh din (“hill”), Irish dún (“fortress”))",
             "Proto-Indo-European *dewh₂- (“to finish, come full circle”)",
             "Middle English word",
             "Old English word",
             "Proto-West Germanic *word",
             "Proto-Germanic *wurdą",
             "Proto-Indo-European *wr̥dʰh₁om",
             "Late Latin phrasis (“diction”)",
             "Ancient Greek φράσις (phrásis, “manner of expression”)",
             "φράζω (phrázō, “I tell, express”).",
             "Middle French charte (“card, map”)",
             "Late Latin charta (“paper, card, map”), Latin charta (“papyrus, writing”)",
             "Ancient Greek χάρτης (khártēs, “papyrus, thin sheet”)"]

    for item in tests:
        # e = getEtymologyItem(item)
        from parsers.plain_word_parser import PlainWordParser
        print(PlainWordParser().parse(item))
        print()


def testGetReferenceWords():
    #
    texts = [
        "Compare Portuguese praia, French plage, Italian spiaggia.",
        "Cognate to Portuguese olho, French œil, Italian occhio, Romanian ochi, Russian око (oko).",
        "Cognate with Kyrgyz туура (tuura), Uzbek toʻgʻri, Old Turkic toğru, toğuru, toğrı‎ (toğru, toğuru, "
        "toğrı), derivative from Old Turkic toğur-",
        "Compare Italian primavera and Romanian primăvară.",
        "Compare also Saterland Frisian Kop (“cup”), West Frisian kop (“cup”), Dutch kop (“cup”), German Low "
        "German Koppke, Köppke (“cup”), Danish kop (“cup”),Swedish kopp (“cup”)",
        "Displaced native Middle English thecchen and bethecchen (“to cover”) (from Old English þeccan, "
        "beþeccan (“to cover”)), Middle English helen, (over),helen, (for)helen (“to cover, conceal”) (from Old "
        "English helan (“to conceal, cover, hide”)), Middle English wrien, (be)wreon (“to cover”) (from Old "
        "English (be)wrēon (“to cover”)), Middle English hodren, hothren (“to cover up”) (from Low German hudren "
        "(“to cover up”)). "
    ]

    referenceType = ['Compare', 'Cognate to', 'Cognate with']
    # bug: multiple wordforms
    # for prefix, test in tests.items():
    #     # print(getReferenceWords(test, prefix))
    #     print(ReferenceWords(prefix, getReferenceWords(test, prefix)))
    #     print()

    for line in texts:
        from extractors.reference_extractor import ReferenceExtractor

        print(ReferenceExtractor().extract(line))


def testGetEtymology(word: str, lang: str):
    e = getRawEtymologyFromWiktionary(word, lang)
    print(e)
    print("\n".join(splitEtymologyText(e)))
    print()
    etymology = processEtymology(splitEtymologyText(e), word, lang)
    printEtymologyItemTable(etymology.etymologyItems)
    print(etymology.references)
    print(etymology.notes)


def testGetStructuredEtymologiesWithEnglishExample():
    eng = ["come",
           "commercial",
           "common",
           "community",
           "company",
           "compare",
           "computer",
           "concern",
           "condition",
           "conference",
           "Congress",
           "consider",
           "consumer",
           "contain",
           "continue",
           "control",
           "cost",
           "could",
           "country",
           "couple",
           "course",
           "court",
           "cover",
           "create",
           "crime",
           "cultural",
           "culture",
           "cup",
           "current",
           "customer"
           ]
    for word in eng:
        testGetEtymology(word, "english")


def testSplitEtymology():
    print(splitEtymologyText(getRawEtymologyFromWiktionary("culture", "english")))


def testGetEtymologyItemForCulture():
    s = "from cultus, perfect passive participle of colō (“till, cultivate, worship”) (related to colōnus and colōnia)"
    print(getEtymologyItem(s, "from"))


def testGetEtymItemForLunes():
    s = "from Latin Lūnae dīēs, variant of dīēs Lūnae"
    print(getEtymologyItem(s, "from"))


def testGetNote():
    lines = [
        "calque  Latin pomum Adami, which is found in the botanical sense from 1560 and the anatomical sense from 1600",
        "from Proto-Germanic *kwemaną (“to come”)", ]

    for line in lines:
        print(getNote(line))


def testGetEtymologyItem(s: str, marker: str):
    print(getEtymologyItem(s, marker))


# telluric


def testProcessCompoundFormation():
    compounds = ["from Latin verbum (“word”) + -ātim (adverbial suffix)",
                 "from ager (“field”) + cultura (“cultivation”)",
                 "from Medieval Latin identicus + Latin faciō",
                 "contra “against, opposite” + Medieval Latin rotulus, Latin rotula “roll, a little wheel”, diminutive of rota “a wheel”"
                 ]
    for compound in compounds:
        print(processCompoundFormation(compound))


# problem: 'NoneType' object has no attribute 'wordForm'

# arabic issue


def testMergeSource():
    s = "particuler, Middle French particuler, particulier"
    print(mergeSource(s.split(",")))


def testFromLanguage():
    s = ["from Anglo-Norman"]
    print(processEtymology(s, "pork", "English"))


# bug from:
# from as meaning
# form:

# todo: make item of grammar info
# todo: no splitting if it's inside apostrophes

# apostrophe: or linked
# siglo


# todo: bugs logger
def testACalqueOf():
    s = "A calque of the German word Kommunismus (from Marx and Engels's Manifesto of the Communist Party, published in 1848)"
    print(splitEtymologyText(s))


def testSavePairs():
    s = "The verb is derived from Middle English embracen (“to clasp in one's arms, embrace; to reach out eagerly for, welcome; to enfold, entwine; to ensnare, entangle; to twist, wrap around; to gird, put on; to lace; to be in or put into bonds; to put a shield on the arm; to grasp (a shield or spear); to acquire, take hold of; to receive; to undertake; to affect, influence; to incite; to unlawfully influence a jury; to surround; to conceal, cover; to shelter; to protect; to comfort; to comprehend, understand”) [and other forms], from Old French embracer, embracier (“to kiss”) (modern French embrasser (“to kiss; (dated) to embrace, hug”)), from Late Latin *imbracchiāre, from in- (prefix meaning ‘in, inside, within’)) + bracchium (“arm”). The English word is analysable as em- +‎ brace.The noun is derived from the verb."
    words = splitEtymologyText(s)
    saved = savePairs(words)
    for i, word in enumerate(saved):
        print(f"{i}: {word}")


# black ditch
# ditch experiences lag
# EtymNotes
# cola < coda
# use re
# make a proper
# record history
# compare two words
# regex to get


def processExamples():
    splitter = TextSplitter()
    with open("../docs/english_spend-solumn.md", "r") as f:
        for word, text, empty in chunked(f.readlines(), 3):
            splitter = TextSplitter()
            print(word)
            print(text)
            print("\n".join(splitter.split(text)))


testGetEtymology("apple", "english")
