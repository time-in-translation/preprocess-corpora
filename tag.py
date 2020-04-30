from treetagger_xml.xml import process_single
from treetagger_xml.utils import instantiate_tagger


def treetag_single(file_in, language):
    """
    Adds part-of-speech-tags and lemmatization to .xml-files (in-place)
    :param file_in: the input file
    :param language: the current language
    """
    tagger = instantiate_tagger(language)
    process_single(tagger, language, file_in, in_place=True)
