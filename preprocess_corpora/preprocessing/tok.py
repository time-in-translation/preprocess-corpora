import os
import shlex
import subprocess

import click
from lxml import etree
from nltk.tokenize import sent_tokenize, word_tokenize

from ..core.constants import UPLUG, NLTK, TREETAGGER, NLTK_LANGUAGES


def tokenize_single(file_in, file_out, language, tokenizer):
    """
    Tokenizes (on sentence- and word-level) the input file.
    :param file_in: the input file
    :param file_out: the output file
    :param language: the current language
    :param tokenizer: the tokenizer being used
    """
    if tokenizer == UPLUG:
        click.echo('Using Uplug tokenization')
        uplug_tokenize(file_in, file_out, language)
    elif tokenizer == NLTK:
        click.echo('Using NLTK tokenization')
        nltk_tokenize(file_in, file_out, language)
    elif tokenizer == TREETAGGER:
        # Use TreeTagger without tokenization, based on the preprocessed .txt-files
        click.echo('Using TreeTagger tokenization')


def uplug_tokenize(file_in, file_out, language):
    # Run Uplug with a fallback to the general module
    command = 'uplug -f pre/basic pre/{language}/basic -in {file_in} > {file_xml}'
    command = command.format(language=language,
                             file_in=shlex.quote(file_in),
                             file_xml=shlex.quote(file_out))
    subprocess.call(command, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)


def nltk_tokenize(file_in, file_out, language):
    punkt_language = NLTK_LANGUAGES.get(language)
    if not punkt_language:
        raise click.ClickException('Tokenization in NLTK not available for language {}'.format(language))

    # Create counters for paragraphs and sentences
    i = j = 1

    # Start a text element and add a first paragraph
    text = etree.Element('text')
    paragraph = etree.SubElement(text, 'p')
    paragraph.set('id', str(i))

    with open(file_in, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                sentences = sent_tokenize(line, language=punkt_language)
                for s in sentences:
                    sentence = etree.SubElement(paragraph, 's')
                    sentence.set('id', 's{}.{}'.format(i, j))
                    words = word_tokenize(s, language=punkt_language)
                    for k, w in enumerate(words, start=1):
                        word = etree.SubElement(sentence, 'w')
                        word.set('id', 'w{}.{}.{}'.format(i, j, k))
                        word.text = w
                j += 1
            else:
                i += 1
                paragraph = etree.SubElement(text, 'p')
                paragraph.set('id', str(i))
                j = 1

    tree = etree.ElementTree(text)
    tree.write(file_out, pretty_print=True, xml_declaration=True, encoding='utf-8')
