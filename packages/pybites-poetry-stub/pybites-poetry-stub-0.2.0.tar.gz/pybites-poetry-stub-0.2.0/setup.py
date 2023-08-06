# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypackage']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'pybites-poetry-stub',
    'version': '0.2.0',
    'description': 'Quick package to test automation of publishing to PyPI',
    'long_description': None,
    'author': 'Bob Belderbos',
    'author_email': 'bobbelderbos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
