# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deeplib']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.42.0,<4.0.0']

setup_kwargs = {
    'name': 'deeplib',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Michael Kalashnikov',
    'author_email': 'm.kalashnikov@quantumobile.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
