# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['civichacker']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch-dsl>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'cybernetickit',
    'version': '0.1.0a1',
    'description': 'Python library for writing software with the intent to make social impact across multiple fields of study',
    'long_description': None,
    'author': 'Jurnell Cockhren',
    'author_email': 'jurnell@civichacker.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
