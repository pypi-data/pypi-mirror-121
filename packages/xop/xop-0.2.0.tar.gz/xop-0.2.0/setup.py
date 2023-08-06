# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xop', 'xop.contrib', 'xop.processors', 'xop.serialization']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.3,<5.0.0']

setup_kwargs = {
    'name': 'xop',
    'version': '0.2.0',
    'description': 'XOP optimization for XML Infosets.',
    'long_description': 'XOP\n===\nThis library models the XOP binary content optimization for XML Infosets, and provides tools to aid the developer\nin dealing with XOP.\n\n_Work in progress._\n',
    'author': 'Bart Kleijngeld',
    'author_email': 'bartkl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
