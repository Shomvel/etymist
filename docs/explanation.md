- 给定一个英语词
- 获取它在罗曼语言中的词形
    - translation?
- 获取词源
    - wiktionary Etymology
    
- refactor wiktionaryparser


French    format
New Latin formatus
New Latin formo


单独成句的compare放入原词里
提取references

The verb is derived from
根据词形分别提取

todos
√ note extractor
√ reference extractor
compoundParser 
√ think of extractor abstraction
test note extractor
test reference extractor

extractor + processor

写配置文件即可解析不同写法的词源

Refactor RelationExtractor

Procedure: 

Display
    alignment of fields  notes
less: vertical          transcription and meaning first
more: horizontal        everything

EtymologyParser:

splitter.split
moveNotes
moveReferences
relationExtractor.extract(), textLeft()
EtymologyPartParser.parse()
fillOmittedLang()


EtymologyPartParser:
1. 
ComplexWordParser or PlainWordParser

-> None -> PlainWordParser

3. ReferenceExtractor.extract(notes), textLeft()



ComplexWordParser:
Delimiter: + ;, [A-Z]
word delimiter: + ; /
relation: "and", "or"
lang

" + ", ", [A-Z]" -> ComplexWordParser
else -> wordParser  

ComplexWordParser:
split, wordParser.parse(), output

ComplexWord
Word1, Word2
lang
relation = ""

Relation : 
AndRelation: wordDelimiter, 
OrRelation
...

history

receipt as special case 
: note at front

Abstraction of Extractor
划定范围
提取

Etymology -> Graph



Latin contra (“against, opposite”) + Medieval Latin rotulus, Latin rotula (“roll, a little wheel”)


<- co- (intensive prefix) + operiō (“I close, cover”)

from  Old English discipul m (“disciple; scholar”) and discipula f (“female disciple”)

commūnis (“common, ordinary; of or for the community, public”) + -itās (ultimately from Proto-Indo-European *-teh₂ts (“suffix forming nouns indicating a state of being”))

com- + par (“equal”).

 From Middle English karette and Middle French carotte,

Compound of Spiel (“game”) +\u200e Zeug (“stuff”) or spielen (“to play”) +\u200e Zeug (“stuff”).\n

Blend of spoon +\u200e fork; originally a trademark'

 from a merger of Proto-Indo-European *n̥dʰér (“under”) and *n̥tér (“inside”).
 
Anglo-Norman memorie, Old French memoire etc

+ -> pass 
and 
or
, -> is preceded by ); is preceded by language name; is not inside a parenthesis 

and; or
+;, 

mark all signs
revert 
    - + -> pass
    - is preceded by )
    - is preceded by lang name, separated by one word
        - must be delicate
    - is inside parenthesis
split
    {and}/{or} first; then +,
hasSigns
    

levels
and/or
,/+

tokens
and/or/,/+/item

Choice: Part and/or Expression / Item
Part: Item ,/+ Item

parseChoice(i):
    result = Node = parsePart() 
    goNext()
    if b == and/or:
        b = parseChoice()
        result = 
        return ComplexWord(a, b, Relation(b))
    else:
    return a
        
parsePart():
    
Node: Relation; Left, Right 

Whole = Part (and/or Part ...)
Part = 

current = iter(tokens)


        
    


