# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rtspm']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=2.0.0,<3.0.0', 'numpy>=1.19.2,<2.0.0']

setup_kwargs = {
    'name': 'python-rtspm',
    'version': '0.1.0',
    'description': 'Python adaptation of SPM functions for real-time fMRI analysis',
    'long_description': '# python-rtspm\nSPM functions in Python for real-time fMRI\n',
    'author': 'OpenNFT Team',
    'author_email': 'opennft@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4',
}


setup(**setup_kwargs)
