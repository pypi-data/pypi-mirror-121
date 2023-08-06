# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deeplib', 'deeplib.pipeline', 'deeplib.pipeline.osd', 'deeplib.platform']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deeplib',
    'version': '0.1.2.1',
    'description': 'Easy to understand and use api extention for DeepStream',
    'long_description': '<h2 align="center">\n    DeepLib\n</h2>\n\n<h6 align="center">\n    Fork of <a href="https://github.com/bluetiger9/DeepEye">DeepEye</a>\'s DeepLib\n</h6>\n\n<p align="center">\n\n<a href="https://pypi.org/project/deeplib/">\n<img alt="PyPI" src="https://img.shields.io/pypi/v/deeplib">\n</a>\n\n<a href="https://github.com/psf/black">\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=plastic">\n</a>\n\n<a href="https://github.com/m-v-kalashnikov/deeplib/blob/master/LICENSE">\n<img alt="license: MIT" src="https://img.shields.io/github/license/m-v-kalashnikov/deeplib?style=plastic">\n</a>\n\n<a href="https://pycqa.github.io/isort">\n<img alt="imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=plastic">\n</a>\n\n</p>\n\n---\n',
    'author': 'Michael Kalashnikov',
    'author_email': 'kalashnikovsystem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m-v-kalashnikov/deeplib',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '==3.6.9',
}


setup(**setup_kwargs)
