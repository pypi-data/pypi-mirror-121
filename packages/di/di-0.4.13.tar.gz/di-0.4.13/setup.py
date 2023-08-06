# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['di', 'di.types']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3,<4']

setup_kwargs = {
    'name': 'di',
    'version': '0.4.13',
    'description': 'Autowiring dependency injection',
    'long_description': '# di: pythonic dependency injection\n\n[![codecov](https://codecov.io/gh/adriangb/di/branch/main/graph/badge.svg?token=A0FXC8B93Y)](https://codecov.io/gh/adriangb/di)\n![Test & Release](https://github.com/adriangb/di/actions/workflows/release.yaml/badge.svg)\n\n⚠️ This project is a WIP. Until there is a 1.X.Y release, expect breaking changes. ⚠️\n\nFor more information, see our [docs].\n\n[docs]: https://www.adriangb.com/di/\n\nSee this release on GitHub: [v0.4.13](https://github.com/adriangb/di/releases/tag/0.4.13)\n',
    'author': 'Adrian Garcia Badaracco',
    'author_email': 'adrian@adriangb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adriangb/di',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4',
}


setup(**setup_kwargs)
