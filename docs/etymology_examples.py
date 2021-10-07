from wiktionary import *


def getEtymologyExamplesInBatch(query: dict):
    etymologies = ""
    for lang, words in query.items():
        for word in words:
            etymologies += word
            etymologies += getRawEtymologyFromWiktionary(word, lang)
            etymologies += "\n"
            print(f"completed:{word}")

    with open("raw_texts.md", "a") as f:
        f.write(etymologies)


def getRawEtymologyTexts(lang, *words):
    etymologies = ""
    for word in words:
        etymologies += word + "\n"
        etymologies += getRawEtymologyFromWiktionary(word, lang)
        etymologies += "\n"
        print(f"completed:{word}")

    with open(f"{lang}_{words[0]}-{words[-1]}.md", "a") as f:
        f.write(etymologies)


def getVariousEtymologyExamples():
    query = {"English": ["word", "phrase", "chart", "pie", "fascinate", "contemplate"],
             "Spanish": ["primavera", "cuero", "pollo", "playa", "ojo", "colección"],
             "Turkish": ["feshetmek", "aktarmak", "mihver", "doğru", "galiba", "sınav"]}

    getEtymologyExamplesInBatch(query)


def getTurkishEtymologyExamples():
    query = {"Turkish": ["abdestbozan",
                         "abdestbozan otu",
                         "abdesthane",
                         "abdestli",
                         "abdestlik",
                         "abdestlilik",
                         "abdestsiz",
                         "abdestsizlik",
                         "abdiâciz",
                         "abdülleziz",
                         "abece",
                         "abece sırası",
                         "abecesel",
                         "aberasyon",
                         "abes"]}
    getEtymologyExamplesInBatch(query)


def getEnglishEtymologyExamples():
    # source: https://www.ef.com/wwen/english-resources/english-vocabulary/top-1000-words/
    eng = {"English": ["come",
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
                       ]}

    getEtymologyExamplesInBatch(eng)


getRawEtymologyTexts("english", "spend", "create", "fathom", "seek", "preach", "solumn")
getRawEtymologyTexts("turkish", "çırak", "feshetmek", "merak","makara")
