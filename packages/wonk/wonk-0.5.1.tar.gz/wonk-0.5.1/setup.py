# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wonk']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'boto3>=1.17.25,<2.0.0',
 'ortools>=8.2.8710,<9.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'toposort>=1.6,<2.0',
 'xdg>=5.0.1,<6.0.0']

entry_points = \
{'console_scripts': ['wonk = wonk.cli:handle_command_line']}

setup_kwargs = {
    'name': 'wonk',
    'version': '0.5.1',
    'description': 'Wonk is a tool for combining a set of AWS policy files into smaller compiled policy sets.',
    'long_description': None,
    'author': 'Kirk Strauser',
    'author_email': 'kirk@amino.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
