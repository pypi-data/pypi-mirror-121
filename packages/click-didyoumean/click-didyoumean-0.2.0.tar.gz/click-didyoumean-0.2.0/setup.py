# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['click_didyoumean']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'click-didyoumean',
    'version': '0.2.0',
    'description': 'Enables git-like *did-you-mean* feature in click',
    'long_description': None,
    'author': 'Timo Furrer',
    'author_email': 'timo.furrer@roche.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
