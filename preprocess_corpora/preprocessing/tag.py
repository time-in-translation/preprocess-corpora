import codecs
import os
import subprocess

import click

from treetagger_xml.txt import process_single as process_txt
from treetagger_xml.xml import process_single as process_xml
from treetagger_xml.utils import instantiate_tagger
from treetagger_xml.treetagger2opus import process as tag2xml

from ..core.constants import TREETAG_TXT, NO_TREETAG, TREETAGGER, HINDI

RNN_TAGGER = '../RNNTagger/'  # YMMV


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

    if language in TREETAG_TXT or tokenizer == TREETAGGER:
        click.echo('Tagging from text...')
        if language == HINDI:
            process_txt_hindi(language, file_in_txt, in_place=False, out_file=file_in_xml)
        else:
            tagger = instantiate_tagger(language)
            process_txt(tagger, language, file_in_txt, in_place=False, out_file=file_in_xml)
    else:
        click.echo('Tagging from xml...')
        tagger = instantiate_tagger(language)
        process_xml(tagger, language, file_in_xml, in_place=True)


def process_txt_hindi(language, in_file, in_place=False, out_file=None):
    result = subprocess.run(['cmd/rnn-tagger-hindi.sh', in_file], cwd=RNN_TAGGER, stdout=subprocess.PIPE)

    if in_place:
        tag_file = in_file
    else:
        tag_file = os.path.splitext(in_file)[0] + '.tag'

    with codecs.open(tag_file, 'w', encoding='utf-8') as g:
        g.write(result.stdout.decode('utf-8'))

    if not out_file:
        out_file = os.path.splitext(tag_file)[0] + '.xml'

    tag2xml(language, tag_file, out_file)
