# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zparser',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Dan Sikes',
    'author_email': 'dansikes7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
