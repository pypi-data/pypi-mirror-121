# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['howdyho']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['howdyho = howdyho:while_true_print_howdyho_help']}

setup_kwargs = {
    'name': 'howdyho',
    'version': '3.0',
    'description': '',
    'long_description': None,
    'author': 'voronin9032',
    'author_email': 'voronin9032n3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
