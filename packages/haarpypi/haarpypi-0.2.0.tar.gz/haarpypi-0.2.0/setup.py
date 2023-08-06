# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haarpypi']

package_data = \
{'': ['*']}

install_requires = \
['testix>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'haarpypi',
    'version': '0.2.0',
    'description': 'haarpypi',
    'long_description': None,
    'author': 'Yoav Kleinberger',
    'author_email': 'haarcuba@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
