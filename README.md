# preprocess-corpora

Python script to preprocess raw text and then to tokenize and tag the text in the [XML format used in OPUS](http://opus.nlpl.eu/). Requires Python 3.

## Usage

Run `python process.py` to process all unformatted .txt-files in a folder. 

Usage:

`process.py [OPTIONS] FOLDER_IN FOLDER_OUT [de|en|es|fr|it|nl|ru|ca|sv]`

Options:

- `--from_word` to use .docx-files as input, rather than .txt-files.
- `--tokenize` to tokenize the files (requires installation of Uplug (and language support in Uplug)).
- `--tag` to tag the files (requires installation of TreeTagger (and language support in TreeTagger))

## Supported languages

### Full support
- German (de)
- English (en)
- Spanish (es)
- French (fr)
- Italian (it)
- Dutch (nl)
- Russian (ru)

### Limited support
- Catalan (ca) [not supported in Uplug/TreeTagger]
- Swedish (sv) [not supported in Uplug/TreeTagger]
