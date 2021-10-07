import re

from check_etymology_in_terminal import check, exhaustiveSearch
from raw_etymology_getter import RawEtymologyGetter

# check()
# print(RawEtymologyGetter().get('translate', 'english'))
exhaustiveSearch('turismo', 'spanish')

# doublet of verb and vrata
# CurrentWord.references[0].words.lang
# from Latin recipit) from Old French recete
#
# string = "{shortening } dkdkdk {borrowi-ng} asdf {}dsaf {blabla }"
# print(list(re.finditer(r"\{[\w'\- ]+\}", string)))