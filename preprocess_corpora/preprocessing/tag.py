import click

from treetagger_xml.txt import process_single as process_txt
from treetagger_xml.xml import process_single as process_xml
from treetagger_xml.utils import instantiate_tagger

from ..core.constants import TREETAG_TXT, NO_TREETAG, TREETAGGER


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
        process_txt(tagger, language, file_in_txt, in_place=False, out_file=file_in_xml)
    else:
        click.echo('Tagging from xml...')
        process_xml(tagger, language, file_in_xml, in_place=True)
