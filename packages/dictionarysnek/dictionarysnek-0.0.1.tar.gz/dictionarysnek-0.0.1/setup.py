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
    'version': '0.0.1',
    'description': 'A Dictionary API Wrapper for Python',
    'long_description': None,
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
