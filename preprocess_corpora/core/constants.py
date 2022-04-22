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
ROMANIAN = 'ro'
ROMANCE = [CATALAN, SPANISH, FRENCH, ITALIAN, PORTUGUESE, ROMANIAN]

# Slavic
BULGARIAN = 'bg'
POLISH = 'pl'
RUSSIAN = 'ru'
SLAVIC = [BULGARIAN, POLISH, RUSSIAN]

# Celtic
BRETON = 'br'
CELTIC = [BRETON]

# Indo Arayan
HINDI = 'hi'
INDO_ARYAN = [HINDI]

# Varieties
RIOPLATENSE = 'ar'
MEXICAN = 'mx'
VARIETIES = {RIOPLATENSE: SPANISH, MEXICAN: SPANISH}

LANGUAGES = GERMANIC + ROMANCE + SLAVIC + CELTIC + INDO_ARYAN + list(VARIETIES.keys())

# No TreeTagger available
NO_TREETAG = [SWEDISH, BRETON]
# TreeTagger directly on plain text
TREETAG_TXT = [BULGARIAN, CATALAN, ROMANIAN]

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

# Available models in Spacy
SPACY_MODELS = {
    GERMAN: 'de_core_news_sm',
    ENGLISH: 'en_core_web_sm',
    DUTCH: 'nl_core_news_sm',
    CATALAN: 'ca_core_news_sm',
    SPANISH: 'es_core_news_sm',
    FRENCH: 'fr_core_news_sm',
    ITALIAN: 'it_core_news_sm',
    PORTUGUESE: 'pt_core_news_sm',
    ROMANIAN: 'ro_core_news_sm',
    POLISH: 'pl_core_news_sm',
    RUSSIAN: 'ru_core_news_sm',
}

# Tokenizers and taggers
NLTK = 'nltk'
SPACY = 'spacy'
TREETAGGER = 'treetagger'
UPLUG = 'uplug'
