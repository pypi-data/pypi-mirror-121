# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instrumentum', 'instrumentum.features', 'instrumentum.time_series']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'instrumentum',
    'version': '0.1.11',
    'description': '',
    'long_description': None,
    'author': 'federico',
    'author_email': 'federico.montanana@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
