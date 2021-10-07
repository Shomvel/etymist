import unittest
from parsers.plain_word_parser import PlainWordParser


class MyTestCase(unittest.TestCase):
    def test_something(self):
        lines = ["Gaulish dūnom (“hill, hillfort”)",
                 "Proto-Celtic *dūnom (compare archaic Welsh din (“hill”), Irish dún (“fortress”))",
                 "Proto-Indo-European *dewh₂- (“to finish, come full circle”)",
                 "Middle English word",
                 "Proto-West Germanic *word",
                 "Proto-Germanic *wurdą",
                 "Proto-Indo-European *wr̥dʰh₁om",
                 "Late Latin phrasis (“diction”)",
                 "Ancient Greek φράσις (phrásis, “manner of expression”)",
                 "φράζω (phrázō, “I tell, express”)",
                 "Middle French charte (“card, map”)",
                 "Ancient Greek χάρτης (khártēs, “papyrus, thin sheet”)"]

        for line in lines:
            print(PlainWordParser().parse(line))

    def test_descendants(self):
        line = "descendants"
        print(PlainWordParser().parse(line))

    def test_only_lang(self):
        line = "From Old Japanese"
        print(PlainWordParser().parse(line))

    def test_carier(self):
        line = "Anglo-Norman carier (modern French charrier);"
        print(PlainWordParser().parse(line))

    def test_greek(self):
        line = 'Ancient Greek βαμβαίνω (bambaínō), βαμβαλύζω (bambalúzō, “I chatter with the teeth”)'
        print(PlainWordParser().parse(line))


if __name__ == '__main__':
    unittest.main()
