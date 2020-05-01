# -*- coding: utf-8 -*-

import glob
import os

import click

from ..core.constants import LANGUAGES, VARIETIES
from .preprocess import preprocess_single, word2txt
from .tag import treetag_single
from .tok import tokenize_single


@click.command()
@click.argument('folder_in', type=click.Path(exists=True))
@click.argument('folder_out', type=click.Path(exists=True))
@click.argument('language', type=click.Choice(LANGUAGES))
@click.option('--from_word', is_flag=True)
@click.option('--tokenize', is_flag=True)
@click.option('--tag', is_flag=True)
def process_folder(folder_in, folder_out, language, from_word=False, tokenize=False, tag=False):
    if from_word:
        word2txt(folder_in)

    if tag:
        tokenize = True

    if language in VARIETIES:
        language = VARIETIES.get(language)

    for file_in in glob.glob(os.path.join(folder_in, '*.txt')):
        file_out = os.path.join(folder_out, os.path.basename(file_in))
        preprocess_single(file_in, file_out, language)

        if tokenize:
            file_xml = os.path.join(folder_out, os.path.splitext(os.path.basename(file_out))[0] + '.xml')
            tokenize_single(file_out, file_xml, language)

            if tag:
                treetag_single(file_xml, language)


if __name__ == "__main__":
    process_folder()
