"""
TODO:

- Spanish questions/exclamations
- Dash vs. hyphen detection doesn't work in XML

"""

import sys
from operator import itemgetter
import optparse

import lxml.etree

QUOTE_STYLES = {
    'ascii-double': ('"', '"'),
    'ascii-single': ("'", "'"),
    'unicode-double': ('“', '”'),
    'unicode-hebrew': ('״', '״'),
    'unicode-single': ('‘', '’'),
    'angle': ('«', '»'),
    'angle-reverse': ('»', '«'),
    'dash': ('-', '-'),
    'double-dash': ('--', '--'),
}

ALTERNATES = {
    'ascii-double': 'unicode-double',
    'ascii-single': 'unicode-single',
    'unicode-single': 'ascii-single',
    'unicode-double': 'ascii-double'
    }


def read_text(filename):
    """reads text out of xml file, disregarding structure"""
    assert filename.endswith('.xml')
    tree = lxml.etree.parse(filename)

    # concatenate all words by iteration
    words = []
    for node in tree.iter():
        if node.tag == 'w':
            words.append(node.text)

    return ' '.join(words)


def read_xml(filename):
    assert filename.endswith('.xml')
    tree = lxml.etree.parse(filename)
    return tree


def paragraphs(tree):
    paragraphs = tree.getroot().getchildren()
    return paragraphs


def tag_dialog(paragraph, quotation_style, use_alternates=False):
    in_dialog = False  # current state of loop
    dialog = False  # have we found any dialog fragment in paragraph

    # stores all the nodes that belong to the current dialogfragment
    dialog_nodes = []

    # if we find a balance mismatch, mark the paragraph
    balanced = True

    # string buffer used for printing
    out = ''

    # helper methods
    def open_dialog():
        nonlocal dialog, in_dialog, out
        dialog = True
        in_dialog = True
        out += '[['

    def close_dialog(_balanced=True):
        nonlocal balanced, in_dialog
        nonlocal out, dialog_nodes

        in_dialog = False
        if not _balanced:
            balanced = False
            out += '}}'

            # update all nodes of current fragment to reflect uncertainty
            for node in dialog_nodes:
                node.attrib['dialog'] = '0.5'
        else:
            out += ']]'

        dialog_nodes = []

    delimiters = QUOTE_STYLES[quotation_style]
    left, right = delimiters

    # similar delimiters that might be wrongly entered
    left_alt, right_alt = None, None
    if use_alternates and quotation_style in ALTERNATES:
        left_alt, right_alt = QUOTE_STYLES[ALTERNATES[quotation_style]]

    symmetric = left == right

    for sentence in paragraph:
        for i in range(len(sentence)):
            node = sentence[i]
            word = node.text

            # mark tree node with dialog prediction
            if in_dialog:
                node.attrib['dialog'] = '1.0'
                dialog_nodes.append(node)
            else:
                node.attrib['dialog'] = '0.0'

            if symmetric:
                if word == left_alt or word == right_alt:
                    word = left

                if word == left:
                    if in_dialog:
                        close_dialog()
                    else:
                        node.attrib['dialog'] = '1.0'
                        dialog_nodes.append(node)
                        open_dialog()

                else:
                    out += word

            else:  # non symmetric
                if word == left or (word == left_alt and not in_dialog):
                    if in_dialog:
                        # as we are already in a dialog,
                        # better close and reopen
                        close_dialog(False)
                    node.attrib['dialog'] = '1.0'
                    dialog_nodes.append(node)
                    open_dialog()

                elif word == right or (word == right_alt and in_dialog):
                    if in_dialog:
                        close_dialog()

                else:
                    out += word

            out += ' '

    if in_dialog:
        # done processing but still in dialog
        # however, this is expected with dash quotation style
        if quotation_style == 'dash':
            close_dialog()
        else:
            close_dialog(False)

    return out, dialog, balanced


def print_red(*args):
    print('\033[91m', *args, '\033[0m')


def print_yellow(*args):
    print('\033[93m', *args, '\033[0m')


def process_file(filename, print_all=False, write=False, use_alternates=False):
    found = False

    print('File:', filename)

    dialog_per_style = {}
    unbalanced_per_style = {}
    tree = read_xml(filename)

    for style in QUOTE_STYLES.keys():
        processed = [tag_dialog(p, style, use_alternates)
                     for p in paragraphs(tree)]

        has_dialog = [p for p in processed if p[1]]
        unbalanced = [p for p in processed if not p[2]]

        ratio = 0
        if len(processed):
            ratio = len(has_dialog)/len(processed)

        unbalanced_ratio = 0
        if len(has_dialog):
            unbalanced_ratio = len(unbalanced)/len(has_dialog)

        dialog_per_style[style] = ratio
        unbalanced_per_style[style] = unbalanced_ratio

    sorted_by_dialog = sorted(dialog_per_style.items(),
                              key=itemgetter(1), reverse=True)

    for style, ratio in sorted_by_dialog:
        # this uses some hardcoded heuristics for now
        if ratio > 0.9 or ratio < 0.1:
            # too few or too many dialog fragments
            continue
        if unbalanced_per_style[style] > 0.3:
            # probably wrong choice
            continue

        processed = [tag_dialog(p, style, use_alternates)
                     for p in paragraphs(tree)]

        has_dialog = [p for p in processed if p[1]]
        balanced = [p for p in processed if p[2]]
        found = True
        print('Quotation style is probably:', style)
        print('Paragraphs:', len(processed))
        print('With Dialog:', len(has_dialog))
        print('Ratio: %.2f' % ratio)
        print('Unbalanced:', len([p for p in processed if not p[2]]))
        print()

        if print_all:
            for p, dialog, balanced in processed:
                if not balanced:
                    print_red(p)
                elif dialog:
                    print_yellow(p)
                else:
                    print(p)
                print()

        if write:
            out_filename = filename.replace('.xml', '.dialog.xml')
            tree.write(open(out_filename, 'wb'), encoding='utf-8', pretty_print=True, xml_declaration=True)
            print('Saved to: %s' % out_filename)

        break

    if not found:
        print('Could not detect quotation style')


def main():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--print", action='store_true', dest="print_all", default=False)
    parser.add_option("-w", "--write", action='store_true', dest="write", default=False)
    parser.add_option("-a", "--use_alternates", action='store_true', dest="use_alternates", default=False)

    options, args = parser.parse_args()

    for filename in args:
        process_file(filename, options.print_all, options.write, options.use_alternates)


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        print('Please run using Python 3!')
    else:
        main()
