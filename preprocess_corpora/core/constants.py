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
POLISH = 'pl'
RUSSIAN = 'ru'
SLAVIC = [BULGARIAN, POLISH, RUSSIAN]

# Celtic
BRETON = 'br'
CELTIC = [BRETON]

# Varieties
RIOPLATENSE = 'ar'
MEXICAN = 'mx'
VARIETIES = {RIOPLATENSE: SPANISH, MEXICAN: SPANISH}

LANGUAGES = GERMANIC + ROMANCE + SLAVIC + CELTIC + list(VARIETIES.keys())

# No TreeTagger available
NO_TREETAG = [SWEDISH, BRETON]
# TreeTagger directly on plain text
TREETAG_TXT = [BULGARIAN, CATALAN]

# Available tokenization models in NLTK (through punkt)
NLTK_LANGUAGES = {
    GERMAN: 'german',
    ENGLISH: 'english',
    DUTCH: 'dutch',
    SWEDISH: 'swedish',
    SPANISH: 'spanish',
    FRENCH: 'french',
    ITALIAN: 'italian',
    PORTUGUESE: 'portuguese',
}

# Tokenizers
NLTK = 'nltk'
TREETAGGER = 'treetagger'
UPLUG = 'uplug'
