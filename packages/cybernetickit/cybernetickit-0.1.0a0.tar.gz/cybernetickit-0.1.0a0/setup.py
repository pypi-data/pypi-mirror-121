# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['civichacker']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch-dsl>=7.0.0,<8.0.0', 'stix2>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'cybernetickit',
    'version': '0.1.0a0',
    'description': 'The Cybernetic Kit is a set of conventions and techniques useful for making software-driven social impact.',
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
