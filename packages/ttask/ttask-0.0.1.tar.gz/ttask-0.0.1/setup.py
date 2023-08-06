# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ttask']

package_data = \
{'': ['*']}

install_requires = \
['windows-curses>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'ttask',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'sleepntsheep',
    'author_email': 'contact@papangkorn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
