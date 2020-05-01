from setuptools import setup, find_packages

setup(
    name='preprocess_corpora',
    version='0.1',
    packages=find_packages(),
    install_requires=['click', 'python-docx', 'treetagger-xml'],
    entry_points={
        'console_scripts': ['preprocess=preprocess_corpora.preprocessing.process:process_folder',
                            'align=preprocess_corpora.alignment.align:sentence_align'],
    },
)
