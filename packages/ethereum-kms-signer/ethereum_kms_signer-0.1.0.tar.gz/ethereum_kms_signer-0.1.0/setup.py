# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ethereum_kms_signer', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.18.46,<2.0.0',
 'cytoolz>=0.11.0,<0.12.0',
 'ecdsa>=0.17.0,<0.18.0',
 'eth-account>=0.5.6,<0.6.0',
 'eth-keys>=0.3.3,<0.4.0',
 'eth-rlp>=0.2.1,<0.3.0',
 'eth-utils>=1.10.0,<2.0.0',
 'fire==0.4.0',
 'hexbytes>=0.2.2,<0.3.0',
 'livereload>=2.6.3,<3.0.0',
 'pyasn1>=0.4.8,<0.5.0',
 'pycryptodome>=3.10.1,<4.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['ethereum_kms_signer = ethereum_kms_signer.cli:main']}

setup_kwargs = {
    'name': 'ethereum-kms-signer',
    'version': '0.1.0',
    'description': 'Sign ETH transactions with keys stored in AWS KMS.',
    'long_description': '# Ethereum KMS Signer\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/ethereum_kms_signer">\n    <img src="https://img.shields.io/pypi/v/ethereum_kms_signer.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/meetmangukiya/ethereum_kms_signer/actions">\n    <img src="https://github.com/meetmangukiya/ethereum_kms_signer/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://ethereum-kms-signer.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/ethereum-kms-signer/badge/?version=latest" alt="Documentation Status">\n</a>\n\n</p>\n\n\nSign ETH transactions with keys stored in AWS KMS\n\n\n* Free software: MIT\n* Documentation: <https://ethereum-kms-signer.readthedocs.io>\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Meet Mangukiya',
    'author_email': 'meet@flamy.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/meetmangukiya/ethereum_kms_signer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
