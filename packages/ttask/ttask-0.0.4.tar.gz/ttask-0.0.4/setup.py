# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ttask']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "windows"': ['windows-curses']}

entry_points = \
{'console_scripts': ['ttask = ttask.main:main']}

setup_kwargs = {
    'name': 'ttask',
    'version': '0.0.4',
    'description': '',
    'long_description': None,
    'author': 'sleepntsheep',
    'author_email': 'contact@papangkorn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
