import re
from re import Match

from base.relation_marker import RelationMarker
from base.reversion_checker import ReversionChecker
from utilities import isMarkedWithinParenthesis, isMarkedWithinApostrophe


class WordReversionChecker(ReversionChecker):
    def __init__(self):
        super().__init__()

    def isMarkedAfterParenthesis(self, match: Match):
        if match.start() == 0:
            return False

        return self.text[match.start() - 1] == ')'

    def isMarkedAfterWordAndLanguage(self, match: Match):
        text = self.text[match.start() - 30:match.start()]
        return bool(re.search(r'[A-Z][a-z-]+ [a-z]+ {}'.format(match.group('relation')), text))

    def isMarkedWithinParenthesis(self, result: Match) -> bool:
        return isMarkedWithinParenthesis(self.text, result)

    def isMarkedWithinApostrophe(self, result: Match) -> bool:
        return isMarkedWithinApostrophe(self.text, result)


class WordRelationMarker(RelationMarker):
    def __init__(self):
        super().__init__(WordReversionChecker())
        self.reversionChecker.text = self.text
        self.findRelationText = r'[andor+, ]'
        self.findRelation = re.compile(fr'\[(?P<relation>{self.findRelationText}+)\]')

    def markRelations(self):
        # consider ", or"
        signs = [', or ',
                 r', ',
                 r' and ',
                 r' or ',
                 r' \+ ',
                 r"/"]
        for sign in signs:
            if sign == r' \+ ':
                toReplace = '[+]'
                # regex issues
            elif sign == ', or ':
                toReplace = '[or]'
            else:
                toReplace = fr'[{sign}]'

            self.text = re.sub(pattern=sign, string=self.text, repl=toReplace)

    def revertUnwantedMarks(self):
        for result in self.findRelation.finditer(self.text):
            sign = result.group('relation')
            if '+' in sign or r'/' in sign:
                continue

            if ',' in sign:
                if self.reversionChecker.isMarkedAfterWordAndLanguage(result):
                    continue

                if self.reversionChecker.isMarkedAfterParenthesis(result):
                    continue

            # deals with 'and' and 'or' amd ','
            if self.reversionChecker.isMarkedWithinParenthesis(result) \
            or self.reversionChecker.isMarkedWithinApostrophe(result):
                self.prepareSignForReplacement(sign, result)

        self.revert()

    def prepareSignForReplacement(self, sign: str, result: Match):
        toReplace = f"|{sign}|"
        self.replaceOnResult(toReplace, result)

    def revert(self):
        self.text = self.text.replace("|", "")

    def hasMarks(self, text: str):
        return '[' in self.mark(text)

    def tokenize(self, text: str) -> list[str]:
        return re.split(r"\[|\]", self.mark(text))
