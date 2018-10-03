# -*- coding: utf-8 -*-

import codecs
import glob
import os
import re

import click
from docx import Document

# Languages
GERMAN = 'de'
ENGLISH = 'en'
SPANISH = 'es'
FRENCH = 'fr'
ITALIAN = 'it'
DUTCH = 'nl'
LANGUAGES = [GERMAN, ENGLISH, SPANISH, FRENCH, ITALIAN, DUTCH]


def normalize_apostrophes(line):
    """Converts left single quotation marks to apostrophes if there's a lowercase letter behind it"""
    return re.sub(ur'\u2019(\w)', ur'\u0027\1', line)


def remove_soft_hyphens(line):
    """Removes any soft hyphens"""
    return line.replace(u'\u00AD', '')


def remove_double_spaces(line):
    """Removes superfluous spaces"""
    return re.sub(r'\s+', ' ', line).strip()


def fix_period_spacing(line):
    """Fixes spacing for periods"""
    return re.sub(r'(\w)\s?\.(\w)', r'\1. \2', line).strip()


def fix_hyphenization(language, line):
    """Remove superfluous spaces in hyphenized words"""
    line = re.sub(r'(\w)-\s(\w)', r'\1-\2', line)
    if language == DUTCH:
        line = line.replace('-en ', '- en ')  # -en should be converted back to - en
        line = line.replace('-of ', '- of ')  # -of should be converted back to - of
    if language == GERMAN:
        line = line.replace('-und ', '- und ')  # -und should be converted back to - und
        line = line.replace('-oder ', '- oder ')  # -oder should be converted back to - oder
    return line


def replace_quotes(language, line):
    """Replaces quote symbols with the ones suited for parsing"""
    if language == GERMAN:
        line = line.replace(u'\u00AB', '"')  # left-pointing double guillemet (replace with quotation mark)
        line = line.replace(u'\u00BB', '"')  # right-pointing double guillemet (replace with quotation mark)
        line = line.replace(u'\u2039', '\'')  # left-pointing single guillemet (replace with apostrophe)
        line = line.replace(u'\u203A', '\'')  # right-pointing single guillemet (replace with apostrophe)
        line = line.replace('<', '\'')  # less-than sign (replace with apostrophe)
        line = line.replace('>', '\'')  # greater-than sign (replace with apostrophe)
    if language in [DUTCH, FRENCH]:
        line = line.replace(u'\u2018', '\'')  # left single quotation mark (replace with apostrophe)
        line = line.replace(u'\u2019', '\'')  # left single quotation mark (replace with apostrophe)
    if language == DUTCH:
        line = line.replace(u'\'\'', '\'')  # double apostrophe (replace with single apostrophe)
        # apostrophe followed by a capital, dot, space or end of the line (replace with quotation mark)
        line = re.sub(r'\'([A-Z]|\.|\s|$)', r'"\1', line)
        line = re.sub(r'(,\s)\'', r'\1"', line)  # apostrophe preceded by a comma (replace with quotation mark)
        line = line.replace('"t ', '\'t ')  # "t should be converted back to 't
    return line


def replace_common_errors(language, line):
    """Replaces some common errors that occurred during OCR"""
    line = line.replace(u'—', '-')
    line = line.replace(u'…', '...')
    if language == ITALIAN:
        line = line.replace('E\'', u'È')
    return line


def process_file(file_in, file_out, language):
    lines = []
    with codecs.open(file_in, 'rb', 'utf-8') as f_in:
        for line in f_in:
            if line.strip():
                line = remove_double_spaces(line)
                line = remove_soft_hyphens(line)
                line = fix_period_spacing(line)
                line = fix_hyphenization(language, line)
                line = replace_quotes(language, line)
                line = replace_common_errors(language, line)
                if language in [ENGLISH, DUTCH, GERMAN]:
                    line = normalize_apostrophes(line)

                lines.append(line)

    with codecs.open(file_out, 'wb', 'utf-8') as f_out:
        for line in lines:
            f_out.write(line)
            f_out.write('\n')
            f_out.write('\n')


@click.command()
@click.argument('folder_in', type=click.Path(exists=True))
@click.argument('folder_out', type=click.Path(exists=True))
@click.argument('language', type=click.Choice(LANGUAGES))
@click.option('--from_word', is_flag=True)
def process_folder(folder_in, folder_out, language, from_word=False):
    if from_word:
        for file_in in glob.glob(os.path.join(folder_in, '*.docx')):
            document = Document(file_in)
            file_txt = os.path.splitext(file_in)[0] + '.txt'
            with codecs.open(file_txt, 'wb', 'utf-8') as f_out:
                full_text = []
                for paragraph in document.paragraphs:
                    full_text.append(paragraph.text)
                f_out.write('\n'.join(full_text))

    for file_in in glob.glob(os.path.join(folder_in, '*.txt')):
        file_out = os.path.join(folder_out, os.path.basename(file_in))
        process_file(file_in, file_out, language)


if __name__ == "__main__":
    process_folder()
