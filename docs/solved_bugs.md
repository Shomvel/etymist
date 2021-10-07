starting from 20210912. Former bugs are not recorded

format: 
text:
query info: 
problem:
reason:
solution:

text: Cognate with Ancient Greek βαμβαίνω (bambaínō), βαμβαλύζω (bambalúzō, “I chatter with the teeth”), Russian болтать (boltatʹ, “to chatter, babble”)
problem: 
orig: Lat. balbus
problem: Ancient greek "," relation not parsed
reason: Reference Extractor used PlainWordParser to parse. 

--

text:
From Proto-Italic *doleō (“hurt, cause pain”), from Proto-Indo-European *dolh₁éyeti (“divide”)

orig: Sp. doler

problem: ", from" not split
reason: unknown


RawEtymology(text='From Middle English rouble, rubel, robel, robeil, from Anglo-Norman *robel (“bits of broken stone”). Presumably related to rubbish, originally of same meaning (bits of stone). Ultimately presumably from Proto-Germanic *reufaną (“to tear”), *raubōną (“to rob, steal, plunder”), perhaps via Old French robe (English rob (“steal”)) in sense of “plunder, destroy”; see also Middle English, Middle French -el.\n', word='rubble', lang='english')

problem:
- perhaps via 
- see also not split
- “plunder, destroy” got split

solution:
- add "perhaps via" to delimiter marker's source marker
- refactor reference get Text
- revert comma in apostrophes; possibly more pairedsymbols needs reversion

