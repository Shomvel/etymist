import re
from re import Pattern
from typing import Match, Union, Text

from base.relation_marker import RelationMarker
from splitter.splitting_reversion_checker import SplitterReversionChecker


class SplittingRelationMarker(RelationMarker):
    def __init__(self):
        super().__init__(SplitterReversionChecker())
        self.relation = r'''[\w"'\- ]+ {sign} '''
        self.INBRACKET = True
        self.signs = ['from', 'of']
        # whether punctuation marks are included in {} or not
        self.starts = {'^': not self.INBRACKET,
                       r'\) ': not self.INBRACKET,
                       r'\. ': not self.INBRACKET,
                       '; ': not self.INBRACKET,
                       ', ': self.INBRACKET}

    @property
    def text(self):
        return self._text.value

    @text.setter
    def text(self, value: str):
        self._text.value = value

    def finish(self):
        self.protectFromAroundSenseDevelopment()

    def markRelations(self):
        regexes = self.getRelationRegex()
        for regex, toReplace in regexes.items():
            self.text = re.sub(pattern=regex,
                               repl=toReplace,
                               string=self.text)

        self.markRelationWithParenthesis()

    def getRelationRegex(self) -> dict[str, str]:

        matchingPatterns = self.getMatchingPatterns()
        replacingPatterns = self.getReplacingPatterns(matchingPatterns)
        return dict(zip(matchingPatterns, replacingPatterns))

    def getReplacingPatterns(self, matchingPatterns: list[str]) -> dict[str, str]:
        replacingPatterns = []
        for matchingPattern in matchingPatterns:
            if 'start' in matchingPattern:
                replacingPatterns.append(r'\g<start>{\g<relation>}')
            else:
                replacingPatterns.append(r'{\g<relation>}')

        return replacingPatterns

    def getMatchingPatterns(self) -> list[str]:
        relations = []
        for start, isInBracket in self.starts.items():
            if isInBracket:
                relation = f'(?P<relation>{start}{self.relation})'
            else:
                relation = f'(?P<start>{start})(?P<relation>{self.relation})'

            for sign in self.signs:
                relations.append(relation.format(sign=sign))

        return relations

    def markRelationWithParenthesis(self):
        forReceipt = re.compile(r"(, \w+ \(.+\) from )")
        # altered (by influence of xx) from
        # why!
        # todo | add
        self.text = forReceipt.sub('{\1}', self.text)
        # word () from/of

    def revertUnwantedMarks(self):
        for relation in re.finditer(string=self.text, pattern=r'''\{(?P<relation>[\w",'\- ]+)\}'''):
            for shouldRevert in self.reversionChecker.getCheckers():
                if shouldRevert == self.reversionChecker.isMarkedSafeWords:
                    toReplace = f"|{self.replaceFromWithProtection(relation, 'relation')}|"
                else:
                    toReplace = f"|{relation.group('relation')}|"

                if shouldRevert(relation):
                    self.replaceOnResult(toReplace, relation)

        self.text = self.text.replace("|", "")

    @staticmethod
    def replaceFromWithProtection(result: Match, group: Union[str, int] = 0):
        return result.group(group).replace('from', '$rom')

    def protectFromAroundSenseDevelopment(self):
        for result in re.finditer("from", self.text):
            if self.reversionChecker.isMarkedSafeWords(result):
                toReplace = self.replaceFromWithProtection(result)
                self.replaceOnResult(toReplace, result)
