from unittest import TestCase

from data_structures import RawEtymology
from parsers.etymology_parser import EtymologyParser


class TestEtymologyParser(TestCase):
    def get_result_from_text(self, text: str, word="", lang=""):
        test = RawEtymology(word=word, lang=lang,
                            text=text)
        e = EtymologyParser().parse(test)
        print(test.text)
        print()
        print(e)

    def get_result_raw(self, e: RawEtymology):
        print(e.text)
        print()
        print(EtymologyParser().parse(e))

    def test_fill_omitted_lang(self):
        test = RawEtymology(word="Germany", lang="English",
                            text=''', from Latin Germānia (“land of the 
                         Germans”), from Germānī, a people living around and east of the Rhine first attested in the 1st 
                         century B.C.E. works of Julius Caesar and of uncertain etymology.''')
        e = EtymologyParser().parse(test)
        self.assertEqual(e.history[2].word.lang, "Latin")

    def test_move_note(self):
        test = RawEtymology(word="jar", lang="English",
                            text="From Middle English jarre (“jar”), from Medieval Latin jarra, or from Middle French "
                                 "jarre (“liquid measure”) (from Old French jare; modern French jarre (“earthenware "
                                 "jar”)), or from Spanish jarra, jarro (“jug, pitcher; mug, stein”), all from Arabic "
                                 "جَرَّة\u200e (jarra, “earthen receptacle”).\nThe word is cognate with Italian giara "
                                 "(“jar; crock”), Occitan jarro, Portuguese jarra, jarro (“jug; ewer, pitcher”).The "
                                 "verb is derived from the noun.")
        e = EtymologyParser().parse(test)
        print(e)

    def test_receipt(self):
        test = RawEtymology(
            text='From Middle English receipt, receyt, receite, recorded since c.\xa01386 as "statement of '
                 'ingredients in a potion or medicine," from Anglo-Norman or Old Northern French receite (“receipt, '
                 'recipe”) (1304), altered (by influence of receit (“he receives”), from Latin recipit) from Old '
                 'French recete, from Latin receptus, perfect passive participle of recipiō, itself from re- (“back”) '
                 '+ capiō (“I take”). The unpronounced p was later inserted to make the word appear closer to its '
                 'Latin root.\n',
            word='receipt', lang='english')
        e = EtymologyParser().parse(test)
        print(e)

    def test_a(self):
        a = RawEtymology(word="spend", lang="english",
                         text="From Middle English spenden, from Old English spendan (attested especially in compounds "
                              "āspendan (“to spend”), forspendan (“to use up, consume”)), from Proto-West Germanic "
                              "*spendōn ( "
                              "“to spend”), borrowed from Latin expendere (“to weigh out”). Doublet of expend. "
                              "Cognate with "
                              "Old High German spentōn (“to consume, use, spend”) (whence German spenden (“to donate, "
                              "provide”)), Middle Dutch spenden (“to spend, dedicate”), Old Icelandic spenna (“to "
                              "spend”).")

        b = RawEtymology(word="Germany", lang="English",
                         text='''From Middle English Germanie, from Old English Germania, from Latin Germānia (“land of the 
                         Germans”), from Germānī, a people living around and east of the Rhine first attested in the 1st 
                         century B.C.E. works of Julius Caesar and of uncertain etymology. The exonym was said by Strabo to 
                         derive from germānus ("close kin; genuine"), making it cognate with "germane" and "german", 
                         but this seems unsupported. Attempts to derive it from Germanic or Celtic roots since the 18th 
                         century are all problematic, although it is perhaps cognate with the Old Irish gair ("neighbor").''')

        c = RawEtymology(word="smurf", lang="english",
                         text='''''')

    def test_etymonline(self):
        a = RawEtymology(word="problem", lang="english",
                         text='''late 14c., probleme, "a difficult question proposed for discussion or solution; a riddle; a scientific topic for investigation," from Old French problème (14c.) and directly from Latin problema, from Greek problēma "a task, that which is proposed, a question;" also "anything projecting, headland, promontory; fence, barrier;" also "a problem in geometry," literally "thing put forward," from proballein "propose," from pro "forward" (from PIE root *per- (1) "forward") + ballein "to throw" (from PIE root *gwele- "to throw, reach"). )  ''')

        e = EtymologyParser().parse(a)
        print(e)

    def test_slash(self):
        a = RawEtymology(word='slash', lang='english',
                         text='''Originally a verb of uncertain etymology. Possibly from French esclachier (“to break”). Used once in the Wycliffe Bible as slascht but otherwise unattested until 16th century. Conjunctive use from various applications of the punctuation mark ⟨/⟩.''')
        e = EtymologyParser().parse(a)
        print(e)

    def test_void(self):
        a = RawEtymology(word='void', lang='english',
                         text=' From Middle English voide, voyde, from Old French vuit, voide, vuide (modern vide), in turn from a Vulgar Latin *vocitus,')

        e = EtymologyParser().parse(a)
        print(e)

    def test_genus(self):
        a = RawEtymology(word='genus', lang='english',
                         text='From Latin genus (compare stem of the genitive generis)')
        e = EtymologyParser().parse(a)
        print(e)

        # ['{}Middle English spenden', '{}Old English spendan (attested especially in compounds āspendan (“to spend”),
        # forspendan (“to use up, consume”))', '{}Proto-West Germanic *spendōn (“to spend”),', '{}Latin expendere (“to weigh
        # out”)', 'Doublet of expend', 'Cognate with Old High German spentōn (“to consume, use, spend”) (whence German
        # spenden (“to donate, provide”)), Middle Dutch spenden (“to spend, dedicate”), Old Icelandic spenna (“to spend”).']

    def test_sand(self):
        a = RawEtymology(
            text='From Middle English sand, from Old English sand, from Proto-Germanic *samdaz (compare West Frisian sân, Dutch zand, German Sand, Danish, Swedish and Norwegian sand), from Proto-Indo-European *sámh₂dʰos (compare Latin sabulum, Ancient Greek ἄμαθος (ámathos)), from *sem- (“to pour”) (compare English dialectal samel (“sand bottom”), Old Irish do·essim (“to pour out”), Latin sentina (“bilge water”), Lithuanian sémti (“to scoop”), Ancient Greek ἀμάω (amáō, “to gather”), ἄμη (ámē, “water bucket”)).\n',
            word='sand', lang='english')
        e = EtymologyParser().parse(a)
        print(e)

    def test_terrazo(self):
        self.get_result_from_text("From the noun terrazo, or more likely borrowed from French terrasse")

    def test_dikaz(self):
        self.get_result_from_text(
            "From Proto-Germanic *dīkaz (compare Swedish dike, Icelandic díki, West Frisian dyk (“dam”), Dutch dijk (“id.”), German Teich (“pond”))")

    def test_jar(self):
        self.get_result_from_text(
            "From Middle English jarre (“jar”), from Medieval Latin jarra, or from Middle French jarre (“liquid measure”) (from Old French jare; modern French jarre (“earthenware jar”)), or from Spanish jarra, jarro (“jug, pitcher; mug, stein”), all from Arabic جَرَّة\u200e (jarra, “earthen receptacle”).\nThe word is cognate with Italian giara (“jar; crock”), Occitan jarro, Portuguese jarra, jarro (“jug; ewer, pitcher”).The verb is derived from the noun.")

    def test_log(self):
        self.get_result_from_text(
            "From Middle English logge, logg (since 14th century, while its Anglo-Latin derivatives are attested since early 13th century), of unknown origin.\nEnding on -g suggests Scandinavian origin, and it has been proposed: cf. Old Norse lóg, lág (“a felled tree; log”), which is from liggja (“to lie”), or its regular reflex Norwegian låg (“fallen tree”), which could have been borrowed through the Norwegian timber trade. However the Old Norse/Middle Norwegian vowel is long while Middle English vowel is short.")

    def test_regular(self):
        self.get_result_from_text(
            "From Middle English reguler, from Anglo-Norman reguler, Middle French reguler, regulier, and their source, Latin rēgulāris (“continuing rules for guidance”), from rēgula (“rule”), ultimately from Proto-Indo-European *reg- (“move in a straight line”).\n'")

    def test_masca(self):
        self.get_result_from_text("'From (a byform of, see it for more) Medieval Latin masca, mascha'")

    def test_grima(self):
        self.get_result_from_text(
            "Replaced Old English grīma (“mask”), whence grime, and displaced non-native Middle English viser (“visor, mask”)")

    def test_murmur(self):
        test = RawEtymology(
            text='From Middle English murmur, murmor, murmour, from Old French murmure (modern French murmure), from Latin murmur (“murmur, humming, muttering, roaring, growling, rushing etc.”).\n',
            word='murmur', lang='english')
        self.get_result_raw(test)

    def test_shirt(self):
        test = RawEtymology(
            text='From Middle English sherte, shurte, schirte, from Old English sċyrte (“a short garment; skirt; kirtle”), from Proto-West Germanic *skurtijā, from Proto-Germanic *skurtijǭ (“a short garment, skirt, apron”).\nCognate with Saterland Frisian Schoarte (“apron”), Dutch schort (“apron”), German Schürze (“apron”), Danish skjorte (“shirt”), Norwegian skjorte (“shirt”), Swedish skjorta (“shirt”), Faroese skjúrta (“shirt”), Icelandic skyrta (“shirt”). \nEnglish skirt is a parallel formation from Old Norse; which is a doublet of short, from the same ultimate source.\n',
            word='shirt', lang='english')
        self.get_result_raw(test)

    def test_doler(self):
        self.get_result_raw(RawEtymology(
            text='From Old Spanish doler, from Latin dolēre, present active infinitive of doleō, from Proto-Italic *doleō (“hurt, cause pain”), from Proto-Indo-European *dolh₁éyeti (“divide”), from *delh₁- (“cut”).\n',
            word='doler', lang='spanish'))

    def test_3(self):
        self.get_result_from_text(
            'From Old English port, borrowed from Latin portus (“port, harbour”), ultimately from Proto-Indo-European *pértus (“crossing”) (and thus distantly cognate with ford). The directional sense derived from ancient vessels with the steering oar on the right (see etymology of starboard), which therefore had to moor with their left sides facing the dock or wharf.\n')

    def test_sker(self):
        self.get_result_from_text('From the Proto-Indo-European *(s)ker- (“to turn, to bend”).')

    def test_rubble(self):
        self.get_result_raw(RawEtymology(
            text='From Middle English rouble, rubel, robel, robeil, from Anglo-Norman *robel (“bits of broken stone”). Presumably related to rubbish, originally of same meaning (bits of stone). Ultimately presumably from Proto-Germanic *reufaną (“to tear”), *raubōną (“to rob, steal, plunder”), perhaps via Old French robe (English rob (“steal”)) in sense of “plunder, destroy”; see also Middle English, Middle French -el.\n',
            word='rubble', lang='english'))

    def test_rubble_last_part(self):
        self.get_result_from_text(
            "bla, perhaps via Old French robe (English rob (“steal”)) in sense of “plunder, destroy”; see also Middle English, Middle French -el.")

    def test_guard(self):
        self.get_result_from_text('From Old French coart, cuard ( > French couard)')

    def test_ter(self):
        self.get_result_from_text('From Ottoman Turkish تر\u200e (ter, “sweat”), Proto-Turkic *dẹr (“sweat”),')

    def test_soil(self):
        self.get_result_raw(RawEtymology(
            text='From Middle English soile, soyle, sule (“ground, earth”), partly from Anglo-Norman soyl (“bottom, ground, pavement”), from Latin solium (“seat, chair; throne”), mistaken for Latin solum (“ground, foundation, earth, sole of the foot”); and partly from Old English sol (“mud, mire, wet sand”), from Proto-Germanic *sulą (“mud, spot”), from Proto-Indo-European *sūl- (“thick liquid”). Cognate with Middle Low German söle (“dirt, mud”), Middle Dutch sol (“dirt, filth”), Middle High German sol, söl (“dirt, mud, mire”), Danish søle (“mud, muck”). Compare French seuil (“level; threshold”) and sol (“soil, earth; ground”). See also sole, soal, solum.\n',
            word='soil', lang='english'))

    def test_shrimp(self):
        self.get_result_raw(RawEtymology(
            text='From Middle English schrimpe (“shrimp, puny person”), ultimately from Proto-Germanic *skrimpaz (“shrivelled”) (compare Middle High German schrimpf (“a scratch, minor wound”), Norwegian skramp (“thin horse, thin man”)), from Proto-Germanic *skrimpaną (“to shrivel”) (compare Old English sċrimman (“to shrink”) and scrimp, Middle High German schrimpfen (“to shrink, dry up”), Swedish skrympa (“to shrink”)), from Proto-Indo-European *skremb-, *skr̥mb- (compare Lithuanian skrembti (“to crust over, stiffen”), and possibly Albanian shkrumb (“embers, ashes; crumble”)).\n',
            word='shrimp', lang='english'))

    def test_skremb(self):
        self.get_result_from_text('{}Proto-Indo-European *skremb-, *skr̥mb- (compare Lithuanian skrembti (“to crust over, stiffen”), and possibly Albanian shkrumb (“embers, ashes; crumble”))')

    def test_change(self):
        self.get_result_from_text('''Euphemistic form of 姮娥 (Héng'é) from the Han dynasty, since 姮 (héng) is homophonous with 恆／恒 (héng),''')