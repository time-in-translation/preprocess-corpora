# -*- coding: utf-8 -*-

import argparse
import codecs
import re


def normalize_apostrophes(line):
    """Converts single quotation marks to apostrophes if there's a lowercase letter behind it"""
    return re.sub(ur'\u2019(\w)', ur'\u0027\1', line)


def remove_soft_hyphens(line):
    """Removes any soft hyphens"""
    return line.replace(u'\u00AD', '')


def remove_double_spaces(line):
    """Removes superfluous spaces"""
    return re.sub(r'\s+', ' ', line).strip()


def fix_hyphenization(line):
    """Remove superfluous spaces in hyphenized words"""
    return re.sub(r'(\w)-\s(\w)', r'\1-\2', line)


def replace_quotes(language, line):
    """Replaces quote symbols with the ones suited for parsing"""
    if language == 'de':
        line = line.replace(u'\u00AB', '"')  # left-pointing double guillemet
        line = line.replace(u'\u00BB', '"')  # right-pointing double guillemet
        line = line.replace(u'\u2039', '\'')  # left-pointing single guillemet
        line = line.replace(u'\u203A', '\'')  # right-pointing single guillemet
    return line


def replace_common_errors(language, line):
    """Replaces some common errors that occurred during OCR"""
    if language == 'it':
        line = line.replace('E\'', u'È')
    return line


def process(file_in, file_out, language):
    lines = []
    with codecs.open(file_in, 'rb', 'utf-8') as f_in:
        for line in f_in:
            if line.strip():
                line = remove_double_spaces(line)
                line = remove_soft_hyphens(line)
                line = fix_hyphenization(line)
                line = replace_quotes(language, line)
                line = replace_common_errors(language, line)
                if language in ['en', 'nl', 'de']:
                    line = normalize_apostrophes(line)

                lines.append(line)

    with codecs.open(file_out, 'wb', 'utf-8') as f_out:
        for line in lines:
            f_out.write(line)
            f_out.write('\n')
            f_out.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    parser.add_argument('language', type=str, help='Language')
    args = parser.parse_args()

    process(args.file_in, args.file_out, args.language)
