# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['how_long_flameai']

package_data = \
{'': ['*']}

install_requires = \
['coo>=0.1.3,<0.2.0', 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'how-long-flameai',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
