import codecs
import glob
import os
import re

from docx import Document

from ..core.constants import GERMAN, ENGLISH, FRENCH, ITALIAN, DUTCH, RUSSIAN, CATALAN, SWEDISH


def normalize_apostrophes(line):
    """Converts left single quotation marks to apostrophes if there's a lowercase letter behind it"""
    return re.sub(r'\u2019(\w)', r"'\1", line)


def remove_soft_hyphens(line):
    """Removes any soft hyphens or middle dots"""
    line = line.replace(u'\u00AC', '')  # not sign (Word's soft hyphen)
    line = line.replace(u'\u00AD', '')  # soft hyphen
    line = line.replace(u'\u00B7', '')  # middle dot
    return line


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
    if language in [GERMAN, CATALAN]:
        line = line.replace(u'\u00AB', '"')  # left-pointing double guillemet (replace with quotation mark)
        line = line.replace(u'\u00BB', '"')  # right-pointing double guillemet (replace with quotation mark)
        line = line.replace(u'\u2039', '\'')  # left-pointing single guillemet (replace with apostrophe)
        line = line.replace(u'\u203A', '\'')  # right-pointing single guillemet (replace with apostrophe)
        line = line.replace('<', '\'')  # less-than sign (replace with apostrophe)
        line = line.replace('>', '\'')  # greater-than sign (replace with apostrophe)
    if language in [DUTCH, FRENCH, CATALAN, SWEDISH]:
        line = line.replace(u'\u201C', '"')  # left double quotation mark (replace with quotation mark)
        line = line.replace(u'\u201D', '"')  # right double quotation mark (replace with quotation mark)
        line = line.replace(u'\u2018', '\'')  # left single quotation mark (replace with apostrophe)
        line = line.replace(u'\u2019', '\'')  # right single quotation mark (replace with apostrophe)
    if language == FRENCH:
        line = re.sub(r'\s\'', '\'', line)  # Remove superfluous spacing before apostrophes
    if language == DUTCH:
        line = line.replace(u'\'\'', '\'')  # double apostrophe (replace with single apostrophe)
        # apostrophe followed by a capital, dot, space or end of the line (replace with quotation mark)
        line = re.sub(r'\'([A-Z]|\.|\s|$)', r'"\1', line)
        line = re.sub(r'(,\s)\'', r'\1"', line)  # apostrophe preceded by a comma (replace with quotation mark)
        line = line.replace('"t ', '\'t ')  # "t should be converted back to 't
    if language == RUSSIAN:
        line = line.replace('""', '"')  # Replace double quotation marks by a single one
        line = re.sub(r'(^|\.\s?)-\s?', r'\1', line)  # Remove hyphens at the start of the line or after punctuation
        line = re.sub(r'([.,?!])\s(\"(?:\s|$))', r'\1\2', line)  # Remove spaces between punctuation and quotation mark
        line = re.sub(r'([.,?!])\s?(\")-', r'\1\2 -', line)  # Switch (or create) spacing between quotation and hyphens
        line = re.sub(r'(^\")\s', r'\1', line)  # Replace superfluous spaces at the start of the line
    if language == CATALAN:
        line = re.sub(r'"\.', '."', line)  # Move dots after quotation marks
    return line


def replace_common_errors(language, line):
    """Replaces some common errors that occurred during OCR"""
    # Replace unicode dashes to hyphen-minus
    line = re.sub(r'\s?\u2012\s?', ' - ', line)  # figure dash
    line = re.sub(r'\s?\u2013\s?', ' - ', line)  # en dash
    line = re.sub(r'\s?\u2014\s?', ' - ', line)  # em dash

    line = line.replace(u'，', ', ')  # u2063, invisible separator
    line = line.replace(u'：', ':')  # uFF1A, fullwidth colon
    line = line.replace(u'…', '...')  # ellipsis
    if language == ITALIAN:
        line = line.replace('E\'', u'È')
        line = line.replace('Be\'', u'Bè')
        line = line.replace('be\'', u'bè')
        line = line.replace('po\'', u'pò')
    return line


def preprocess_single(file_in, file_out, language):
    lines = []
    with codecs.open(file_in, 'r', 'utf-8') as f_in:
        for line in f_in:
            if line.strip():
                line = remove_double_spaces(line)
                line = remove_soft_hyphens(line)
                line = replace_common_errors(language, line)
                line = fix_period_spacing(line)
                line = fix_hyphenization(language, line)
                line = replace_quotes(language, line)
                if language in [ENGLISH, DUTCH, GERMAN]:
                    line = normalize_apostrophes(line)

                lines.append(line)

    with codecs.open(file_out, 'w', 'utf-8') as f_out:
        for line in lines:
            f_out.write(line)
            f_out.write('\n')
            f_out.write('\n')


def word2txt(folder_in):
    for file_in in glob.glob(os.path.join(folder_in, '*.docx')):
        document = Document(file_in)
        file_txt = os.path.splitext(file_in)[0] + '.txt'
        with codecs.open(file_txt, 'w', 'utf-8') as f_out:
            full_text = []
            for paragraph in document.paragraphs:
                full_text.append(paragraph.text)
            f_out.write('\n'.join(full_text))
