# preprocess-corpora

This repository contains Python scripts to preprocess and sentence-align parallel (or monolingual) corpora. 
The repository originally heavily relied upon the software applications [Uplug](https://bitbucket.org/tiedemann/uplug/src/master/) and (in lesser respect) [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) to work.
Nowadays, we also have support for [NLTK](https://www.nltk.org/), [Spacy](https://spacy.io/), and [Stanza](https://stanfordnlp.github.io/stanza/).

## Installation

First, make sure to have installed [Uplug](https://bitbucket.org/tiedemann/uplug/src/master/) and [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/).
Users intending to use [NLTK](https://www.nltk.org/) and/or [Spacy](https://spacy.io/) and/or [Stanza](https://stanfordnlp.github.io/stanza/) can skip this step.

Then, create a [virtual environment](https://docs.python.org/3/library/venv.html) and activate it:

    $ python -m venv venv
    $ source venv/bin/activate

Then, install the requirements in this virtual environment via:

    $ pip install -r requirements.txt

Finally, create the executables `preprocess` and `align` via:    
 
    $ pip install --editable .

If you intend to use [NLTK](https://www.nltk.org/) for tokenization, be sure to download the [Punkt models](https://www.nltk.org/api/nltk.tokenize.html?highlight=punkt#module-nltk.tokenize.punkt):

    $ python
    >>> import nltk
    >>> nltk.download('punkt')

If you intend to use [Spacy](https://spacy.io/) for tokenization and tagging, be sure to download the language models (small models suffice, be sure to replace `en_core_web_sm` with the model for your language):

    $ python -m spacy download en_core_web_sm

With [Stanza](https://stanfordnlp.github.io/stanza/), models will be downloaded on-the-fly.

## Usage

### Preprocessing

The `preprocess` script allows preprocessing raw text and then to tokenize and tag the text in the [XML format used in OPUS](http://opus.nlpl.eu/).

Run `preprocess` to process all unformatted .txt-files in a folder. 

Usage:

    $ preprocess [OPTIONS] FOLDER_IN FOLDER_OUT {de|en|nl|sv|ca|es|fr|it|pt|ro|bg|pl|ru|br|hi|ar|mx}

Options:

- `--from_word` to use .docx-files as input, rather than .txt-files.
- `--tokenizer` to tokenize the files; choose either:
    - `uplug` (requires installation of Uplug (and language support in Uplug)).
    - `nltk` (requires installation of the Punkt models (and language support in Punkt))
    - `spacy` (requires installation of the Spacy models (and language support in Spacy))
    - `stanza` (requires installation of the Stanza models (and language support in Stanza))
    - `treetagger` (use the very naive tokenization in the *treetagger-xml* package (not recommended!))
- `--tag` to tag the files (requires installation of Spacy or TreeTagger (and language support))
- `--dialog` to detect dialogs in the generated .xml-files.


### Alignment

Run `align` to sentence-align .xml-files in a working directory. Requires installation of Uplug.

Usage:

    $ align [OPTIONS] WORKING_DIR [[de|en|nl|sv|ca|es|fr|it|pt|ro|bg|pl|ru|br|hi|ar|mx]]...

### Supported languages

| Genus      | Language   | ISO | Preprocessing | Tokenization | Tagging |
|------------|------------|-----|:-------------:|:------------:|:-------:|
| Germanic   | German     | de  |       ✔       |      ✔       |    ✔    |
| Germanic   | English    | en  |       ✔       |      ✔       |    ✔    |
| Germanic   | Dutch      | nl  |       ✔       |      ✔       |    ✔    |
| Germanic   | Swedish    | sv  |       ✔       |   ✔ (NLTK)   |    ✗    |
| Romance    | Catalan    | ca  |       ✔       |  ✔ (Stanza)  |    ✔    |
| Romance    | Spanish    | es  |       ✔       |      ✔       |    ✔    |
| Romance    | French     | fr  |       ✔       |      ✔       |    ✔    |
| Romance    | Italian    | it  |       ✔       |      ✔       |    ✔    |
| Romance    | Portuguese | pt  |       ✔       |  ✔ (Uplug)   |    ✔    |
| Romance    | Romanian   | ro  |       ✔       |  ✔ (Stanza)  |    ✔    |
| Hellenic   | Greek      | el  |       ✔       |  ✔ (Stanza)  |    ✔    |
| Slavic     | Belarusian | be  |       ✔       |  ✔ (Stanza)  |    ✔    |
| Slavic     | Bulgarian  | bg  |       ✔       |  ✔ (Stanza)  |    ✔    |
| Slavic     | Czech      | cs  |       ✔       |  ✔ (Stanza)  |    ✔    |
| Slavic     | Croatian   | hr  |       ✔       |  ✔ (Spacy)   |    ✔    |
| Slavic     | Lithuanian | lt  |       ✔       |  ✔ (Spacy)   |    ✔    |
| Slavic     | Latvian    | lv  |       ✔       |  ✔ (Stanza)  |    ✔    |
| Slavic     | Macedonian | mk  |       ✔       |  ✔ (Spacy)   |    ✔    |
| Slavic     | Polish     | pl  |       ✔       |  ✔ (Spacy)   |    ✔    |
| Slavic     | Russian    | ru  |       ✔       |  ✔ (Uplug)   |    ✔    |
| Slavic     | Slovak     | sk  |       ✔       |  ✔ (Stanza)  |    ✔    |
| Slavic     | Slovenian  | sl  |       ✔       |  ✔ (Stanza)  |    ✔    |
| Slavic     | Serbian    | sr  |       ✔       |  ✔ (Stanza)  |    ✗    |
| Slavic     | Ukrainian  | uk  |       ✔       |  ✔ (Spacy)   |    ✔    |
| Celtic     | Breton     | br  |       ✔       |      ✗       |    ✗    |
| Indo-Aryan | Hindi      | hi  |       ✔       |  ✔ (Stanza)  |    ✔    |

Some comments:
- For Dutch, for tokenization, Uplug can potentially use [Alpino](https://www.let.rug.nl/vannoord/alp/Alpino/) (recommended).
- For Swedish, consider using [Stagger](https://www.ling.su.se/english/nlp/tools/stagger) for part-of-speech tagging.
- Spanish varieties (Mexican Spanish (mx) and Rioplatense Spanish (ar)) are supported by referring to the Spanish parameters.
- Note that the Portuguese NLTK Punkt parameters are based upon Brazilian Portuguese.
- For Hindi, we use [RNNTagger](https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/) instead of TreeTagger.

## Tests

Run the tests via

    $ python -m unittest discover

In `preprocess_corpora/tests/data/alice`, you can find the example corpus used in the tests.
This corpus was compiled from Lewis Carroll's Alice in Wonderland and its translations into German, French, and Italian.
The source files are available through [Project Gutenberg](http://www.gutenberg.org/).
