import unittest

from parsers.word_relation_marker import WordRelationMarker


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # add assertion here
        a = [
        '''Latin contra (“against, opposite”) + Medieval Latin rotulus, Latin rotula (“roll, a little wheel”)''',
        '''<- co- (intensive prefix) + operiō (“I close, cover”)''',
        '''from  Old English discipul m (“disciple; scholar”) and discipula f (“female disciple”)''',
        '''commūnis (“common, ordinary; of or for the community, public”) + -itās (ultimately from Proto-Indo-European *-teh₂ts (“suffix forming nouns indicating a state of being”))''',
        '''com- + par (“equal”).''',
        '''From Middle English karette and Middle French carotte''',
        '''Compound of Spiel (“game”) + Zeug (“stuff”) or spielen (“to play”) + Zeug (“stuff”).\n''',
        '''Blend of spoon + fork; originally a trademark''''',
        '''from a merger of Proto-Indo-European *n̥dʰér (“under”) and *n̥tér (“inside”).''',         
        '''Anglo-Norman memorie, Old French memoire etc''',        ]

        for i in a:
            print(WordRelationMarker().mark(i))

if __name__ == '__main__':
    unittest.main()
