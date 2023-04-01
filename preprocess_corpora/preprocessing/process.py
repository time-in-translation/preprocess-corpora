# -*- coding: utf-8 -*-

import glob
import os

import click

from ..core.constants import LANGUAGES, VARIETIES, UPLUG, NLTK, SPACY, STANZA, TREETAGGER
from .preprocess import preprocess_single, word2txt
from .tag import treetag_single
from .tok import tokenize_single
from .dialog import process_file as detect_dialog


@click.command()
@click.argument('folder_in', type=click.Path(exists=True))
@click.argument('folder_out', type=click.Path(exists=True))
@click.argument('language', type=click.Choice(LANGUAGES))
@click.option('--from_word', is_flag=True)
@click.option('--tokenizer', type=click.Choice([UPLUG, NLTK, SPACY, STANZA, TREETAGGER]))
@click.option('--tag', is_flag=True)
@click.option('--dialog', is_flag=True)
def process_folder(folder_in, folder_out, language, from_word=False, tokenizer=UPLUG, tag=False, dialog=False):
    if from_word:
        word2txt(folder_in)

    if tag and not tokenizer:
        raise click.ClickException('Please supply a tokenizer')

    if language in VARIETIES:
        language = VARIETIES.get(language)

    for file_in in glob.glob(os.path.join(folder_in, '*.txt')):
        file_out = os.path.join(folder_out, os.path.basename(file_in))
        preprocess_single(file_in, file_out, language)

        file_xml = os.path.join(folder_out, os.path.splitext(os.path.basename(file_out))[0] + '.xml')
        if tokenizer:
            tokenize_single(file_out, file_xml, language, tokenizer)

            if tag:
                # For Spacy and Stanza, tagging is done during tokenization, so no need to tag again! :-)
                if tokenizer in [SPACY, STANZA]:
                    pass
                else:
                    treetag_single(file_out, file_xml, language, tokenizer)

            if dialog:
                detect_dialog(file_xml, write=True)


if __name__ == "__main__":
    process_folder()
