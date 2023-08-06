# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sleepwell']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'sleepwell',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Yves Tumushimire',
    'author_email': 'ytumushimire@truststamp.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
