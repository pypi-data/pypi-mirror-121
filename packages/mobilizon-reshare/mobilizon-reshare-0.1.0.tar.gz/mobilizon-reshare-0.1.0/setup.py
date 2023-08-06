# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mobilizon_reshare',
 'mobilizon_reshare.cli',
 'mobilizon_reshare.config',
 'mobilizon_reshare.event',
 'mobilizon_reshare.formatting',
 'mobilizon_reshare.mobilizon',
 'mobilizon_reshare.models',
 'mobilizon_reshare.publishers',
 'mobilizon_reshare.publishers.templates',
 'mobilizon_reshare.storage']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11,<3.0',
 'aiosqlite>=0.16,<0.17',
 'appdirs>=1.4,<2.0',
 'arrow>=1.1,<2.0',
 'beautifulsoup4>=4.9,<5.0',
 'click>=8.0,<9.0',
 'dynaconf>=3.1,<4.0',
 'markdownify>=0.9,<0.10',
 'requests>=2.25,<3.0',
 'tortoise-orm>=0.17,<0.18']

entry_points = \
{'console_scripts': ['mobilizon-reshare = '
                     'mobilizon_reshare.cli.cli:mobilizon_reshare']}

setup_kwargs = {
    'name': 'mobilizon-reshare',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Simone Robutti',
    'author_email': 'simone.robutti@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
