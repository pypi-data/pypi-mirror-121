# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['di']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3,<4']

setup_kwargs = {
    'name': 'di',
    'version': '0.2.4',
    'description': 'Autowiring dependency injection',
    'long_description': 'None',
    'author': 'Adrian Garcia Badaracco',
    'author_email': 'adrian@adriangb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4',
}


setup(**setup_kwargs)
