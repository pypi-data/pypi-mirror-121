# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ttask']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "windows"': ['windows-curses>=2.2.0,<3.0.0']}

entry_points = \
{'console_scripts': ['ttask = ttask.main:main']}

setup_kwargs = {
    'name': 'ttask',
    'version': '0.1.3',
    'description': '',
    'long_description': '<div align="center">\n<h1>ttask (WIP)</h1>\ntui task manager built in python\n<hr>\n</div>\n\n\n## usages\n\nkey\n```\na: add new task\nr: remove selected task\nj, k/ up, down: navigate selected task/ property\nd: mark task as done \nw: write changes to todo.txt\nq: quit and write changes\ne: edit priority\n```\n\n## dependencies\n\nwindows:\n>  windows-curses\n\n## notes\n\ntodo.txt is put in your home folder',
    'author': 'sleepntsheep',
    'author_email': 'contact@papangkorn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sleepntsheep/ttask',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
