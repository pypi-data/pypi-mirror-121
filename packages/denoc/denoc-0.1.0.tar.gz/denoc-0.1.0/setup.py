# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['denoc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'denoc',
    'version': '0.1.0',
    'description': 'Utilities for compile JavaScript with Deno',
    'long_description': None,
    'author': 'Eliaz Bobadilla',
    'author_email': 'eliaz.bobadilladev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
