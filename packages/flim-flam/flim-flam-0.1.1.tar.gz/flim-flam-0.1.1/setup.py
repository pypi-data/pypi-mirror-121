# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flim_flam']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.18.49,<2.0.0']

entry_points = \
{'console_scripts': ['flim-flam = flim_flam.cli:run']}

setup_kwargs = {
    'name': 'flim-flam',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'tlonny',
    'author_email': 't@lonny.io',
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
