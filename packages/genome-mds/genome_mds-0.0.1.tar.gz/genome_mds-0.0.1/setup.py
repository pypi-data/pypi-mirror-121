#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['streamlit_bokeh_events>=0.1.2','streamlit==0.89.0','pandas','numpy','scikit-learn','biopython','bokeh==2.2.0','watchdog','ncbi-genome-download']

test_requirements = [ ]

setup(
    author="Koji Ishiya",
    author_email='koji.ishiya@aist.go.jp',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    description="Genome-MDS: A graphical two-dimensional comparison tool for prokaryotic genomes",
    entry_points={
        'console_scripts': [
            'genome-mds=genome_mds.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='genome_mds',
    name='genome_mds',
    packages=find_packages(include=['genome_mds', 'genome_mds.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/omics-tools/genome-mds',
    version='0.0.1',
    zip_safe=False,
)
