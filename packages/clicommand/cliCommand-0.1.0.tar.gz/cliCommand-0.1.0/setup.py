# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clicommand']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cliCommand = clicommand.cli:main']}

setup_kwargs = {
    'name': 'clicommand',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
