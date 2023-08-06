# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deeplib', 'deeplib.pipeline', 'deeplib.pipeline.osd', 'deeplib.platform']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deeplib',
    'version': '0.1.1.5',
    'description': '',
    'long_description': None,
    'author': 'Michael Kalashnikov',
    'author_email': 'kalashnikovsystem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
