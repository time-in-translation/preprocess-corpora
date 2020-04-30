# -*- coding: utf-8 -*-

import argparse
import os

from lxml import etree


def merge(files_in, file_out, delete_files_in=False):
    """
    Merges several alignment files (cesAlign format) into a single alignment file
    :param files_in: the input files
    :param file_out: the output file, with all alignments merged into one file
    :param delete_files_in: whether or not to delete the input files
    """
    root = etree.Element('cesAlign', attrib={'version': '1.0'})

    for file_in in files_in:
        parser = etree.XMLParser(remove_blank_text=True)
        in_tree = etree.parse(file_in, parser)

        for linkGrp in in_tree.xpath('//linkGrp'):
            root.set('fromDoc', linkGrp.get('fromDoc').split('/')[0])
            root.set('toDoc', linkGrp.get('toDoc').split('/')[0])
            root.append(linkGrp)

    tree = etree.ElementTree(root)
    tree.docinfo.public_id = '-//CES//DTD XML cesAlign//EN'
    tree.docinfo.system_url = 'dtd/xcesAlign.dtd'
    tree.write(file_out, pretty_print=True, xml_declaration=True, encoding='utf-8')

    if delete_files_in:
        for file_in in files_in:
            os.remove(file_in)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', nargs='+', help='Input files')
    parser.add_argument('file_out', help='Output file')
    parser.add_argument('--delete', action='store_true', help='Delete input files?')
    args = parser.parse_args()

    merge(args.file_in, args.file_out, args.delete)
