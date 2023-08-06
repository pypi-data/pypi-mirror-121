# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dictionarysnek']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'dictionarysnek',
    'version': '0.0.2',
    'description': 'A Dictionary API Wrapper for Python',
    'long_description': '<h1>dictionarysnek</h1>\n\n## Table of contents\n* [General info](#general-info)\n* [Dependencies](#dependencies)\n* [Setup](#setup)\n* [Usage](#usage)\n\n## General info\nA Dictionary API Wrapper for Python.\n\t\n## Dependencies\nProject is created with:\n* Requests Version: 2.26.0\n* Dictionary API: dictionaryapi.dev\n\t\n## Setup\nPython-pip:\n```\n$ pip install dictionarysnek\n```\nPoetry:\n```\n$poetry add dictionarysnek\n```\n\n## Usage\n* Import the module: ```from dictionarysnek import dictionarysnek```\n* Get the data: ```data = dictionarysnek.getdata("mundane")```\n* Pass it to the desired function to get the output: ```synonyms = dictionarysnek.getsyn(data)```\n\n## Functions\n* Get Synonyms -> Returns an array of Synonyms -> ```dictionarysnek.getsyn(json: list)```\n* Get Antonyms -> Returns an array of Antonyms -> ```dictionarysnek.getant(json: list)```\n* Get Definition -> Returns the definition of the given word -> ```dictionarysnek.getdefi(json: list)```\n* Get Word -> Returns the given word -> ```dictionarysnek.getword(json: list)```\n* Get Phonetic -> Returns the phonetic of the given word -> ```dictionarysnek.getphonetic(json: list)```\n* Get Part of Speech -> Returns the Part of Speech of the given word -> ```dictionarysnek.getpos(json: list)```\n* Get Example -> Gives an usage of the given word -> ```dictionarysnek.getex(json: list)```\n* Get Origin -> Gives information about the origin of the given word -> ```dictionarysnek.getorigin(json: list)```\n',
    'author': 'Nessundorma',
    'author_email': 'vismdbs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gizems-Cult/dictionarysnek',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
