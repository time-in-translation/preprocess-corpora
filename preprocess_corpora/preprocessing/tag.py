import codecs
import os

import click

from treetagger_xml.txt import process_single as process_txt
from treetagger_xml.xml import process_single as process_xml
from treetagger_xml.utils import instantiate_tagger
from treetagger_xml.treetagger2opus import process as tag2xml

from ..core.constants import TREETAG_TXT, NO_TREETAG, TREETAGGER, HINDI


def treetag_single(file_in_txt, file_in_xml, language, tokenizer):
    """
    Adds part-of-speech-tags and lemmatization to .xml-files (in-place)
    :param file_in_txt: the input txt file
    :param file_in_xml: the input xml file
    :param language: the current language
    :param tokenizer: the tokenizer being used
    """
    if language in NO_TREETAG:
        click.echo('TreeTagger not available for language {}'.format(language))
        return

    tagger = instantiate_tagger(language)

    if language in TREETAG_TXT or tokenizer == TREETAGGER:
        click.echo('Tagging from text...')
        if language == HINDI:
            process_txt_hindi(language, file_in_txt, in_place=False, out_file=file_in_xml)
        else:
            process_txt(tagger, language, file_in_txt, in_place=False, out_file=file_in_xml)
    else:
        click.echo('Tagging from xml...')
        process_xml(tagger, language, file_in_xml, in_place=True)


def process_txt_hindi(language, in_file, in_place=False, out_file=None):
    with codecs.open(in_file, 'r', encoding='utf-8') as f:
        lines = []
        for line in f:
            if line.strip():
                lines.append('\n'.join(tag_line(line)))

            lines.append('\n\n')

    if in_place:
        tag_file = in_file
    else:
        tag_file = os.path.splitext(in_file)[0] + '.tag'

    with codecs.open(tag_file, 'w', encoding='utf-8') as g:
        g.writelines(lines)

    if not out_file:
        out_file = os.path.splitext(tag_file)[0] + '.xml'

    tag2xml(language, tag_file, out_file)


def tag_line(line):
    # to be implemented
    pass
