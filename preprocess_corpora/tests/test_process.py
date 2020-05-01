import os
import unittest

from click.testing import CliRunner

from ..preprocessing.process import process_folder
from ..core.constants import ENGLISH, GERMAN, FRENCH, ITALIAN


class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def setUpFolders(self, language):
        data_dir = 'preprocess_corpora/tests/data'
        self.folder_in = os.path.join(os.getcwd(), data_dir, 'alice', language)
        self.folder_out = os.path.join(os.getcwd(), data_dir, 'alice-out', language)
        self.folder_cmp = os.path.join(os.getcwd(), data_dir, 'alice-cmp', language)

    def preprocess(self, language):
        self.setUpFolders(language)

        with self.runner.isolated_filesystem():
            os.makedirs(self.folder_out, exist_ok=True)

            result = self.runner.invoke(process_folder, [self.folder_in, self.folder_out, language])
            assert result.exit_code == 0

            with open(os.path.join(self.folder_out, '1.txt'), 'r') as tmp:
                with open(os.path.join(self.folder_cmp, '1.txt'), 'r') as cmp:
                    self.assertListEqual(tmp.readlines(), cmp.readlines())

    def test_preprocess(self):
        self.preprocess(ENGLISH)
        self.preprocess(GERMAN)
        self.preprocess(FRENCH)
        self.preprocess(ITALIAN)

    def tokenize(self, language):
        self.setUpFolders(language)

        with self.runner.isolated_filesystem():
            os.makedirs(self.folder_out, exist_ok=True)

            result = self.runner.invoke(process_folder, [self.folder_in, self.folder_out, language, '--tokenize'])
            assert result.exit_code == 0

            with open(os.path.join(self.folder_out, '1.xml'), 'r') as tmp:
                with open(os.path.join(self.folder_cmp, '1.tok'), 'r') as cmp:
                    self.assertListEqual(tmp.readlines(), cmp.readlines())

    def test_tokenize(self):
        self.tokenize(ENGLISH)
        self.tokenize(GERMAN)
        self.tokenize(FRENCH)
        self.tokenize(ITALIAN)

    def tag(self, language):
        self.setUpFolders(language)

        with self.runner.isolated_filesystem():
            os.makedirs(self.folder_out, exist_ok=True)

            result = self.runner.invoke(process_folder, [self.folder_in, self.folder_out, language, '--tag'])
            assert result.exit_code == 0

            with open(os.path.join(self.folder_out, '1.xml'), 'r') as tmp:
                with open(os.path.join(self.folder_cmp, '1.xml'), 'r') as cmp:
                    self.assertListEqual(tmp.readlines(), cmp.readlines())

    def test_tag(self):
        self.tag(ENGLISH)
        self.tag(GERMAN)
        self.tag(FRENCH)
        self.tag(ITALIAN)
