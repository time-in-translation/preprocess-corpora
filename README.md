# preprocess-corpora

This repository contains scripts to preprocess and sentence-align (parallel) corpora.

## Usage

### Preprocessing

Python script to preprocess raw text and then to tokenize and tag the text in the [XML format used in OPUS](http://opus.nlpl.eu/). Requires Python 3.

Run `python process.py` to process all unformatted .txt-files in a folder. 

Usage:

`process.py [OPTIONS] FOLDER_IN FOLDER_OUT [de|en|es|fr|it|nl|ru|ca|sv|pt]`

Options:

- `--from_word` to use .docx-files as input, rather than .txt-files.
- `--tokenize` to tokenize the files (requires installation of Uplug (and language support in Uplug)).
- `--tag` to tag the files (requires installation of TreeTagger (and language support in TreeTagger))


### Alignment

Run `python align.py` to align .xml-files in a working directory. Requires installation of Uplug.

Usage:

`align.py [OPTIONS] WORKING_DIR [[de|en|es|fr|it|nl|ru|ca|sv|pt]]...`

### Supported languages

#### Full support
- German (de)
- English (en)
- Spanish (es)
- French (fr)
- Italian (it)
- Dutch (nl)
- Russian (ru)
- Portuguese (pt)

#### Limited support
- Catalan (ca) [not supported in Uplug/TreeTagger]
- Swedish (sv) [not supported in Uplug/TreeTagger]
