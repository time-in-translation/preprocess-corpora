import glob
import itertools
import os
import shutil
import subprocess

import click

from ..core.constants import LANGUAGES, VARIETIES
from .merge_alignments import merge


UPLUG_ALIGN = 'uplug align/hun -src {src} -trg {trg} -s {sl} -t {tl}'


def check_variety(language):
    result = language
    if language in VARIETIES:
        result = VARIETIES.get(language)
    return result


@click.command()
@click.argument('working_dir', type=click.Path(exists=True))
@click.argument('languages', nargs=-1, type=click.Choice(LANGUAGES))
def sentence_align(working_dir, languages):
    """
    Applies sentence alignment (using hunalign) to a corpus
    """
    os.chdir(working_dir)

    comb_ls = itertools.combinations(sorted(languages), 2)
    for sl, tl in comb_ls:
        for src in glob.glob(os.path.join(sl, '*.xml')):
            src_base = os.path.splitext(os.path.basename(src))[0]
            trg = os.path.join(tl, '{}.xml'.format(src_base))

            sl_align = check_variety(sl)
            tl_align = check_variety(tl)

            command = UPLUG_ALIGN.format(src=src, trg=trg, sl=sl_align, tl=tl_align)
            out_file = '{sl}-{tl}-{base}.xml'.format(sl=sl, tl=tl, base=src_base)
            with open(out_file, 'w') as out:
                subprocess.call(command, stdout=out, stderr=open(os.devnull, 'w'), shell=True)

        alignments = glob.glob('{sl}-{tl}-*.xml'.format(sl=sl, tl=tl))
        merged_file = '{sl}-{tl}.xml'.format(sl=sl, tl=tl)
        merge(alignments, merged_file, delete_files_in=True)

    # Remove artefacts created by hunalign
    shutil.rmtree(os.path.join(working_dir, 'data'))
    os.remove(os.path.join(working_dir, 'translate.txt'))


if __name__ == "__main__":
    sentence_align()
