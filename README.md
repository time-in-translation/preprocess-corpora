# preprocess-corpora

This repository contains Python scripts to preprocess and sentence-align parallel (or monolingual) corpora. 
The repository heavily relies upon [Uplug](https://bitbucket.org/tiedemann/uplug/src/master/) and (in lesser respect) [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) to work. 

## Installation

First, make sure to have installed [Uplug](https://bitbucket.org/tiedemann/uplug/src/master/) and [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/).

Then, install the requirements via:

    $ pip install -r requirements.txt

Finally, create the executables `preprocess` and `align` via:    
 
    $ pip install --editable .

## Usage

### Preprocessing

The `preprocess` script allows to preprocess raw text and then to tokenize and tag the text in the [XML format used in OPUS](http://opus.nlpl.eu/).

Run `preprocess` to process all unformatted .txt-files in a folder. 

Usage:

`process [OPTIONS] FOLDER_IN FOLDER_OUT [de|en|es|fr|it|nl|ru|ca|sv|pt]`

Options:

- `--from_word` to use .docx-files as input, rather than .txt-files.
- `--tokenize` to tokenize the files (requires installation of Uplug (and language support in Uplug)).
- `--tag` to tag the files (requires installation of TreeTagger (and language support in TreeTagger))


### Alignment

Run `align` to sentence-align .xml-files in a working directory. Requires installation of Uplug.

Usage:

`align [OPTIONS] WORKING_DIR [[de|en|es|fr|it|nl|ru|ca|sv|pt]]...`

### Supported languages

#### Full support
- German (de)
- English (en)
- Spanish (es) (+ variants Rioplatense (ar) and Mexican (mx) Spanish)
- French (fr)
- Italian (it)
- Dutch (nl)
- Russian (ru)
- Portuguese (pt)

#### Limited support
- Breton (br) [not supported in Uplug/TreeTagger]
- Catalan (ca) [not supported in Uplug/TreeTagger]
- Swedish (sv) [not supported in Uplug/TreeTagger]

## Tests

Run the tests via

`python -m unittest discover`

In `preprocess_corpora/tests/data/alice`, you can find the example corpus used in the tests.
This corpus was compiled from Lewis Carroll's Alice in Wonderland and its translations into German, French, and Italian.
The source files are available through [Project Gutenberg](http://www.gutenberg.org/).
