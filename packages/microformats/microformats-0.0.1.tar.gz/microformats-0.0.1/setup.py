# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['microformats']
install_requires = \
['mf2py>=1.1.2,<2.0.0', 'mf2util>=0.5.1,<0.6.0', 'understory>=0.0.71,<0.0.72']

setup_kwargs = {
    'name': 'microformats',
    'version': '0.0.1',
    'description': 'A Microformats parser and utilities.',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'self@angelogladding.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
