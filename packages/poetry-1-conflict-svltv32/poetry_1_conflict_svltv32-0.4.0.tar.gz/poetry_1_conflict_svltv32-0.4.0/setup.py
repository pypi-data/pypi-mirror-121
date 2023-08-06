# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_1_conflict_svltv32']

package_data = \
{'': ['*']}

install_requires = \
['poetry_2_conflict_svltv32']

setup_kwargs = {
    'name': 'poetry-1-conflict-svltv32',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'sdfasdf',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
