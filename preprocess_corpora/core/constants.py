# Germanic
GERMAN = 'de'
ENGLISH = 'en'
DUTCH = 'nl'
SWEDISH = 'sv'
GERMANIC = [GERMAN, ENGLISH, DUTCH, SWEDISH]

# Romance
CATALAN = 'ca'
SPANISH = 'es'
FRENCH = 'fr'
ITALIAN = 'it'
PORTUGUESE = 'pt'
ROMANCE = [CATALAN, SPANISH, FRENCH, ITALIAN, PORTUGUESE]

# Slavic
BULGARIAN = 'bg'
RUSSIAN = 'ru'
SLAVIC = [BULGARIAN, RUSSIAN]

# Celtic
BRETON = 'br'
CELTIC = [BRETON]

# Varieties
RIOPLATENSE = 'ar'
MEXICAN = 'mx'
VARIETIES = {RIOPLATENSE: SPANISH, MEXICAN: SPANISH}

LANGUAGES = GERMANIC + ROMANCE + SLAVIC + CELTIC + list(VARIETIES.keys())

# No tokenization available
NO_TOK = [BULGARIAN, CATALAN, SWEDISH, BRETON]

# No TreeTagger available
NO_TREETAG = [SWEDISH, BRETON]
# TreeTagger directly on plain text
TREETAG_TXT = [BULGARIAN, CATALAN]
