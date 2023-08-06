# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypstruct']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypstruct',
    'version': '0.1.1',
    'description': 'PDB coordinates management python package',
    'long_description': None,
    'author': 'glaunay',
    'author_email': 'pitooon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MMSB-MOBI/pypstruct',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
