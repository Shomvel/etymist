from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from data_structures import Relation, ComplexWord
from parsers.plain_word_parser import PlainWordParser
from parsers.tokenizer import Tokenizer


@dataclass
class Node:
    relation: Relation
    left: Union[Node, str]
    right: Union[Node, str]


class WordParser:
    def __init__(self):
        self.wholeRelation = ['and', 'or', '/']
        self.partRelation = [',', '+']
        self.text = ""
        self.isNounCapitalized = False
        self.tokenizer = Tokenizer()
        self.plainWordParser = PlainWordParser()
        self.tokens = []
        self.i = 0
        self.it = None
        self.current = None
        self.next = None

    def isWord(self, item):
        return not (item in self.wholeRelation or item in self.partRelation)

    def parseWord(self):
        if self.isWord(self.current):
            return self.current
        else:
            return None

    def parsePart(self):
        a = self.parseWord()
        while True:
            if self.next in self.partRelation:
                relation = Relation(self.next)
                try:
                    self.goNext()
                except StopIteration:
                    return a
                b = self.parseWord()
                if not b:
                    return a

                a = Node(relation, a, b)
            elif not self.next:
                return a
            else:
                return a

    def parseWholeToTree(self):
        a = self.parsePart()
        while True:
            if self.next in self.wholeRelation:
                relation = Relation(self.next)
                try:
                    self.goNext()
                except StopIteration:
                    return a

                b = self.parsePart()
                a = Node(relation, a, b)
            elif not self.next:
                return a
            else:
                return a

    def evalBranch(self, branch: Union[Node, str]):
        if isinstance(branch, str):
            return self.plainWordParser.parse(branch)
        elif isinstance(branch, Node):
            return self.eval(branch)

    def eval(self, node: Node):
        left, right = self.evalBranch(node.left), self.evalBranch(node.right)
        return ComplexWord([left, right], node.relation)

    def parse(self, text: str) -> ComplexWord | None:
        self.text = text

        self.plainWordParser.isNounCapitalized = self.isNounCapitalized

        note = None
        if self.text.endswith("etc"):
            note = "possibly other sources"
        self.text = self.text.replace("etc", "")

        self.tokens = self.tokenizer.tokenize(self.text)
        if len(self.tokens) == 1:
            return self.plainWordParser.parse(self.text)

        self.it = iter(self.tokens)
        self.current = next(self.it)
        self.next = next(self.it)

        return self.eval(self.parseWholeToTree())

    def goNext(self):
        try:
            self.current = next(self.it)
            self.next = next(self.it)
        except StopIteration:
            self.next = None


# for testing parseWholeToTree
# parser.parse("a + b or c + d")
# parser.parse("a + b or c")
# parser.parse("a , b or c")
# parser.parse("a or b or c")
# parser.parse("a(), b(), c")
c = 2
