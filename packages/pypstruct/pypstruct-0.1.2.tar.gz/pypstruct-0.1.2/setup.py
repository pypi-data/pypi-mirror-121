# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypstruct']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.2,<2.0.0']

setup_kwargs = {
    'name': 'pypstruct',
    'version': '0.1.2',
    'description': 'PDB coordinates management python package',
    'long_description': None,
    'author': 'glaunay',
    'author_email': 'pitooon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MMSB-MOBI/pypstruct',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
