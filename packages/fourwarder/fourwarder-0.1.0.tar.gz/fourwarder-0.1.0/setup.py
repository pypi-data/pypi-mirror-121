# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fourwarder']

package_data = \
{'': ['*']}

install_requires = \
['docker>=5.0.2,<6.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['fourwarder = fourwarder.main:run']}

setup_kwargs = {
    'name': 'fourwarder',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Giacomo Tagliabue',
    'author_email': 'giacomo.tag@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
