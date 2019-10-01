# preprocess-corpora
Python script to preprocess raw text. Requires Python 3.

## Usage

Run `python process.py` to process all unformatted .txt-files in a folder. 

Usage:

`process.py [OPTIONS] FOLDER_IN FOLDER_OUT [de|en|es|fr|it|nl|ru|ca|sv]`

Options:

- `--from_word` to use .docx-files as input, rather than .txt-files.
- `--tokenize` to tokenize the files (requires installation of Uplug (and language support in Uplug)).  

## Supported languages

- German (de)
- English (en)
- Spanish (es)
- French (fr)
- Italian (it)
- Dutch (nl)
- Russian (ru)
- Catalan (ca)
- Swedish (sv)
