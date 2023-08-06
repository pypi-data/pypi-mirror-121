# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['maptiler', 'maptiler.cloud_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['maptiler-cloud = maptiler.cloud_cli:cli']}

setup_kwargs = {
    'name': 'maptiler-cloud-cli',
    'version': '1.0.0',
    'description': 'CLI utility for MapTiler Cloud',
    'long_description': None,
    'author': 'MapTiler',
    'author_email': 'info@maptiler.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maptiler/maptiler-cloud-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
