# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smc', 'smc.controllers', 'smc.models', 'smc.plugins']

package_data = \
{'': ['*'],
 'smc': ['www/*', 'www/static/css/*', 'www/static/js/*', 'www/static/media/*']}

install_requires = \
['Flask>=2.0.1,<3.0.0',
 'kgdata>=1.2.3,<2.0.0',
 'peewee>=3.14.4,<4.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'sem-desc>=0.1.15,<0.2.0',
 'tornado>=6.1,<7.0']

entry_points = \
{'console_scripts': ['smc = smc.cli:cli']}

setup_kwargs = {
    'name': 'sem-desc-curator',
    'version': '0.1.0',
    'description': 'UI for browsing/editing semantic descriptions',
    'long_description': None,
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
