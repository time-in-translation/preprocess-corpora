import setuptools


def readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
    name='preprocess-corpora',
    version='0.1.1',
    author='Martijn van der Klis',
    author_email='m.h.vanderklis@uu.nl',
    description='Preprocessing and sentence-aligning for parallel corpora',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Topic :: Text Processing :: Linguistic',
    ],
    url='https://github.com/time-in-translation/preprocess-corpora',
    license='MIT',
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'click',
        'python-docx',
        'treetagger-xml'],
    entry_points={
        'console_scripts': ['preprocess=preprocess_corpora.preprocessing.process:process_folder',
                            'align=preprocess_corpora.alignment.align:sentence_align'],
    },
)
