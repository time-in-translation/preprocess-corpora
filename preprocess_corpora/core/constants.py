# Germanic
GERMAN = 'de'
ENGLISH = 'en'
DUTCH = 'nl'
SWEDISH = 'sv'

# Romance
CATALAN = 'ca'
SPANISH = 'es'
FRENCH = 'fr'
ITALIAN = 'it'
PORTUGUESE = 'pt'

# Slavic
RUSSIAN = 'ru'

# Celtic
BRETON = 'br'

# Varieties
RIOPLATENSE = 'ar'
MEXICAN = 'mx'
VARIETIES = {RIOPLATENSE: SPANISH, MEXICAN: SPANISH}

LANGUAGES = [GERMAN, ENGLISH, SPANISH, FRENCH, ITALIAN, DUTCH, RUSSIAN, CATALAN, SWEDISH, PORTUGUESE, BRETON] \
            + list(VARIETIES.keys())

# No tokenization available
NO_TOK = [CATALAN, SWEDISH, BRETON]

# No TreeTagger available
NO_TREETAG = [SWEDISH, BRETON]
# TreeTagger directly on plain text
TREETAG_TXT = [CATALAN]
