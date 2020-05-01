import os
import shlex
import subprocess


# Uplug tokenize command
UPLUG_TOKENIZE = 'uplug -f pre/basic pre/{language}/basic -in {file_in} > {file_xml}'


def tokenize_single(file_in, file_out, language):
    command = UPLUG_TOKENIZE.format(language=language,
                                    file_in=shlex.quote(file_in),
                                    file_xml=shlex.quote(file_out))
    subprocess.call(command, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
