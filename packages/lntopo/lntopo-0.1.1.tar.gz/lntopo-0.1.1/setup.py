# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lntopo']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2',
 'networkx>=2.5,<3.0',
 'pyln-proto>=0.10,<0.11',
 'tqdm>=4.50,<5.0']

entry_points = \
{'console_scripts': ['lntopo-cli = lntopo.__main__:cli']}

setup_kwargs = {
    'name': 'lntopo',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Christian Decker',
    'author_email': 'decker.christian@gmail.com',
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
